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

## Does FL guarantee privacy?

No. Keeping raw data local changes what is shared, but updates may still reveal sensitive information. Privacy guarantees and resistance to malicious participants require explicit mechanisms and assumptions. [McMahan et al., Section 1, Privacy](https://proceedings.mlr.press/v54/mcmahan17a/mcmahan17a.pdf#page=2).

## Where should I start?

Begin with [model, loss, gradient, and local training](foundations.md), then read [FedAvg](dimensions/aggregation/fedavg.md) for our first equation and worked example, or return to the [dimension cylinder](index.md). This website is a developing survey: introductory notes are being added while many concept pages remain placeholders.


## What this website is building

The survey connects a learning route, a visual map of the notes, and a [paper bank](papers.md). Written notes and collected papers do not establish personal understanding or reproduced results. The first complete worked example is FedAvg; the other dimensions are a developing reading plan.

## Design and research pending

- A structured paper-comparison module is **pending**, not part of this prototype.
- A secure-FL research question or proposal has not been selected. It should follow the survey and analysis of original studies.
- Statistical heterogeneity, partial participation, and explicit threat models need deeper notes.
- A dataset-based FL simulator and reproduction experiments are future work. The learning-rate widget is only an arithmetic illustration.


## Visual reference

The rotating, segmented cylinder interaction is inspired by the [Northstar-RF taxonomy on its Home page](https://northstar-rf.pages.dev/). This website uses an independent SVG implementation and FL note metadata. Its cells indicate whether sections of our notes have been written; they are not evidence grades, method rankings, or a completed comparison.
