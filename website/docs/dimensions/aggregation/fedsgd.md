---
layout: concept
order: 12
math: true
description: Average gradients evaluated at a shared model, then take one server step.
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

# FedSGD

## Intuition

FedSGD is a useful starting point for understanding what FedAvg changes: clients compute gradients at the **same** model, the server averages them, and one update follows. In the original FedAvg study, its full-batch baseline uses one local step per communication round. Read [FedAvg](fedavg.md) after this note. [McMahan et al., Section 2](https://proceedings.mlr.press/v54/mcmahan17a/mcmahan17a.pdf#page=4).

## Update rule

For full participation, client mean loss $F_k$, sample count $n_k$, and $n=\sum_k n_k$:

$$
g_k=\nabla F_k(w_t),\qquad
g=\sum_{k=1}^{K}\frac{n_k}{n}g_k,\qquad
w_{t+1}=w_t-\eta g.
$$

Because differentiation is linear, $g=\nabla F(w_t)$ for the sample-weighted objective $F=\sum_k(n_k/n)F_k$. This identity uses **full local gradients evaluated at the same point**, not gradients evaluated after different local trajectories.

```text
server broadcasts w
for each client k in parallel:
    g[k] = gradient of its mean loss at w
server sets g = sum(n[k] / total_samples * g[k])
server sets w = w - learning_rate * g
```

Sending $w-\eta g_k$ and averaging those models gives the same result when all clients use the same learning rate and exactly one such step. A one-epoch run with many minibatches is not this special case. With randomly sampled minibatch gradients, equality to the full empirical gradient no longer holds for every realization; expectation statements require a sampling convention.

## Worked example

Our hand calculation uses $\hat y=wx$, squared error, $w_t=1$, and $\eta=0.1$. A has one example $(1,2)$; B has three identical copies of $(2,4)$, so its mean loss remains $(2w-4)^2$.

- A returns gradient $2(w-2)=-2$.
- B returns gradient $4(2w-4)=-8$.
- The server forms $g=\tfrac14(-2)+\tfrac34(-8)=-6.5$.
- The updated parameter is $1-0.1(-6.5)=1.65$.

A and B's one-step models would be 1.2 and 1.8; their weighted average is also 1.65. The two-local-step FedAvg calculation instead produces 1.81 because its second gradients are evaluated at different local parameters. These are arithmetic examples, not performance results.

## Assumptions and limits

Full gradients can require substantial local computation, and each step requires a communication round. Client dropout changes the participating objective unless the protocol accounts for it. Gradient averaging alone neither hides the gradients nor rejects malicious ones. Compatible parameter shapes and a common starting model are required.

## Self-check

<details><summary>Is FedSGD the same as averaging training losses?</summary><p>No. Loss values are scalars; this server averages gradient vectors and uses them to update parameters.</p></details>

<details><summary>When is one-step model averaging equivalent?</summary><p>When the same model, learning rate, gradient definition, and client weights are used, with exactly one local gradient step.</p></details>

<details><summary>Is one local epoch necessarily one step?</summary><p>No. An epoch can contain many minibatches and therefore many steps.</p></details>

## Sources

**P001.** [McMahan et al., AISTATS 2017, official record](https://proceedings.mlr.press/v54/mcmahan17a.html). Section 2 describes FedSGD and its relation to FedAvg. The example and algebra above are our own. [Paper bank](../../papers.md).
