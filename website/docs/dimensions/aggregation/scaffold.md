---
layout: concept
order: 18
math: true
description: Use client and server control variates to correct local updates before averaging.
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

# SCAFFOLD

## Intuition

Local gradients need not point in the same direction across clients. SCAFFOLD uses control variates to correct this client drift before averaging model changes. It changes local updates **and** carries additional state; it is not just a new weighted mean. [Karimireddy et al., Section 4 and Algorithm 1](https://proceedings.mlr.press/v119/karimireddy20a/karimireddy20a.pdf#page=4).

## Update rule

Use the paper's **uniform-client objective**, $F(w)=N^{-1}\sum_{i=1}^N F_i(w)$, not the sample-weighted objective used in our FedAvg example. The server maintains $c$; client $i$ maintains $c_i$. Starting from $y_i=w_t$, local steps use:

$$
y_i\leftarrow y_i-\eta_l\left(g_i(y_i)-c_i+c\right).
$$

Here $g_i$ is a stochastic local gradient. After $L$ local steps, the paper's Option II control update is:

$$
c_i^{+}=c_i-c+\frac{w_t-y_i}{L\eta_l}.
$$

For selected cohort $S_t$, update the server model and control:

$$
w_{t+1}=w_t+\frac{\eta_g}{|S_t|}\sum_{i\in S_t}(y_i-w_t),\qquad
c^{+}=c+\frac{1}{N}\sum_{i\in S_t}(c_i^{+}-c_i).
$$

The control denominator is **all $N$ clients**, not only the participating cohort. Nonparticipants keep their $c_i$. Initialize controls to zero in a fresh run. Algorithm 1 also supplies Option I, which recomputes the local full gradient; it is not the same computation budget.

```text
send w and c to selected clients
client i starts y = w and repeats L corrected gradient steps
client i computes its new control and returns changes in y and c_i
server averages model changes over selected clients
server adds sum(control_changes) / total_number_of_clients to c
```

## Worked example

This is a deliberately invented **later-round state**, not zero initialization. Two equally weighted clients have $w_t=1$, controls $c_A=0.2$, $c_B=0.8$, hence $c=0.5$. At this point let their exact gradients be −2 and −8. With one local step and $\eta_l=0.1$:

- A's corrected gradient is $-2-0.2+0.5=-1.7$, giving $y_A=1.17$.
- B's corrected gradient is $-8-0.8+0.5=-8.3$, giving $y_B=1.83$.
- With both participating and $\eta_g=1$, the model becomes $(1.17+1.83)/2=1.5$.
- Option II gives $c_A^{+}=0.2-0.5+(1-1.17)/0.1=-2$ and $c_B^{+}=-8$.
- The server control becomes $0.5+[(-2-0.2)+(-8-0.8)]/2=-5$.

The resulting control is the mean of the updated client controls. Uniform clients were chosen to match this protocol; applying sample-count weights would require a separately defined variant. A one-step example demonstrates bookkeeping, not drift reduction over many rounds.

## Assumptions and limits

Controls require additional storage and communication. A changing client population complicates retained state. Smoothness, stochastic-gradient assumptions, sampling, and objective weighting matter to the analysis. SCAFFOLD does not hide updates or validate that clients computed their controls honestly.

## Self-check

<details><summary>What is corrected locally?</summary><p>The update direction: local gradient minus client control plus server control.</p></details>

<details><summary>Why is the server control update divided by N?</summary><p>It maintains an average over the whole client population while only participating clients replace their controls.</p></details>

<details><summary>Can sample-weighted FedAvg coefficients be inserted without explanation?</summary><p>No. This presentation follows the original uniform-client objective and its coupled model/control updates.</p></details>

## Sources

**P007.** Karimireddy et al. [SCAFFOLD: Stochastic Controlled Averaging for Federated Learning](https://proceedings.mlr.press/v119/karimireddy20a.html), ICML 2020, PMLR 119:5132–5143. Section 4 and **Algorithm 1** specify the algorithm and its two control-update options; later theorems state their assumptions. Local copy: `ref-papers/karimireddy-2020-scaffold.pdf`. [Paper bank](../../papers.md).
