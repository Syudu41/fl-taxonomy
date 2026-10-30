# Website status and architecture

Updated: **2026-10-30**. Session handoff; inspect `git status`, recent commits, and the latest Pages deployment before continuing.

## Purpose and agreed scope

Sudarshan Balaji’s first-year PhD source bank for a comprehensive survey of FL, secure FL, and applications. The presentation is a live website demonstration. Research and thorough understanding take priority; drafted text is not proof of understanding.

- Current prototype: rotating taxonomy cylinder, introductory learning guide, 11 sourced aggregation/optimization notes, sourced FL introduction with a captioned Manim video, and a 12-record searchable paper bank.
- The eight concept notes outside aggregation remain placeholders. No secure-FL proposal has been selected; it should emerge from studying original research.
- **No comparison module now.** It is recorded as pending in `website/docs/about.md`.
- A dataset-based training simulator, reproductions, and paper comparisons remain future work. The learning-rate slider is only an arithmetic illustration.
- User prefers concise communication, Arial/system typography, a light background, and polished visuals. Do not restore the green theme, black backdrop, obsolete vertical concept lists, or “5 visible · 6 concepts” label.

## Repository and deployment

| Item | Location |
| --- | --- |
| Repository | https://github.com/Syudu41/flsurvey |
| Live site | https://syudu41.github.io/flsurvey/ |
| Branch | `main` |
| Configuration | `website/mkdocs.yml` |
| Generated output | `website/site/`, ignored by Git |
| Deployment | `.github/workflows/pages.yml` |

Pushes affecting `website/**` or the workflow build and deploy Pages; manual dispatch is also available. Actions installs Python 3.12 and requirements, runs a strict MkDocs build, and publishes the generated output. Committing alone does not publish. Root-only documentation changes do not trigger deployment.

The root `index.html` redirects to `website/site/index.html` for local use after building. Pages serves the build directly. This project site coexists with the owner’s personal GitHub Pages site.

## Current experience

The Home-page taxonomy cylinder at [Northstar-RF](https://northstar-rf.pages.dev/) is the **confirmed reference**, not its `#/lab` waveform page. Both old cylinders have been replaced with an independently implemented SVG barrel using curved segments and horizontal rotation.

1. The homepage introduces the survey and offers dimension tabs above the barrel.
2. Columns represent concepts, grouped by dimension. Five rows represent written-note coverage: explanation, mathematics, worked example, sources, and self-check.
3. Dragging, horizontal trackpad swipes, and Shift+wheel rotate from anywhere over the diagram in both views. Ordinary vertical scrolling and pinch zoom are preserved. Arrows and selectors choose concepts. Up/down keys choose reading sections; Enter inspects. The side inspector supplies the note link and Explore all.
4. Clicking a cell or Expand opens a native dialog containing a larger barrel. Selecting a cell there opens its note. Section links use explicit anchors when supplied. Escape closes the dialog and restores focus.
5. Filled cells mean a note section is written; dashed cells mean planned. This is **not a comparison, evidence score, or certification of understanding**.
6. Header links lead to the learning guide, paper bank, and About/FL introduction. Dimension pages retain automatically generated concept listings.

| Dimension | Concepts |
| --- | --- |
| Aggregation | FedAvg, FedSGD, FedAvgM, FedProx, SCAFFOLD, FedOpt (FedAdagrad/FedAdam/FedYogi), Robust aggregation, Coordinate-wise median, Trimmed mean, Krum, Geometric median/RFA |
| Data distribution | IID & non-IID, Sample imbalance |
| Participation | Client selection, Availability |
| Privacy | Differential privacy, Secure aggregation |
| Security | Poisoning, Threat models |

All 11 aggregation notes have explanation, mathematics, worked examples, sources, and self-checks written. The eight other concept pages remain placeholders. Written coverage does not mean personal understanding or experimental reproduction.

## Research content

- `foundations.md`: model → loss → gradient → local training → FL, with a hand-computable regression example, adjustable learning rate, sources, and self-checks. Sources include Goodfellow et al., Chapters 5 and 8.
- `fedavg.md`: sample-weighted objective and its derivation, local updates, full-participation averaging, explicit normalized-cohort convention, pseudocode, assumptions, original-paper reading route, and self-checks. An explicitly invented two-client example performs two local steps: parameters 1.36 and 1.96, aggregated to 1.81. It is not a reproduced experiment.
- Other aggregation notes explain FedSGD, server momentum, proximal objectives, SCAFFOLD controls, adaptive server state, and robust operators. Each contains original arithmetic, pseudocode, assumptions, and primary-source pointers. SCAFFOLD uses its original uniform-client objective. FedOpt explains the printed algorithm's reuse of the momentum-filtered displacement in its accumulator; this differs from some library conventions.
- `about.md`: FL introduction, privacy caveat, a six-stage FedAvg life cycle with a Manim video with Computer Modern typography and chapter navigation, prototype scope, visual reference, and pending design/research tasks.
- `papers.md` plus `data/papers.yml`: 12 collected papers, searchable by metadata, filterable by type, with publication/version labels, source/PDF links, reading prompts, and BibTeX. “Collected” does not mean read or understood.
- Eleven PDFs are in repository-root `ref-papers/`. The Mahmud survey has a recorded source but a previously failed HTTP 403 download. PDFs are not automatically republished by the website.
- Surveys include Kairouz (2021), Mahmud (2026 issue), Zhao (2025 author manuscript), and Jimenez-Gutierrez (2025 preprint). Version labels refer to stored records; do not claim the collection is exhaustive or always current.

Suggested live route: homepage → learning guide → FL workflow video → FedAvg worked round → paper bank → return to the map. Teach the foundations interactively before assuming the user can explain the algorithm.

## Architecture

**MkDocs 1.6.1 + custom Jinja theme + vanilla JavaScript/CSS + SVG + Arithmatex/MathJax.** Static hosting; no backend, database, React, Three.js, or runtime Markdown fetch.

```text
Markdown + optional front matter + papers.yml
                     ↓
hooks.py: discover concepts, infer coverage, load records
                     ↓
MkDocs + theme/main.html → static HTML and local assets
                     ↓
GitHub Pages → SVG cylinder, reading notes, paper filters
```

| File | Responsibility |
| --- | --- |
| `website/docs/index.md` | Homepage copy and registered dimension H2s, IDs, descriptions, listing links |
| `website/docs/dimensions/<slug>/index.md` | Dimension introduction; listing appended during build |
| Other Markdown below each dimension | Automatically discovered concept notes, including nested READMEs |
| `website/hooks.py` | Discovery, metadata defaults, coverage inference, README aliases, listings, paper records |
| `website/theme/main.html` | Shared shell, home/dialog, reading layouts, paper cards, local math loading |
| `website/docs/assets/atlas.js` | SVG projection, rotation, dragging, selectors, tabs, expanded view |
| `website/docs/assets/site.js` | Learning-rate arithmetic, paper filtering, citation copying, video chapter seeking |
| `website/visuals/` | Editable Manim scene, isolated environment, render/package wrapper |
| `website/docs/assets/manim-outputs/` | Final MP4, poster, captions, transcript, and media metadata |
| `.agents/skills/minim-agent/SKILL.md` | Reusable project-local visual-production skill |
| `website/docs/assets/atlas.css` | Light responsive theme, barrel, reading content, mobile layouts |
| `website/docs/assets/math-config.js` | MathJax delimiter configuration |
| `website/docs/assets/vendor/mathjax/` | Pinned MathJax 3.2.2 bundle, Apache license, origin note |
| `website/data/papers.yml` | Static paper-bank records |
| `website/requirements.txt` | MkDocs and pymdown-extensions pins |
| `website/assets/workflow.svg` | Workflow image used by root README |
| `website/preview-desktop.png` | Saved visual preview, not a runtime dependency |

### Data flow and controls

`on_config` scans dimensions with root `index.md` files and recursively discovers other Markdown. Entries include title, summary, ordering, coverage, and optional section anchors in `config.extra.dimension_concepts`. Paper records are loaded into `config.extra.papers`; local-copy existence is checked against `ref-papers/`.

`on_files` creates `readme-note.md` aliases so READMEs can coexist with index pages. `on_page_markdown` adds concept layouts/breadcrumbs and generated dimension listings. The homepage embeds navigation metadata in hidden DOM elements; JavaScript constructs the cylinder from these, without a second hardcoded concept catalog.

SVG coordinates use sine/cosine projection; animation uses requestAnimationFrame. A second barrel instance supplies the expanded dialog. Native dropdowns provide an alternative to direct SVG interaction. Reduced motion, focus restoration, resizing, and mobile internal scrolling are supported. URLs use `.html` and MkDocs URL filtering for the `/flsurvey/` project prefix.

Math uses `$...$` or separate `$$` blocks. Arithmatex preserves notation; **locally vendored MathJax** renders SVG, including without an internet connection. This is browser math typesetting, not a LaTeX document compiler.

### Manim production

`minim-agent` is a project-local skill for FL/neural-network explanations; invoke it by name and provide the concept, source, and learner prerequisites. Manim Community 0.19.0 rendering is separate from MkDocs. The tested isolated environment is specified in `website/visuals/environment.yml`; see its README for commands. The scene requires a complete LaTeX installation and dvisvgm. All text is Computer Modern Roman; see the visuals README for the tested TinyTeX setup.

Run `python website/visuals/render.py` inside that environment to produce 1920×1080, 60fps, silent H.264/yuv420p MP4 with faststart, poster, WebVTT, transcript, and metadata. Preview mode writes to a temporary directory. Inspect motion sequences and representative frames, verify arithmetic, and synchronize About-page chapter offsets with the generated JSON before publishing. The About page uses native video controls without autoplay and optional captions because the MP4 already has visible captions. Stage buttons seek without forcing playback.

The film independently illustrates the FedAvg note's exact 1 → (1.36, 1.96) → 1.81 calculation, including rebroadcast. It is original educational composition, not a claim of matching another creator's production quality.

## Editing workflow

Detailed examples: [website/README.md](website/README.md).

- Add/update concepts under `website/docs/dimensions/<slug>/`. Listings and cylinder data update on rebuild. Optional `title`, `description`, `order`, `draft`, `coverage`, and `section_anchors` front matter customize discovery. `draft` omits navigation; it is not access control.
- Coverage inference checks for equations, example headings, source links, and self-check headings. Placeholder text marks sections planned. Explicit metadata overrides inference. Review inferred labels; this is a simple text heuristic.
- Add a dimension by creating its folder/index and registering an H2 with matching ID and Explore all link in homepage Markdown. New dimensions are not registered automatically. Common styling and controls then apply.
- Add papers in `website/data/papers.yml`; store reading PDFs under root `ref-papers/` and maintain its reference index. There is no web editor or download automation.

One-time setup from root:

```sh
python3 -m venv website/.venv
website/.venv/bin/pip install -r website/requirements.txt
```

Preview or validate:

```sh
source website/.venv/bin/activate
cd website
mkdocs serve
# Release check: mkdocs build --strict
```

Push intended website changes to `main`, then verify GitHub Actions. Do not edit generated output or depend on temporary QA environments surviving a session.

## Validation and limitations

The 2026-10-30 update passed strict builds and ad hoc Chrome checks for barrel rotation, tabs, expansion, section navigation, mathematical rendering without errors, offline math, exact slider arithmetic, paper filters/citations, and mobile overflow on four principal routes. Screenshots were inspected. Temporary integration checks verified new-concept discovery, nested README aliases, and a registered new dimension; local links and anchors passed across the generated HTML pages. There is no committed browser test suite. The current release additionally checks wheel/trackpad interception, preserved vertical scrolling/zoom, all 11 method pages and math, exact arithmetic recomputed independently, paper filters, and embedded video metadata/captions/chapter seeking. All seven tested mobile routes fit the viewport; the final link/asset/anchor audit passed across 29 generated HTML pages. The skill passed its validator; the video passed complete FFmpeg decoding and multi-frame visual inspection.

Metadata inference is intentionally simple. The website renders trusted repository content; no upload/editor API is present. Source attribution is editorial, not an automated claim-verification system. Many research topics are unfinished, and no training, convergence reproduction, security guarantee, or personal learning outcome is established by the prototype.

## Continue in a future session

Read this file and the latest user instructions; inspect working-tree changes and deployment status. Preserve concise communication and the confirmed Home-page reference. Distinguish visual implementation, content drafting, and the user’s actual understanding. Validate relevant changes, inspect screenshots for visual work, and refresh this handoff after material changes.
