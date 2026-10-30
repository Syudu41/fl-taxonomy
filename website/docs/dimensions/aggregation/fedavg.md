---
layout: concept
order: 10
math: true
description: Derive sample-weighted averaging and work through two local training steps on two clients.
coverage:
  overview: true
  math: true
  example: true
  sources: true
  check: true
section_anchors:
  overview: intuition
  math: the-learning-objective
  example: one-complete-round
  sources: sources-and-reading-route
  check: self-check
---

# FedAvg

**Reading state: sourced algorithm note with a worked round.** Begin with the [learning foundations](../../foundations.md) if gradients or local training are unfamiliar. This page separates the algorithm described in the paper, our derivation, and our hand calculation. It is not a benchmark reproduction.

## Intuition

Clients train a shared starting model on local data. The server takes a weighted average of their resulting parameter vectors, then repeats the process. FedAvg includes both local optimization and model aggregation. [McMahan et al., Section 2 and Algorithm 1](https://proceedings.mlr.press/v54/mcmahan17a/mcmahan17a.pdf#page=4).

## The learning objective

Let $D_k$ contain client $k$'s $n_k$ training examples. Define its mean loss:

$$
F_k(w)=\frac{1}{n_k}\sum_{i\in D_k}\ell_i(w).
$$

For $K$ clients and $n=\sum_{k=1}^{K}n_k$, the sample-weighted global objective is:

$$
\min_w F(w), \qquad F(w)=\sum_{k=1}^{K}\frac{n_k}{n}F_k(w).
$$

**Why those weights?** Substitute the definition of $F_k$:

$$
\sum_{k=1}^{K}\frac{n_k}{n}\left(\frac{1}{n_k}\sum_{i\in D_k}\ell_i(w)\right)
=\frac{1}{n}\sum_{k=1}^{K}\sum_{i\in D_k}\ell_i(w).
$$

The cancellation makes every training example contribute equally to this pooled empirical objective. Equal client weighting is a different objective when sample counts differ. This algebra explains the objective's weights; it does not prove arbitrary parameter averaging solves that objective. **Source:** Section 2, Equation (1) and the partitioned objective immediately following it. The substitution above is our explicit working of that identity.

## Local training, then averaging

For this page, all clients participate and use a compatible parameterization. Every client starts a round from the same server model $w_t$. A local minibatch step has the form:

$$
w\leftarrow w-\eta\nabla\ell(w;b).
$$

After its local steps, client $k$ returns $w_{t+1}^{(k)}$. The server forms:

$$
w_{t+1}=\sum_{k=1}^{K}\frac{n_k}{n}w_{t+1}^{(k)}.
$$

| Symbol | Meaning |
| --- | --- |
| $t$ | Communication round |
| $w_t$ | Server model at the start of a round |
| $w_{t+1}^{(k)}$ | Client $k$'s model after local training |
| $n_k/n$ | Client's sample-count weight |
| $\eta$ | Local learning rate |
| $b$ | Local minibatch; its loss is averaged in this note |

**Source:** Algorithm 1, PDF page 5. This introductory treatment assumes **full participation**. The participation section below makes a separate normalized-cohort convention explicit for future implementations.

## Executing a round

```text
server initializes compatible model parameters w
repeat communication rounds:
    select a nonempty cohort S and broadcast the same w to every member
    for each client k in S, in parallel:
        local_w = copy(w)
        repeat E local epochs:
            for each local minibatch b:
                local_w -= client_learning_rate * gradient(mean_loss(local_w, b))
        return local_w and the declared local sample count
    w = weighted_mean(returned_models, declared_weights)
```

An **epoch** is a local pass through data, not one communication round or one minibatch. The original method specifies client fraction $C$, local epochs $E$, batch size $B$, and learning rate $\eta$. Parameter averaging requires the same parameter layout; averaging losses or predictions would be different operations. [McMahan et al., Algorithm 1](https://proceedings.mlr.press/v54/mcmahan17a/mcmahan17a.pdf#page=5).

### Participation and normalization

The worked example below uses all clients, so the denominator is unambiguous. For an implementation with selected cohort $S_t$, one explicitly defined **normalized cohort convention** is:

$$
p_{k,t}=\frac{n_k}{\sum_{j\in S_t}n_j},\qquad
w_{t+1}=\sum_{k\in S_t}p_{k,t}w_{t+1}^{(k)}.
$$

Its weights sum to one over the clients whose models were actually received. The printed original Algorithm 1 instead shows $n_k/n$ inside the selected-client sum, with $n$ introduced for the full objective. Do not silently equate these expressions under partial participation. Record sampling, denominator, dropout policy, and any treatment of nonparticipants. Our FedAvgM/FedOpt examples declare normalized cohort weighting; SCAFFOLD follows its own uniform-client convention.

Neither selecting clients nor renormalizing automatically makes an update an unbiased estimate of a full-population objective. If clients have unequal inclusion probabilities, the sampling and weighting need joint analysis. This note supplies a reproducible convention, not a sampling theorem.

### Parameters and model changes

With normalized weights, define $\Delta_k=w_{t+1}^{(k)}-w_t$. Then:

$$
w_t+\sum_{k\in S_t}p_{k,t}\Delta_k
=\sum_{k\in S_t}p_{k,t}w_{t+1}^{(k)}.
$$

This identity explains why transmitting model changes can implement the same average. All clients must refer to the same starting model, and the signs and coefficients must match. These algebraic equivalences are our explicit derivations.

## One complete round

This is our invented arithmetic example, not a published experimental result. Model: $\hat y=wx$; loss: $(wx-y)^2$; shared start: $w_t=1$; learning rate: 0.1. Each client takes **two full-batch local steps**.

Client A has one example $(1,2)$. Client B has three identical copies of $(2,4)$, chosen deliberately to make the calculation easy. Its *mean* loss is still $(2w-4)^2$, not three times that value.

| Local operation | Client A | Client B |
| --- | --- | --- |
| Starting model | 1 | 1 |
| First gradient | $2(1-2)=-2$ | $4(2-4)=-8$ |
| After first step | $1-0.1(-2)=1.2$ | $1-0.1(-8)=1.8$ |
| Second gradient | $2(1.2-2)=-1.6$ | $4(3.6-4)=-1.6$ |
| Returned parameter | $1.2+0.16=1.36$ | $1.8+0.16=1.96$ |

With weights $1/4$ and $3/4$:

$$
w_{t+1}=\frac14(1.36)+\frac34(1.96)=1.81.
$$

Both clients started at 1; they did not start from one another's updated model. The server aggregated only after the two local steps. The repeated data and common optimum make this an illustration of mechanics, not a test of statistical heterogeneity, privacy, robustness, or generalization.

<details><summary>Why not simply call this two centralized training steps?</summary><p>Clients evaluate their second gradient at different local models: A at 1.2, B at 1.8. A centralized procedure would evaluate at the shared updated model. These are different computation paths.</p></details>

## Assumptions and limits

- This worked round assumes full participation, trusted sample counts, synchronous updates, and honest clients with compatible models.
- Sample count is a weighting choice, not a measure of trustworthiness.
- Local data can have different distributions. More local work changes the optimization path; the paper's experimental findings must be read with their settings.
- Keeping raw data local does not establish privacy. The original paper discusses update leakage in Section 1, Privacy, including its footnote.
- A weighted mean does not filter malicious updates. Security requires an explicit threat model and additional analysis.

Algorithm 1 specifies client fraction $C$, local epochs $E$, minibatch size $B$, and learning rate $\eta$. Read those together with the results in Section 3. We have not reproduced the paper's convergence or communication experiments.

## Self-check

<details><summary>1. Why does a client with three times as many samples get three times the weight here?</summary><p>The chosen global objective gives each example equal weight. Substituting each client's mean loss produces the sample-count coefficients. Equal client weighting would express another objective.</p></details>

<details><summary>2. Does the server average the losses or the returned model parameters?</summary><p>In the averaging step shown here it averages returned parameters. The objective is defined using losses, but a loss is not itself a parameter vector.</p></details>

<details><summary>3. Why is client B's local mean loss not multiplied by three?</summary><p>It averages three identical losses. The factor of three cancels with the local 1/3 normalization. B's sample count still affects its server aggregation weight.</p></details>

<details><summary>4. What should be understood before studying a defense?</summary><p>Which actor may be malicious, what it can observe or change, what it aims to achieve, and which property the defense claims to protect. A privacy mechanism and a poisoning defense need not address the same threat.</p></details>

## Sources and reading route

**P001.** McMahan, Moore, Ramage, Hampson, and Agüera y Arcas. *Communication-Efficient Learning of Deep Networks from Decentralized Data*. AISTATS 2017, PMLR 54:1273–1282. [Official record](https://proceedings.mlr.press/v54/mcmahan17a.html) · [PDF](https://proceedings.mlr.press/v54/mcmahan17a/mcmahan17a.pdf).

Read Section 1 for the setting; Section 2 for the objective; Algorithm 1 for execution; then Section 3 before repeating performance claims. PDF page numbers count from the first page of the file. A local reading copy is in `ref-papers/mcmahan-2017-fedavg.pdf`.

Continue with [FedSGD](fedsgd.md), [FedAvgM](fedavgm.md), [FedProx](fedprox.md), [SCAFFOLD](scaffold.md), or [adaptive server optimization](fedopt.md). Next research tasks: make a claim/section record and design a small reproducible experiment with a declared participation convention. Comparisons and a secure-FL proposal remain pending until the survey supports them. Open the [paper bank](../../papers.md) for the current reading collection.
