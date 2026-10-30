---
layout: concept
order: 16
math: true
description: Penalize local movement away from the broadcast model before averaging client outputs.
coverage:
  overview: true
  math: true
  example: true
  sources: true
  check: true
section_anchors:
  overview: intuition
  math: update-rule
  example: worked-example
  sources: sources
  check: self-check
---

# FedProx

## Intuition

FedProx changes the **client optimization problem**. Each client is encouraged to fit its local data while remaining near the broadcast model. A proximal penalty is added locally; a model mean remains at the server. It addresses heterogeneity rather than introducing a malicious-update filter. [Li et al., Section 3, Algorithm 2](https://proceedings.mlsys.org/paper/2020/file/1f5fe83998a09396ebe6477d9475ba0c-Paper.pdf#page=4).

## Update rule

For current global model $w_t$ and local mean loss $F_k$, the client approximately minimizes:

$$
h_k(w;w_t)=F_k(w)+\frac{\mu}{2}\lVert w-w_t\rVert_2^2,\qquad \mu\geq 0.
$$

A local gradient step is:

$$
w\leftarrow w-\eta\left[\nabla F_k(w)+\mu(w-w_t)\right].
$$

The reference $w_t$ stays fixed throughout the round. For this note's **full-participation, sample-weighted illustration**, aggregate the returned models with $w_{t+1}=\sum_k(n_k/n)w_{t+1}^{(k)}$. The paper's Algorithm 2 instead samples devices using objective weights and averages the selected outputs uniformly. Do not substitute our demonstration convention silently into its theorem or implementation.

```text
broadcast w_reference
for each client in parallel:
    w_local = w_reference
    repeat local steps:
        grad = local_loss_gradient(w_local) + mu * (w_local - w_reference)
        w_local = w_local - learning_rate * grad
average returned models using the declared cohort-weighting convention
```

## Worked example

Use the same two clients as the FedAvg note, shared start 1, learning rate 0.1, two full-batch steps, and choose $\mu=1$.

| Operation | A: one (1,2) example | B: three (2,4) examples |
| --- | --- | --- |
| Initial proximal gradient | 0 | 0 |
| First local parameter | 1.2 | 1.8 |
| Second data-loss gradient | −1.6 | −1.6 |
| Second penalty gradient | 0.2 | 0.8 |
| Second total gradient | −1.4 | −0.8 |
| Returned parameter | 1.34 | 1.88 |

The weighted result is $\tfrac14(1.34)+\tfrac34(1.88)=1.745$. The first step matches FedAvg because $w-w_t=0$ initially. The second step reveals the penalty. This is our hand calculation, not a measurement of convergence or accuracy.

## Assumptions and limits

$\mu$ controls a trade-off and needs tuning; it does not certify closeness of data distributions. With $\mu=0$ and identical local solver, work, participation, and weighting, the penalty disappears. Approximate solving and differing local work need to be documented. The paper's convergence analysis has smoothness, dissimilarity, and solution-accuracy conditions; its name alone supplies no guarantee for an arbitrary neural network or attacker.

## Self-check

<details><summary>Why is the proximal gradient zero at the beginning?</summary><p>Each client starts exactly at the fixed reference model, so mu times their difference is zero.</p></details>

<details><summary>Should the penalty reference move after every local step?</summary><p>No. It is the server model broadcast at the beginning of that round.</p></details>

<details><summary>Does the proximal term identify malicious clients?</summary><p>No. It regularizes honest local optimization and is not a Byzantine filter.</p></details>

## Sources

**P006.** Li, Sahu, Zaheer, Sanjabi, Talwalkar, and Smith. [Federated Optimization in Heterogeneous Networks](https://proceedings.mlsys.org/paper_files/paper/2020/hash/1f5fe83998a09396ebe6477d9475ba0c-Abstract.html), MLSys 2020. Read Section 3 and Algorithm 2 for the objective/protocol, Section 4 before citing convergence, and Section 5 for experimental conditions. Local copy: `ref-papers/li-2020-fedprox-mlsys.pdf`. [Paper bank](../../papers.md).
