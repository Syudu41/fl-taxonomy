# Manim visuals

Editable source for the website's original teaching animations. Rendering is separate from the MkDocs build; Pages serves the finished media without running Manim.

## Render

A tested setup uses Python 3.12, Manim Community 0.19.0, Cairo/Pango, and FFmpeg. With micromamba or conda:

```sh
micromamba create -y -p /tmp/fl-manim -f website/visuals/environment.yml
export PATH="/path/to/texlive/bin/x86_64-linux:/tmp/fl-manim/bin:$PATH"
python website/visuals/render.py --preview
python website/visuals/render.py
```

Alternatively, install the native Cairo/Pango/FFmpeg dependencies following the [Manim installation documentation](https://docs.manim.community/en/stable/installation.html), then install `requirements.txt` in a dedicated virtual environment. A complete TeX installation is required: `latex`, `dvisvgm`, `standalone`, `preview`, `amsmath`, and `amsfonts`. Tested with official TinyTeX-1 (TeX Live 2026), plus `tlmgr update --self` and `tlmgr install standalone preview dvisvgm`. Put its binary directory first on PATH. The conda `texlive-core` package alone is insufficient. All labels use `Tex` and all mathematics use `MathTex`; the custom template selects Computer Modern Roman without loading Latin Modern. Do not replace this with Pango or a similar-looking system font.

The render wrapper writes MP4, poster PNG, WebVTT, transcript, and media metadata under `website/docs/assets/manim-outputs/`. Preview output goes to a temporary directory. Production output is 1920×1080, 60fps, silent, H.264/yuv420p with faststart. Captions are also visible within the video. Native player controls let the reader pause and replay.

Inspect frames after rendering, for example:

```sh
ffmpeg -ss 24 -i website/docs/assets/manim-outputs/fedavg-lifecycle.mp4 -frames:v 1 /tmp/fedavg-frame.png
ffprobe -v error -show_streams -show_format website/docs/assets/manim-outputs/fedavg-lifecycle.mp4
```

## Example and sources

`fedavg_lifecycle.py` illustrates one full-participation FedAvg round, based on [McMahan et al., Section 2 and Algorithm 1](https://proceedings.mlr.press/v54/mcmahan17a.html). The numbers are an invented arithmetic example, consistent with the FedAvg note:

- A has one example (1,2); B has three copies of (2,4).
- Model ŷ=wx; squared-error mean loss; shared w=1; learning rate0.1; two full-batch local steps.
- A returns1.36; B returns1.96; sample weights1/4 and3/4 produce1.81.

The example assumes honest, synchronous clients and does not establish privacy or reproduce a published experiment. Original visual composition and animation; no external artwork, voice, or music.

## Motion and review

Preview at 720p/30fps; final output is 1080p/60fps. Quintic easing gives moving objects zero velocity and acceleration at both endpoints. Client colors persist through broadcast, local loss curves, return, weighted averaging, and rebroadcast. Moving loss-curve points interpolate between discrete gradient-step endpoints; they do not represent extra training steps. The number-line merge illustrates the weighted mean, not the server implementation.

Inspect transition sequences as well as still frames. Verify text at embedded-player size, stable decimal alignment, chapter offsets, captions and the final arithmetic. `fedavg-lifecycle.json` records chapter timestamps and an explicit poster timestamp. Keep the chapter buttons in `docs/about.md` synchronized after changing the storyboard.

Visual study: the official [3Blue1Brown gradient-descent lesson](https://www.3blue1brown.com/lessons/gradient-descent/) informed the use of persistent mathematical objects, purposeful point movement and spare composition. This is an original animation, not a reproduction or a claim of equivalent production quality.
