---
layout: concept
order: 44
math: true
description: Select one submitted vector with a small nearest-neighbor distance score.
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

# Krum

## Intuition

Krum scores each submission by distances to its nearest neighboring submissions and selects **one whole vector**. It is a selection rule, not an arithmetic average. [Blanchard et al., Section 4](https://proceedings.neurips.cc/paper/2017/file/f4b9ec30ad9f68f89b29639786cb62ef-Paper.pdf#page=4).

## Update rule

Let $m$ vectors $u_1,\ldots,u_m$ be submitted, with an assumed upper bound $f$ on Byzantine workers. Let $N_i$ contain the $m-f-2$ nearest **other** vectors to $u_i$, under Euclidean distance. Define:

$$
s_i=\sum_{j\in N_i}\lVert u_i-u_j\rVert_2^2,\qquad
i^*=\operatorname*{arg\,min}_i s_i,\qquad a=u_{i^*}.
$$

The original resilience result requires $m>2f+2$, plus its assumptions on honest stochastic gradients and their noise relative to the true gradient. The count condition alone is not a guarantee. Resolve equal scores deterministically, for example by smallest client identifier as in the paper.

```text
require m > 2*f + 2 for the original stated setting
for each submitted vector i:
    compute squared distances to all other vectors
    score[i] = sum of the m-f-2 smallest distances
return the submitted vector with minimum score
```

## Worked example

Our scalar vectors are $[0,0.1,0.2,0.3,10]$, with $m=5$, $f=1$. Each score sums its **two** nearest other squared distances:

| Submission | Two nearest squared distances | Score |
| --- | --- | --- |
| 0 | 0.01, 0.04 | 0.05 |
| 0.1 | 0.01, 0.01 | 0.02 |
| 0.2 | 0.01, 0.01 | 0.02 |
| 0.3 | 0.01, 0.04 | 0.05 |
| 10 | 94.09, 96.04 | 190.13 |

With client identifiers following the displayed order, choose 0.1 from the tied minimum. This calculation shows the selection mechanism. It does not establish that the selected client is honest, nor that clustering proves benign behavior.

## Assumptions and limits

Krum performs pairwise distance work, $O(m^2d)$ in the paper's analysis for $d$ coordinates. Honest non-IID local updates can be far apart. A theorem for common-objective stochastic gradients cannot be transferred automatically to arbitrary local training. **Multi-Krum is a separate extension** that selects multiple candidates and averages them; do not call its output the original single-vector Krum rule. Neither variant inherently hides individual submissions.

## Self-check

<details><summary>How many neighbors are used with five submissions and f = 1?</summary><p>Two: 5 − 1 − 2. The candidate itself is excluded.</p></details>

<details><summary>Is the output a coordinate-wise mixture?</summary><p>No. Original Krum returns one submitted vector intact.</p></details>

<details><summary>Does m greater than 2f + 2 suffice for arbitrary FL convergence?</summary><p>No. The original noise, gradient, and other assumptions must also hold; heterogeneous local-training updates are a different setting.</p></details>

## Sources

**P010.** Blanchard, El Mhamdi, Guerraoui, and Stainer. [Machine Learning with Adversaries: Byzantine Tolerant Gradient Descent](https://proceedings.neurips.cc/paper_files/paper/2017/hash/f4b9ec30ad9f68f89b29639786cb62ef-Abstract.html), NeurIPS 2017. Sections 3–4 define resilience, Krum, and its assumptions. Local copy: `ref-papers/blanchard-2017-krum.pdf`. Our scalar example is original. [Paper bank](../../papers.md).
