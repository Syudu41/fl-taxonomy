# Federated Learning survey website

Static MkDocs source bank for a comprehensive FL survey. The prototype has a rotating SVG taxonomy cylinder, introductory learning guide, 11 sourced aggregation/optimization notes, a 12-record paper bank, and a captioned FedAvg workflow video. Other dimensions still contain planned notes.

## Preview and build

From the repository root:

```sh
python3 -m venv website/.venv
website/.venv/bin/pip install -r website/requirements.txt
website/.venv/bin/mkdocs serve -f website/mkdocs.yml
```

Open the printed URL, normally http://127.0.0.1:8000. `serve` rebuilds automatically. For a release check:

```sh
website/.venv/bin/mkdocs build --strict -f website/mkdocs.yml
```

## Add or update concepts

Create Markdown under `docs/dimensions/<dimension>/`, including nested files or `README.md`:

```markdown
# My concept

A brief description for the listing.

## Explanation

Write the explanation and cite its sources.
```

The next build adds it to the cylinder and generated dimension listing. Optional front matter supports `title`, `description`, numeric `order`, and `draft: true` to omit it from navigation. Titles otherwise come from the H1; descriptions from the first ordinary paragraph. READMEs publish as `readme-note.html` to avoid index collisions.

The five cylinder rows describe **note coverage**: explanation, mathematics, worked example, sources, and self-check. Coverage is inferred from Markdown, with all sections marked planned for placeholder notes. Override it and provide exact section destinations when needed:

```yaml
---
coverage:
  overview: true
  math: true
  example: false
  sources: true
  check: false
section_anchors:
  overview: explanation
  math: objective
  sources: references
---
```

Coverage indicates written sections, not research quality or personal understanding. Without an explicit anchor, the link opens the note at its beginning.

## Add a dimension

Create `docs/dimensions/<slug>/index.md` and its concept documents. Register it in `docs/index.md` with an H2 whose ID matches the folder:

```markdown
## Communication {#communication}

How communication affects FL.

[Explore all](dimensions/communication/index.md)
```

It inherits the cylinder controls. Concept lists inside dimension indexes are generated; do not maintain duplicate links.

## Add papers

Add a record to `data/papers.yml`, using an existing record as the schema. Include a stable ID, title, authors, publication/version status, source/PDF URLs, topics, reading prompt, collection date, and BibTeX. Optional `local_file` is a filename relative to repository-root `ref-papers/`; the build checks whether that copy exists. Optional `note` links to a Markdown note.

The paper bank provides search, type filtering, citations, and source links. “Collected” does not mean read or understood. PDFs stay in the repository library and are not automatically republished. Record unavailable downloads honestly.

## Mathematics and interactions

Use `$w_t$` inline or a separate `$$` equation block. Arithmatex preserves the notation; locally vendored MathJax 3.2.2 renders SVG equations, including offline. Its license and origin are in `docs/assets/vendor/mathjax/`.

`hooks.py` discovers content and loads paper records. `theme/main.html` renders the shared shell. `docs/assets/atlas.js` projects an original SVG barrel with horizontal trackpad/Shift-wheel/drag/arrow rotation, selectors, and an expanded dialog. Ordinary vertical scrolling and pinch zoom remain native. `site.js` handles the learning-rate illustration, paper filtering, and video chapter navigation. `atlas.css` supplies the responsive light theme and Arial typography.

Visual reference: [Northstar-RF Home taxonomy](https://northstar-rf.pages.dev/). The implementation is independent; cells show note coverage rather than method ratings. Reduced motion and keyboard/dropdown navigation are supported.

## Manim illustrations

The project-local [minim-agent skill](../.agents/skills/minim-agent/SKILL.md) creates original mathematical workflow and neural-network visuals. Editable scene source and isolated rendering dependencies are in `visuals/`; the [rendering guide](visuals/README.md) contains the tested command.

Final artifacts go in `docs/assets/manim-outputs/`: MP4, poster, WebVTT, transcript, and metadata. The FL introduction embeds the 1080p/60fps silent FedAvg video with LaTeX Computer Modern typography with native controls and chapter buttons. Captions are baked into the video; the optional caption track is not enabled by default to avoid duplicates. Re-render before building when scene source changes. GitHub Pages serves the final assets and does not install or run Manim.

The workflow illustrates one honest, synchronous, full-participation round. It is a teaching example, not an experiment or privacy guarantee. Frame inspection, arithmetic checks, and browser playback validation accompany production rendering.

## Publish

Live: https://syudu41.github.io/fl-taxonomy/

Push website changes to `main`; `.github/workflows/pages.yml` builds and deploys GitHub Pages. Committing alone does not publish. Check the Actions result before assuming a release is live.

Generated `website/site/` is ignored by Git. The root `index.html` redirects to that build for local use; Pages serves the build directly. Architecture, current scope, and pending work are recorded in [website-status.md](../website-status.md).
