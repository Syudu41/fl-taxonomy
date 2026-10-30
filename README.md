# Federated Learning Survey

A website for a comprehensive FL survey, supporting Sudarshan Balaji’s PhD research in federated learning, secure FL, and applications. Work in progress.

**[Website](https://syudu41.github.io/flsurvey/)** · [Website guide](website/README.md) · [Session handoff](website-status.md) · [Reference papers](ref-papers/README.md)

The prototype includes an interactive concept cylinder, 11 sourced aggregation/optimization notes with worked examples, a learning guide, a 12-paper bank, and a captioned Manim video of one FedAvg round. Other dimensions remain a reading plan. Paper comparisons and a training simulator are pending.

## Content workflow

![Workflow: edit or add Markdown content, preview locally, push to main, and automatically publish the survey.](website/assets/workflow.svg)

- **Update/add a concept:** edit or create Markdown under `website/docs/dimensions/<dimension>/`. Listings and the cylinder update on rebuild.
- **Add a dimension:** create its folder and `index.md`, then register it in `website/docs/index.md`.
- **Add a paper:** add a record to `website/data/papers.yml`; keep reading copies in `ref-papers/`.
- **Create a visual:** use the project-local [minim-agent skill](.agents/skills/minim-agent/SKILL.md); [rendering guide](website/visuals/README.md).

## Preview and publish

After the one-time environment setup in the [website guide](website/README.md):

```sh
source website/.venv/bin/activate
cd website
mkdocs serve
```

`serve` builds automatically. Use `mkdocs build --strict` for a release check. Commit and **push to main** to publish through GitHub Actions.
