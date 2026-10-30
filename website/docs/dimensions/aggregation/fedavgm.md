---
layout: concept
order: 14
math: true
description: Keep server momentum across rounds after averaging client model changes.
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

# FedAvgM

## Intuition

FedAvgM adds **server momentum** to model averaging. Local training produces client changes as in FedAvg; the server keeps a velocity across rounds. This is different from enabling momentum only inside each client's optimizer. [Hsu, Qi, and Brown, Section 4.2](https://arxiv.org/pdf/1909.06335v1#page=4).

## Update rule

We use a positive-displacement convention. For a selected cohort $S_t$, let $p_{k,t}=n_k/\sum_{j\in S_t}n_j$:

$$
\Delta_t=\sum_{k\in S_t}p_{k,t}(w_{t+1}^{(k)}-w_t),\qquad
v_{t+1}=\beta v_t+\Delta_t,\qquad
w_{t+1}=w_t+\eta_s v_{t+1}.
$$

Here $v$ is the server velocity, $0\leq\beta<1$ its decay, and $\eta_s$ the server learning rate. Initialize $v_0=0$. The paper uses the opposite model-difference sign and subtracts the velocity; the conventions are equivalent if used consistently. This recurrence does **not** multiply the current displacement by $(1-\beta)$; some optimizer libraries do, so matching names is insufficient for reproduction. The paper reports using **Nesterov momentum in its experiments**; the basic recurrence here explains its displayed momentum mechanism and does not reproduce those experimental optimizer details.

```text
broadcast w; clients train locally and return models
average their model displacements into delta
velocity = beta * velocity + delta
w = w + server_learning_rate * velocity
retain velocity for the next round
```

## Worked example

Take the returned models from our FedAvg example: 1.36 and 1.96, weighted 1/4 and 3/4, with current server model 1. Their mean displacement is $\Delta_t=0.81$.

For an illustrative existing velocity $v_t=0.2$, $\beta=0.9$, and $\eta_s=1$:

$$
v_{t+1}=0.9(0.2)+0.81=0.99,\qquad w_{t+1}=1.99.
$$

At initialization, $v_t=0$ would instead give 1.81 for this round. The retained state explains the difference; 1.99 is not evidence of a better model. Setting $\beta=0$ and $\eta_s=1$ recovers the normalized model average in the equations above.

## Assumptions and limits

Record both client and server learning rates, momentum convention, initialization, cohort weighting, and local work. Momentum can carry an unhelpful or adversarial direction forward. It is an optimization mechanism, not a poisoning defense or privacy guarantee. Report conclusions from the paper with its dataset and partition, rather than claiming a universal improvement.

## Self-check

<details><summary>Can resetting server velocity every round implement this recurrence?</summary><p>No. It removes the cross-round memory that defines server momentum.</p></details>

<details><summary>Does a larger parameter value mean better learning?</summary><p>No. Evaluate a defined loss or metric on appropriate data.</p></details>

<details><summary>What happens with beta = 0 and server learning rate = 1?</summary><p>The server adds the current mean displacement, giving this note's weighted model average.</p></details>

## Sources

**P012.** Hsu, Qi, and Brown. [Measuring the Effects of Non-Identical Data Distribution for Federated Visual Classification](https://arxiv.org/abs/1909.06335v1), 2019 preprint. Section 4.2 (PDF page 4) for server momentum; the surrounding Section 4 for experiments. Our numerical state is invented for explanation. Local copy: `ref-papers/hsu-2019-fedavgm-arxiv-v1.pdf`. [Paper bank](../../papers.md).
