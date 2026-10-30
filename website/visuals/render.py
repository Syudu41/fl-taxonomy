#!/usr/bin/env python3
"""Render, package and inspect the FedAvg scene without polluting site sources."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
OUTPUT=ROOT/'website/docs/assets/manim-outputs'


def timestamp(seconds):
    millis=round(seconds*1000)
    hours,millis=divmod(millis,3_600_000)
    minutes,millis=divmod(millis,60_000)
    secs,millis=divmod(millis,1000)
    return f'{hours:02}:{minutes:02}:{secs:02}.{millis:03}'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview',action='store_true',help='Render 720p/30fps into /tmp instead of publishing assets.')
    args=parser.parse_args()
    output=Path(tempfile.mkdtemp(prefix='minim-preview-')) if args.preview else OUTPUT
    output.mkdir(parents=True,exist_ok=True)
    ffmpeg=shutil.which('ffmpeg');ffprobe=shutil.which('ffprobe')
    if not ffmpeg or not ffprobe:raise SystemExit('FFmpeg and ffprobe must be on PATH. See website/visuals/README.md.')
    if not shutil.which('latex') or not shutil.which('dvisvgm'):
        raise SystemExit('A complete LaTeX installation and dvisvgm are required for Computer Modern. See website/visuals/README.md.')
    with tempfile.TemporaryDirectory(prefix='minim-render-') as work:
        work=Path(work)
        timeline=work/'timeline.json'
        env=os.environ.copy();env['MINIM_TIMELINE_PATH']=str(timeline)
        subprocess.run([sys.executable,'-m','manim','--renderer','cairo','--disable_caching',
                        '-r','1280,720' if args.preview else '1920,1080','--fps','30' if args.preview else '60',
                        '--media_dir',str(work/'media'),'-o','fedavg-lifecycle.mp4',
                        str(Path(__file__).with_name('fedavg_lifecycle.py')),'FedAvgLifecycle'],check=True,env=env)
        rendered=next((work/'media/videos').rglob('fedavg-lifecycle.mp4'))
        final=output/'fedavg-lifecycle.mp4'
        subprocess.run([ffmpeg,'-y','-i',str(rendered),'-an','-c:v','libx264','-crf','20','-preset','medium',
                        '-pix_fmt','yuv420p','-movflags','+faststart',str(final)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        info=json.loads(subprocess.check_output([ffprobe,'-v','error','-show_streams','-show_format','-of','json',str(final)]))
        stream=info['streams'][0]
        assert stream['codec_name']=='h264' and stream['pix_fmt']=='yuv420p'
        data=json.loads(timeline.read_text())
        vtt=['WEBVTT','']
        transcript=['# FedAvg: one complete round','',
                    'Silent, captioned original teaching animation. Full participation; honest synchronous clients. Numerical data are invented.',
                    '', 'Motion between local-step endpoints is visual interpolation, not additional optimization steps. The merging dots illustrate the weighted mean geometrically.', '', 'Algorithm source: [McMahan et al., Section 2 and Algorithm 1](https://proceedings.mlr.press/v54/mcmahan17a.html).', '']
        for i,cue in enumerate(data['cues'],1):
            vtt.extend([str(i),f"{timestamp(cue['start'])} --> {timestamp(cue['end'])}",cue['text'],''])
            transcript.extend([f"**{timestamp(cue['start'])}** — {cue['text']}",''])
        (output/'fedavg-lifecycle.vtt').write_text('\n'.join(vtt))
        (output/'fedavg-lifecycle-transcript.md').write_text('\n'.join(transcript))
        poster_time=data['poster_time']
        subprocess.run([ffmpeg,'-y','-ss',str(poster_time),'-i',str(final),'-frames:v','1',str(output/'fedavg-lifecycle-poster.png')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        (output/'fedavg-lifecycle.json').write_text(json.dumps({'renderer':'Manim Community 0.19.0','resolution':[stream['width'],stream['height']],
            'fps':stream['r_frame_rate'],'duration_seconds':float(info['format']['duration']),'has_audio':False, 'typography':'Computer Modern Roman (LaTeX)', 'chapters':data['chapters'], 'poster_time':poster_time,
            'source':'website/visuals/fedavg_lifecycle.py','algorithm_source':'https://proceedings.mlr.press/v54/mcmahan17a.html',
            'example':'Invented full-participation arithmetic, not experimental results','captions':data['cues']},indent=2)+'\n')
        print(f'Artifacts: {output}\nDuration: {info["format"]["duration"]} seconds\nCodec: H.264/yuv420p')

if __name__=='__main__':main()
