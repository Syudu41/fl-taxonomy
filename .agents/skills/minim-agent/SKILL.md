---
name: minim-agent
description: Create and render Manim explanations of federated learning workflows, neural networks, and mathematical concepts for this survey, delivering inspected video or still-image artifacts and reproducible source.
---

# Minim agent

Use Manim Community to turn a precise mathematical explanation into an original visual. Start from the research note, its primary sources, and the intended learner's prerequisites. Distinguish the published algorithm, simplifying assumptions, and invented examples. Work through numerical values independently before animating them.

In this repository:

- Scene source and isolated render dependencies live in `website/visuals/`.
- Final site artifacts belong in `website/docs/assets/manim-outputs/`.
- Read `website/visuals/README.md` for the tested environment, rendering, and extraction commands. `fedavg_lifecycle.py` and `render.py` are working examples, not mandatory templates for every subject.

Use a storyboard with a clear learning question, purposeful motion, consistent visual identities, and enough reading time. Prefer small, exact examples over dense text. For neural networks, distinguish architecture, forward computation, loss, and parameter updates; do not imply that a moving dot is a literal implementation of learning. For FL, preserve ownership of data, update direction, synchronization, and weighting conventions.

Aim for precise mathematical exposition and polished composition. Do not copy another creator's branding or claim parity with their production quality. Use genuine LaTeX Computer Modern Roman for all video typography, as requested by the user. Use Tex/MathTex with a custom Computer Modern template; do not substitute Pango, Unicode approximations, or Latin Modern. Install the required TeX dependencies when missing. Keep labels inside safe margins and verify legibility at the embedded player size.

Render a low-resolution preview first when composition is uncertain, then render the final artifact. Render final videos at 60 fps, with purposeful continuous motion, smooth easing, and deliberate reading pauses. Frame rate alone does not establish smoothness. For website videos use browser-compatible H.264/yuv420p with faststart, a poster, captions/transcript, and native playback controls. Do not autoplay. Preserve editable source and separate rendering dependencies from MkDocs requirements.

Inspect multiple frames covering transitions and mathematical steps, not just the poster. Check dimensions, codec, duration, timing, arithmetic, text overlap, and clipping. Correct defects before embedding the result. A successful renderer exit does not establish visual quality. When blocked by dependencies, report the actual blocker instead of presenting placeholder media as completed output.

Use existing publishing authorization only; generating an animation does not itself authorize unrelated external publication or messages.
