---
layout: about
---

# What is federated learning?

Federated learning (FL) lets multiple participants train a model collaboratively while keeping their training data distributed. Participants can be devices or organizations; a common architecture uses a coordinating server. [Kairouz et al., introduction and abstract](https://arxiv.org/abs/1912.04977).

## Who participates?

A **client** holds local data and performs computation. A **server** coordinates training and combines contributions in the centralized setting. The **model** contains the learned parameters used for prediction.

For example, several hospitals could collaborate on a prediction task while retaining their patient records locally. This is an illustration of the setting, not a claim about a deployed system.

## What happens in a round?

1. The server distributes the current model to selected clients.
2. Clients train locally.
3. Clients send model contributions back.
4. The server combines them to update the shared model.

This is the basic server-coordinated workflow used in the [original FedAvg paper, Section 2 and Algorithm 1](https://proceedings.mlr.press/v54/mcmahan17a.html). Other FL designs can use different coordination and learning objectives.

## Watch one FedAvg life cycle

This original Manim animation follows one complete round: choose the participants, send the shared model, train locally, return parameters, average, and start the next round. It uses the [FedAvg note's worked example](dimensions/aggregation/fedavg.md#one-complete-round): two honest clients, full participation, two full-batch local steps, and sample-count weights. The numbers are teaching arithmetic, not a reproduced experiment. Algorithm source: [McMahan et al., Section 2 and Algorithm 1](https://proceedings.mlr.press/v54/mcmahan17a.html).

<figure class="workflow-film">
  <video id="fedavg-film" controls playsinline preload="metadata" poster="assets/manim-outputs/fedavg-lifecycle-poster.png?v=cmr60" aria-label="FedAvg life cycle: a silent, captioned mathematical animation" aria-describedby="film-description">
    <source src="assets/manim-outputs/fedavg-lifecycle.mp4?v=cmr60" type="video/mp4">
    <track kind="captions" src="assets/manim-outputs/fedavg-lifecycle.vtt?v=cmr60" srclang="en" label="English">
    Your browser does not support embedded video. Open the MP4 using the download link below.
  </video>
  <figcaption id="film-description">Original Manim animation · 1080p / 60 fps · Computer Modern · approximately 74 seconds · silent with visible captions. Pause, replay, or jump to a stage below.</figcaption>
  <nav class="film-chapters" aria-label="Video chapters">
    <button type="button" data-video-seek="0">01 · Participants</button>
    <button type="button" data-video-seek="4.95">02 · Broadcast</button>
    <button type="button" data-video-seek="12.45">03 · Local training</button>
    <button type="button" data-video-seek="33.1">04 · Return models</button>
    <button type="button" data-video-seek="41.55">05 · Weighted mean</button>
    <button type="button" data-video-seek="60.15">06 · Next round</button>
  </nav>
</figure>

[Read the text transcript](assets/manim-outputs/fedavg-lifecycle-transcript.md) · [Open or download the video](assets/manim-outputs/fedavg-lifecycle.mp4)

### The round, step by step

<ol class="workflow-steps">
  <li><strong>Choose the participants.</strong><p>Our full-participation example selects A and B. A holds one example; B holds three. This is an explicit choice, not a requirement that every FL deployment includes everyone.</p></li>
  <li><strong>Broadcast the same model.</strong><p>The server sends parameter w = 1 to both clients. Neither client starts from the other client's locally updated model.</p></li>
  <li><strong>Train locally.</strong><p>Using learning rate 0.1 and two full-batch steps, A goes 1 → 1.20 → 1.36; B goes 1 → 1.80 → 1.96. Their raw training examples remain local.</p></li>
  <li><strong>Return the contributions.</strong><p>The clients send their trained parameters back. Sending compatible model differences could implement the same update with the declared sign convention.</p></li>
  <li><strong>Aggregate.</strong><p>The sample-count weights are 1/4 and 3/4. The new global parameter is (1/4)(1.36) + (3/4)(1.96) = 1.81. A larger sample count is not a higher trust score.</p></li>
  <li><strong>Evaluate and continue.</strong><p>A real experiment records a defined evaluation metric and stopping rule. If training continues, the next round broadcasts 1.81. This animation computes one round; it does not measure accuracy or show convergence.</p></li>
</ol>

The server coordinates the round and receives model contributions, rather than the raw examples. That distinction is central to FL, but it does not make the updates confidential by itself.

## Does FL guarantee privacy?

No. Keeping raw data local changes what is shared, but updates may still reveal sensitive information. Privacy guarantees and resistance to malicious participants require explicit mechanisms and assumptions. [McMahan et al., Section 1, Privacy](https://proceedings.mlr.press/v54/mcmahan17a/mcmahan17a.pdf#page=2).

## Where should I start?

Begin with [model, loss, gradient, and local training](foundations.md), then read [FedAvg](dimensions/aggregation/fedavg.md) for our first equation and worked example, or return to the [dimension cylinder](index.md). This website is a developing survey: introductory notes are being added while many concept pages remain placeholders.


## What this website is building

The survey connects a learning route, a visual map of the notes, and a [paper bank](papers.md), and reusable Manim illustrations. Written notes and collected papers do not establish personal understanding or reproduced results. The aggregation dimension now has sourced method notes and worked examples; the other dimensions are a developing reading plan.

## Design and research pending

- A structured paper-comparison module is **pending**, not part of this prototype.
- A secure-FL research question or proposal has not been selected. It should follow the survey and analysis of original studies.
- Statistical heterogeneity, partial participation, and explicit threat models need deeper notes.
- A dataset-based FL simulator and reproduction experiments are future work. The learning-rate widget is only an arithmetic illustration.


## Visual reference

The rotating, segmented cylinder interaction is inspired by the [Northstar-RF taxonomy on its Home page](https://northstar-rf.pages.dev/). This website uses an independent SVG implementation and FL note metadata. Its cells indicate whether sections of our notes have been written; they are not evidence grades, method rankings, or a completed comparison.
