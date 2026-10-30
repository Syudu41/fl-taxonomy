---
layout: concept
order: 30
math: true
description: Define the attacker and the honest-update assumptions before choosing a robust aggregation rule.
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

# Robust aggregation: setting and assumptions

## Intuition

Averages give every submitted value influence; a single unbounded malicious vector can move a mean arbitrarily. Robust aggregation asks how to combine contributions when some may be corrupted. It is a **problem family**, not one algorithm. Start with a threat model before studying [median](coordinate-wise-median.md), [trimmed mean](trimmed-mean.md), [Krum](krum.md), or [geometric median/RFA](geometric-median.md).

## Update rule

For an unweighted mean of $m$ submitted vectors, write:

$$
a=\frac1m\left(\sum_{i=1}^{m-1}u_i+u_{\mathrm{bad}}\right).
$$

If an attacker can choose $u_{\mathrm{bad}}$ freely, it can force any desired aggregate $a^*$ by choosing:

$$
u_{\mathrm{bad}}=m a^*-\sum_{i=1}^{m-1}u_i.
$$

This is our direct algebraic illustration of why an unrestricted mean has unbounded influence. It assumes an attacker that knows the other submissions; weaker attackers require a separately defined analysis. [Blanchard et al., Section 3](https://proceedings.neurips.cc/paper/2017/file/f4b9ec30ad9f68f89b29639786cb62ef-Paper.pdf#page=3).

```text
declare whether inputs are gradients, parameters, or model displacements
state who can alter them, and how many or how much weight can be corrupt
check the chosen rule's requirements against cohort size and honest data
apply that rule with fixed hyperparameters and tie conventions
interpret its output using the declared model-update convention
```

## Worked example

Four honest scalar displacements are $[1,1,1,1]$. A fifth arbitrary submission of 100 makes the ordinary mean $104/5=20.8$. To force a mean of −10, an all-knowing attacker could instead send $5(-10)-4=-54$.

The median of the first list with 100 is 1. That arithmetic observation does not establish robust learning for arbitrary neural networks, a heterogeneous honest population, or adaptive attackers. It only exposes the effect of one extreme scalar submission in this invented setting.

## Specify the setting first

Record the following in a method or experiment note:

- **Object:** full gradients at one shared model, local model changes, or parameter vectors; dimensions and synchronization.
- **Attacker:** control of labels/data versus arbitrary messages; knowledge of the model, other updates, and defenses; number or total weight of corrupt clients; collusion and Sybil assumptions.
- **Honest population:** common versus heterogeneous objectives, gradient concentration/noise assumptions, and sample sizes.
- **Protocol:** selected cohort, dropout, authenticated identities, weights, inspection access, clipping, and communication visibility.
- **Claim:** convergence, estimation error, clean accuracy, attack success, or confidentiality. Define exactly what is measured.

## Assumptions and limits

A Byzantine-gradient theorem is not automatically a theorem for non-IID multi-epoch FedAvg. Outliers are not necessarily attackers. Confidentiality mechanisms can hide individual messages that an inspection-based defense needs; combining the two requires a protocol design, not just enabling both flags. RFA studies one construction using secure-average oracles. [Pillutla et al., Sections 2–3](https://arxiv.org/pdf/1912.13445v2).

## Self-check

<details><summary>Is robust aggregation one named rule?</summary><p>No. It is a problem setting with multiple operators and different assumptions.</p></details>

<details><summary>Does an honest but unusual update establish Byzantine behavior?</summary><p>No. Honest data heterogeneity can produce unusual updates.</p></details>

<details><summary>Does resisting poisoning establish confidentiality?</summary><p>No. Robustness and information disclosure are different properties.</p></details>

## Sources

**P010.** [Blanchard et al., NeurIPS 2017](https://proceedings.neurips.cc/paper_files/paper/2017/hash/f4b9ec30ad9f68f89b29639786cb62ef-Abstract.html), Sections 3–4 for Byzantine aggregation and Krum. **P009.** [Yin et al., ICML 2018](https://proceedings.mlr.press/v80/yin18a.html), Sections 3–5 for coordinate rules and statistical assumptions. **P011.** [Pillutla et al., 2022 author manuscript](https://arxiv.org/abs/1912.13445v2), Sections 2–3 for the RFA oracle. These are source-linked explanatory notes, not a completed paper-comparison module or verified defense implementation. [Paper bank](../../papers.md).
