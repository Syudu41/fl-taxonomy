---
layout: guide
math: true
title: From a model to federated learning
description: A guided route through model, loss, gradient, local training, and aggregation.
---

# From a model to federated learning

Start here if loss functions, gradients, and local training are unfamiliar. Work through one section at a time. The calculations below are our own small teaching example; they are not results from an FL benchmark.

<div class="reading-route"><a href="#1-a-model-makes-a-prediction">Model</a><span>→</span><a href="#2-loss-measures-the-error">Loss</a><span>→</span><a href="#3-a-gradient-gives-a-direction">Gradient</a><span>→</span><a href="#4-training-changes-the-parameter">Training</a><span>→</span><a href="#5-local-training-and-aggregation">Federation</a></div>

## 1. A model makes a prediction

A model is a function with adjustable parameters. In this example it predicts a number from an input:

$$
\hat y = f_w(x) = wx.
$$

Here $x$ is the input, $\hat y$ is the prediction, and $w$ is the adjustable parameter. The hat distinguishes a prediction from the observed target $y$.

Take one training example: $x=2$, $y=4$. Starting with $w=1$ gives $\hat y=2$. We want a rule for changing $w$ so its prediction fits the training example better. A single example cannot tell us whether a model generalizes to unseen data.

<details><summary>Check: if w = 3, what does the model predict for x = 2?</summary><p>The prediction is 3 × 2 = 6. The observed target remains 4; changing the model does not change the data.</p></details>

**Reading anchor:** Goodfellow, Bengio, and Courville, [Deep Learning, Section 5.1.4: Example — Linear Regression](https://www.deeplearningbook.org/contents/ml.html). The one-parameter example here deliberately omits an intercept.

## 2. Loss measures the error

Choose squared error as the loss for one example:

$$
\ell(w;x,y) = (wx-y)^2.
$$

At $w=1$, the prediction is 2 and the loss is $(2-4)^2=4$. At $w=2$, the prediction is 4 and the loss is 0. A loss function supplies a numerical training objective; squared error is a choice for this demonstration, not the loss used for every task.

For $n$ examples, average their losses:

$$
F(w) = \frac{1}{n}\sum_{i=1}^{n}\ell(w;x_i,y_i).
$$

<details><summary>Check: does loss = 0 on this one example establish a good model?</summary><p>No. It establishes an exact fit to this training example. We still need other data and a defined evaluation procedure to assess generalization.</p></details>

**Reading anchor:** [Deep Learning, Sections 5.1.4 and 5.2](https://www.deeplearningbook.org/contents/ml.html), for linear regression and the distinction between training performance and generalization.

## 3. A gradient gives a direction

The derivative tells us how the loss changes locally when $w$ changes. For this one-parameter model:

$$
\frac{\partial\ell}{\partial w} = 2x(wx-y).
$$

At $x=2$, $y=4$, $w=1$, the derivative is $2(2)(2-4)=-8$. Moving a small distance in the direction opposite the derivative reduces this differentiable loss locally. For a vector of parameters, the collection of partial derivatives is the **gradient**, written $\nabla_w\ell$.

A negative derivative does not mean a negative loss. It describes the local slope of the loss curve.

## 4. Training changes the parameter

A gradient descent step is:

$$
w_{\mathrm{new}} = w - \eta\nabla F(w),
$$

where $\eta$ is the learning rate. With $\eta=0.1$ and our derivative of $-8$:

$$
w_{\mathrm{new}}=1-0.1(-8)=1.8.
$$

The new prediction is 3.6 and the loss is 0.16. This calculation is one optimization step, not a complete training procedure.

<section class="learning-widget" data-gradient-demo aria-label="Explore one gradient step">
  <div class="widget-heading"><strong>Try one step</strong><span>One training example · no dataset download</span></div>
  <label for="learning-rate">Learning rate <output id="rate-value" for="learning-rate">0.100</output></label>
  <input id="learning-rate" type="range" min="0" max="0.3" step="0.005" value="0.1">
  <div class="step-readout"><div><span>Starting parameter</span><strong>1.000</strong></div><div><span>New parameter</span><strong id="new-weight">1.800</strong></div><div><span>Loss before</span><strong>4.000</strong></div><div><span>Loss after</span><strong id="new-loss">0.160</strong></div></div>
  <p id="step-explanation" aria-live="polite">The step moves the prediction closer to the observed target.</p>
</section>

**Try:** set the learning rate to 0, then 0.125, then 0.3. At 0 nothing changes; at 0.125 this particular quadratic reaches $w=2$ in one step; at 0.3 it overshoots far enough to increase the loss. Those values depend on this example's loss scaling.

**SGD** estimates the training-loss gradient using a randomly selected example or minibatch rather than the complete local dataset. An **epoch** is a pass through the training dataset; a **minibatch** is a subset used for a step. Step count and epoch count are not interchangeable.

**Reading anchor:** [Deep Learning, Section 8.3.1: Stochastic Gradient Descent](https://www.deeplearningbook.org/contents/optimization.html). The widget uses an exact derivative of the one-example objective, not random minibatch sampling.

<details><summary>Check: are the learning rate and parameter the same thing?</summary><p>No. The parameter is part of the model being fitted. The learning rate is a setting controlling the update size.</p></details>

## 5. Local training and aggregation

In a common server-coordinated FL round, clients receive the same starting model. Each performs training on its own data. The server then combines their returned parameters or updates. Local training answers “how does one client change the model?” Aggregation answers “how do we combine the clients' contributions?” [McMahan et al., Section 2 and Algorithm 1](https://proceedings.mlr.press/v54/mcmahan17a.html).

Keeping data distributed does not by itself establish privacy. Model updates can still reveal information; privacy and security need their own assumptions and mechanisms. See the original paper's Section 1, Privacy.

Continue to [FedAvg: objective, local steps, and one complete round](dimensions/aggregation/fedavg.md), or open the [paper bank](papers.md) to find the original sources.

## Before moving on

Explain these five sentences without relying on the symbols: the model predicts; the loss measures error; the gradient describes local slope; training changes parameters; aggregation combines contributions. Use the checks above to identify what needs another pass. Reading this page is not automatically recorded as understanding it.
