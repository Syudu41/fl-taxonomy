---
layout: concept
order: 46
math: true
description: Minimize weighted Euclidean distances to submitted vectors; approximate it with smoothed Weiszfeld steps.
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

# Geometric median / RFA

## Intuition

The geometric median finds a central vector by minimizing total **Euclidean distance**, rather than squared distance. RFA uses an approximate geometric-median oracle within federated learning. It operates on whole-vector geometry, unlike taking a median coordinate by coordinate. [Pillutla, Kakade, and Harchaoui, Sections 2–3](https://arxiv.org/pdf/1912.13445v2#page=4).

## Update rule

For vectors $u_i$ and normalized nonnegative weights $p_i$:

$$
a\in\operatorname*{arg\,min}_{z\in\mathbb R^d}\sum_{i=1}^{m}p_i\lVert z-u_i\rVert_2.
$$

A smoothed Weiszfeld iteration with smoothing radius $\nu>0$ uses:

$$
q_i^{(r)}=\frac{p_i}{\max(\nu,\lVert z^{(r)}-u_i\rVert_2)},\qquad
z^{(r+1)}=\frac{\sum_i q_i^{(r)}u_i}{\sum_i q_i^{(r)}}.
$$

Smoothing avoids division by zero and corresponds to a smoothed problem. A finite iteration budget gives an approximation, not necessarily an exact minimizer of the unsmoothed objective. Record the starting point, $\nu$, stopping criterion, weights, and iteration count.

```text
initialize z, often from the weighted arithmetic mean
repeat for the declared iteration budget:
    distance[i] = max(smoothing_radius, norm(z - update[i]))
    q[i] = base_weight[i] / distance[i]
    z = sum(q[i] * update[i]) / sum(q[i])
return z as the approximate robust aggregate
```

## Worked example

For equal-weight scalar displacements $[0,1,10]$, the **exact** geometric median is 1. The mean is $11/3$. At 1 the unnormalized sum of distances is $1+0+9=10$; at $11/3$ it is $11/3+8/3+19/3=38/3$. Multiplying by 1/3 does not change the minimizer.

To expose the iterative calculation, start instead at $z^{(0)}=2$, choose $\nu=0.5$, and use weights 1/3. Distances are 2, 1, and 8, so $q=[1/6,1/3,1/24]$. One step gives:

$$
z^{(1)}=\frac{0/6+1/3+10/24}{1/6+1/3+1/24}=\frac{18}{13}\approx1.384615.
$$

That single smoothed step is **not** the exact median 1. In two or more dimensions, coordinate-wise and geometric medians can differ; the shared scalar median example does not make them interchangeable.

## Assumptions and limits

Robustness depends on the **total weight** of corruption as well as the geometry of honest updates. A small client count with very large weights can dominate. A weighted majority below 1/2 is a key condition in geometric-median robustness arguments, not an unconditional convergence guarantee. Approximation and non-IID effects still matter.

The paper implements its oracle using repeated secure weighted-average calls. A naive server implementation of the recurrence above that reads each vector and distance is **not** automatically secure aggregation. Treat protocol privacy and aggregation robustness as distinct requirements.

## Self-check

<details><summary>Which objective distinguishes this from a mean?</summary><p>The geometric median minimizes unsquared Euclidean distances. A weighted mean minimizes squared Euclidean distances.</p></details>

<details><summary>Does one Weiszfeld step necessarily return the exact median?</summary><p>No. Our example returns 18/13, not 1.</p></details>

<details><summary>Is corrupted client count sufficient for a weighted guarantee?</summary><p>No. The corrupt submissions' total weight matters.</p></details>

## Sources

**P011.** Pillutla, Kakade, and Harchaoui. [Robust Aggregation for Federated Learning](https://arxiv.org/abs/1912.13445v2), IEEE Transactions on Signal Processing 70:1142–1154, 2022. Stored copy is the author manuscript v2. Sections 2–3 define the oracle and RFA; Appendix C analyzes the smoothed Weiszfeld algorithm. Local copy: `ref-papers/pillutla-2022-robust-aggregation-arxiv-v2.pdf`. [Paper bank](../../papers.md).
