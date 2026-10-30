---
layout: concept
order: 42
math: true
description: Remove extreme entries in each coordinate and average the retained values.
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

# Coordinate-wise trimmed mean

## Intuition

A trimmed mean discards a chosen number of the largest and smallest values **per coordinate**, then averages what remains. It retains averaging among central values without giving the extremes their original influence. [Yin et al., Section 3](https://proceedings.mlr.press/v80/yin18a/yin18a.pdf#page=3).

## Update rule

For $m$ vectors, sort coordinate $j$ into $u_{(1),j}\leq\cdots\leq u_{(m),j}$. With integer trim count $b\geq0$ and $m>2b$:

$$
[a]_j=\frac{1}{m-2b}\sum_{r=b+1}^{m-b}u_{(r),j}.
$$

The paper parameterizes trimming as a fraction; an implementation must specify how that fraction maps to an integer. Here $b$ is directly the number removed **at each tail**, not the total number removed. This is an unweighted coordinate rule.

```text
require number_of_submissions > 2 * trim_count
for each coordinate:
    sort its values
    remove trim_count values from each tail
    average the retained values
```

## Worked example

Use five scalar displacements $[-100,1,2,3,100]$ and $b=1$. Remove −100 and 100, then compute $(1+2+3)/3=2$. The plain mean is $6/5=1.2$. With $b=0$, all five values are retained and the rule becomes the ordinary unweighted mean.

In multiple dimensions different entries can be removed in different coordinates. The procedure does **not** necessarily exclude the same clients as whole vectors. If five submitted vectors have different coordinate rankings, their retained-client sets can differ across coordinates.

## Assumptions and limits

A bound on the corruption fraction informs trimming, but counting alone does not establish learning robustness. Over-trimming loses useful honest information; under-trimming can retain adversarial values. Non-extreme attacks can remain in the retained set. The original statistical results require assumptions on honest gradients and losses; using this rule for non-IID local model deltas is a separate setting needing validation. It does not provide confidentiality.

## Self-check

<details><summary>With m = 5 and b = 1, how many values remain per coordinate?</summary><p>Three: remove one from each of two tails.</p></details>

<details><summary>Can b = 3 be used with five submissions?</summary><p>No. It violates m greater than 2b and leaves no valid central set.</p></details>

<details><summary>Are whole clients necessarily removed?</summary><p>No. Coordinate-wise rankings can select different retained subsets.</p></details>

## Sources

**P009.** [Yin et al., ICML 2018](https://proceedings.mlr.press/v80/yin18a.html), Section 3 for the trimmed-mean operator and later theorems for statistical assumptions. Local copy: `ref-papers/yin-2018-byzantine-robust.pdf`. This example and pseudocode are our teaching calculations. [Paper bank](../../papers.md).
