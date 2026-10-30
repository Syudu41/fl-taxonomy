---
layout: concept
order: 40
math: true
description: Choose the middle value separately in each coordinate instead of averaging vectors.
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

# Coordinate-wise median

## Intuition

A coordinate-wise median sorts each coordinate independently and takes its middle value. It limits the influence of extreme entries, but it can assemble a vector that no client submitted. [Yin et al., Section 3](https://proceedings.mlr.press/v80/yin18a/yin18a.pdf#page=3).

## Update rule

Given $m$ submitted vectors $u_i\in\mathbb R^d$, coordinate $j$ of the aggregate is:

$$
[a]_j=\operatorname{median}\{[u_1]_j,\ldots,[u_m]_j\}.
$$

For even $m$, this note uses the mean of the two middle values. Declare the tie convention in code. When inputs are gradients, use $w_{t+1}=w_t-\eta a$; when inputs are positive model displacements, use $w_{t+1}=w_t+a$. Do not mix these two meanings.

```text
for each coordinate j:
    sort the submitted j-th coordinates
    take the median using the declared even-count convention
return the assembled vector
```

## Worked example

Our three submitted vectors are $(0,0)$, $(1,100)$, and $(100,1)$. The coordinate lists are both $[0,1,100]$, so the result is $(1,1)$. The coordinate means would both be $101/3\approx33.667$. No submitted vector equals the median result.

A median need not identify an attacker. In this invented example we have not even labeled any vector malicious. Different honest data can also produce spread-out values.

## Assumptions and limits

Fewer than half arbitrarily corrupted submissions is a basic median intuition, **not a complete learning theorem**. Honest-coordinate concentration, dimension, loss regularity, and data assumptions still matter. The cited analysis studies distributed gradient learning under its own statistical model, not unrestricted heterogeneous multi-step FL. Coordinates are treated separately, so rotating the representation can change the result. This unweighted rule does not preserve FedAvg's sample-weighted mean objective automatically.

## Self-check

<details><summary>Must the aggregate be a submitted vector?</summary><p>No. Each coordinate can come from a different submission, as the example shows.</p></details>

<details><summary>Is a large coordinate proof of an attack?</summary><p>No. Honest heterogeneous data can also cause disagreement.</p></details>

<details><summary>Does using a median guarantee privacy?</summary><p>No. This arithmetic operation says nothing about who can observe the submissions.</p></details>

## Sources

**P009.** Yin, Chen, Ramchandran, and Bartlett. [Byzantine-Robust Distributed Learning: Towards Optimal Statistical Rates](https://proceedings.mlr.press/v80/yin18a.html), ICML 2018, PMLR 80:5650–5659. Section 3 defines the operators; Sections 4–5 state model-dependent rates. Local copy: `ref-papers/yin-2018-byzantine-robust.pdf`. The example is our own. [Paper bank](../../papers.md).
