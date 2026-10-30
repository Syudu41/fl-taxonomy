# Manim visuals

Editable source for the website's original teaching animations. Rendering is separate from the MkDocs build; Pages serves the finished media without running Manim.

## Render

A tested setup uses Python 3.12, Manim Community 0.19.0, Cairo/Pango, and FFmpeg. With micromamba or conda:

```sh
micromamba create -y -p /tmp/fl-manim -f website/visuals/environment.yml
micromamba run -p /tmp/fl-manim python website/visuals/render.py --preview
micromamba run -p /tmp/fl-manim python website/visuals/render.py
```

Alternatively, install the native Cairo/Pango/FFmpeg dependencies following the [Manim installation documentation](https://docs.manim.community/en/stable/installation.html), then install `requirements.txt` in a dedicated virtual environment. The scene uses DejaVu Sans/Mono text and Pango markup for proper mathematical subscripts, so this example does not require a LaTeX installation.

The render wrapper writes MP4, poster PNG, WebVTT, transcript, and media metadata under `website/docs/assets/manim-outputs/`. Preview output goes to a temporary directory. Production output is 1920×1080, 30fps, silent, H.264/yuv420p with faststart. Captions are also visible within the video. Native player controls let the reader pause and replay.

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
