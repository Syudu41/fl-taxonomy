---
layout: concept
order: 20
math: true
description: Average client displacements, then apply a stateful adaptive server optimizer.
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

# FedOpt: FedAdagrad, FedAdam, and FedYogi

## Intuition

FedOpt separates client optimization from server optimization. The server first averages client displacements, then feeds that direction into its own optimizer. FedAdagrad, FedAdam, and FedYogi use different second-moment recurrences. They are a family of federated optimization procedures, rather than three ways to compute an ordinary arithmetic mean. [Reddi et al., Section 3, Algorithms 1–2](https://sanjivk.com/adaptive_federated_optimization_ICLR2021.pdf#page=3).

## Update rule

Use **positive model displacement** $\Delta_t=\sum_{k\in S_t}p_{k,t}(w_{t+1}^{(k)}-w_t)$, with normalized cohort weights $p_{k,t}$. The paper's theoretical pseudocode uses a uniform cohort mean; its experiments also discuss sample-count weighting. State which you implement.

The shared momentum update and server step are:

$$
m_t=\beta_1 m_{t-1}+(1-\beta_1)\Delta_t,\qquad
w_{t+1}=w_t+\eta_s\frac{m_t}{\sqrt{v_t}+\tau}.
$$

All squaring, square roots, division, and sign operations below are **coordinate-wise**. The positive sign follows our displacement convention; treating $\Delta_t$ as a positive loss gradient and subtracting this same expression would reverse the intended direction.

### FedAdagrad

$$
v_t=v_{t-1}+m_t^2.
$$

### FedAdam

$$
v_t=\beta_2v_{t-1}+(1-\beta_2)m_t^2.
$$

### FedYogi

$$
v_t=v_{t-1}-(1-\beta_2)m_t^2\operatorname{sign}(v_{t-1}-m_t^2).
$$

Here $\eta_s$ is a server learning rate and $\tau>0$ stabilizes the denominator. This follows the printed Algorithm 2: its symbol for the displacement is overwritten by the momentum-filtered value, so its accumulator uses **$m_t^2$** in our separate notation. Some implementations instead accumulate the raw averaged displacement squared. That is a different convention when $\beta_1>0$. These are **uncorrected moments**, not bias-corrected Adam. Record $m_{-1}$, $v_{-1}$, $\tau$, both decay factors, and the client optimizer before attempting a reproduction. The paper initializes $m_{-1}=0$ and $v_{-1}\geq\tau^2$.

```text
clients train from a common server model
server averages returned model displacements into delta
update first moment m from delta
update second moment v using the chosen recurrence on m squared
server adds server_learning_rate * m / (sqrt(v) + tau)
retain both moments for the next round
```

## Worked example

Our single-coordinate FedAdagrad example chooses current $w=1$, mean displacement $\Delta=0.5$, old $m=0$, old $v=0.01$, $\beta_1=0$, $\tau=0.1$, and $\eta_s=0.1$:

$$
m=0.5,\qquad v=0.01+0.5^2=0.26,\qquad
w_{\mathrm{new}}=1+\frac{0.1(0.5)}{\sqrt{0.26}+0.1}\approx1.081980.
$$

An ordinary mean model with that displacement would be 1.5. The example makes the server transformation visible; the smaller movement is not a claim of better accuracy. For the **same incoming state**, choosing $\beta_2=0.9$ gives $v=0.034$ under FedAdam and $v=0.035$ under FedYogi. They can diverge even on their first shown update because the nonzero initialization participates differently.

## Assumptions and limits

Adaptivity changes update scaling, not client honesty or confidentiality. Coordinate-wise state adds server memory. Learning rates, stabilizers, initial accumulators, sparse coordinates, and partition choices can materially affect behavior. Do not transfer the paper's convergence results beyond their stated assumptions or infer universal performance rankings from an optimizer name.

## Self-check

<details><summary>Where is the adaptive optimizer applied?</summary><p>At the server, to an averaged client displacement. Clients still use their own declared optimizer.</p></details>

<details><summary>Why is the server update added?</summary><p>Delta was defined as returned client model minus starting server model, so it is a displacement rather than a positive gradient.</p></details>

<details><summary>Does this note use Adam bias correction?</summary><p>No. It follows the printed uncorrected-moment Algorithm 2, including its use of the momentum-filtered displacement in the accumulator. Check both choices in any implementation.</p></details>

## Sources

**P008.** Reddi et al. [Adaptive Federated Optimization, author publication page](https://research.google/pubs/adaptive-federated-optimization/), ICLR 2021. [Author-hosted paper](https://sanjivk.com/adaptive_federated_optimization_ICLR2021.pdf): Section 3, Algorithms 1–2 for recurrences; Section 4 for analysis; Section 5 for experiments; Appendix B for implementation details. Local copy: `ref-papers/reddi-2021-adaptive-federated-optimization.pdf`. [Paper bank](../../papers.md).
