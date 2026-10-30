# Federated Learning Survey

A website for a comprehensive FL survey, supporting Sudarshan Balaji’s PhD research in federated learning, secure FL, and applications. Work in progress.

**[Website](https://syudu41.github.io/FL-survey/)** · [Website guide](website/README.md) · [Session handoff](website-status.md) · [Reference papers](ref-papers/README.md)

The prototype includes a rotating concept cylinder, a learning guide, a worked FedAvg example with equations, and a searchable paper bank. Other concept notes remain placeholders. Paper comparisons and a training simulator are pending.

## Content workflow

![Workflow: edit or add Markdown content, preview locally, push to main, and automatically publish the survey.](website/assets/workflow.svg)

- **Update/add a concept:** edit or create Markdown under `website/docs/dimensions/<dimension>/`. Listings and the cylinder update on rebuild.
- **Add a dimension:** create its folder and `index.md`, then register it in `website/docs/index.md`.
- **Add a paper:** add a record to `website/data/papers.yml`; keep reading copies in `ref-papers/`.

## Preview and publish

After the one-time environment setup in the [website guide](website/README.md):

```sh
source website/.venv/bin/activate
cd website
mkdocs serve
```

`serve` builds automatically. Use `mkdocs build --strict` for a release check. Commit and **push to main** to publish through GitHub Actions.
