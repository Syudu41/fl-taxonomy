"""An original, continuous FedAvg explanation. All typography is genuine TeX CM."""
import json
import os
from pathlib import Path
from manim import *

CM = TexTemplate(documentclass=r'\documentclass[preview]{standalone}',
                 preamble=r'\usepackage{amsmath}\usepackage{amssymb}\renewcommand{\rmdefault}{cmr}')
config.tex_template = CM
Tex.set_default(tex_template=CM)
MathTex.set_default(tex_template=CM)
BG, INK, MUTED = '#0B0E15', '#EDF2FA', '#A5AFBF'
A, B, GLOBAL = '#63B5F6', '#FFCB78', '#C5F1DD'

def ease(t):
    return t*t*t*(10+t*(-15+6*t))

def words(s, size=32, color=INK):
    return Tex(s, font_size=size, color=color)

def math(s, size=38, color=INK):
    return MathTex(s, font_size=size, color=color)

class FedAvgLifecycle(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.cues, self.chapters = [], []
        self.heading = words('Federated averaging', 43).move_to(UP*3.35)
        self.caption = None
        self.add(self.heading)
        source = words('FedAvg: McMahan et al. (2017) --- an invented numerical example', 17, MUTED).move_to(DOWN*3.77)
        self.add(source)

        def stage(title, caption):
            self.chapters.append({'title': title, 'start': round(self.time, 3)})
            new = words(title, 43).move_to(self.heading)
            self.play(FadeOut(self.heading, shift=UP*.12), FadeIn(new, shift=UP*.12), run_time=.7)
            self.heading = new
            say(caption)

        def say(s):
            if self.cues: self.cues[-1]['end'] = round(self.time, 3)
            self.cues.append({'start': round(self.time, 3), 'text': s})
            new = words(r'\mbox{'+s+'}', 25, MUTED).move_to(DOWN*3.18)
            if new.width > 12.7: new.scale_to_fit_width(12.7)
            old = [FadeOut(self.caption)] if self.caption is not None else []
            self.play(*old, FadeIn(new), run_time=.45)
            self.caption = new

        # Preserve the same model and client identities throughout the round.
        server = VGroup(Circle(.65, color=GLOBAL, stroke_width=2), math('w_t=1', 30, GLOBAL)).move_to(UP*1.7)
        server_label = words('Server', 27).next_to(server, UP, .15)
        nodes, labels, samples = [], [], []
        for x, col, name, n in [(-3.6,A,'A',1),(3.6,B,'B',3)]:
            node = Circle(.65, color=col, stroke_width=2).move_to([x,-.65,0])
            label = words('Client '+name, 30, col).next_to(node, DOWN, .2)
            dots = VGroup(*[Dot(radius=.075,color=col) for _ in range(n)]).arrange(RIGHT,.18).move_to([x,-2,0])
            count = math('n_'+name+'='+str(n), 27,col).next_to(dots,DOWN,.17)
            nodes.append(node); labels.append(label); samples.append(VGroup(dots,count))
        self.chapters.append({'title':'Participants','start':0})
        say('Two clients keep their data locally; the server coordinates one shared model.')
        self.play(Create(server[0]), FadeIn(server[1],server_label),
                  *[Create(n) for n in nodes], *[FadeIn(g) for g in labels+samples],run_time=2,rate_func=ease)
        self.wait(2.5)
        stage('One model, two starting points', 'Broadcast the same parameter to both clients: each starts at w = 1.')
        paths = [ArcBetweenPoints(server.get_bottom(),n.get_top(),angle=a,color=MUTED,stroke_opacity=.45) for n,a in zip(nodes,[.3,-.3])]
        self.play(*[Create(p) for p in paths],run_time=1.1)
        packets = [math('1',36,col).move_to(server) for col in [A,B]]
        self.play(*[MoveAlongPath(p, path) for p,path in zip(packets,paths)],run_time=2.6,rate_func=ease)
        self.play(*[p.animate.move_to(n) for p,n in zip(packets,nodes)],run_time=.65,rate_func=ease)
        self.wait(2)

        stage('Local learning changes each copy', 'Use the model y = wx and mean squared error; take two local gradient steps.')
        self.play(*[FadeOut(g) for g in [server,server_label,*paths,*nodes,*samples,*packets]],
                  labels[0].animate.move_to([-3.5,2.15,0]),labels[1].animate.move_to([3.5,2.15,0]),run_time=1.4,rate_func=ease)
        update = math(r'w\leftarrow w-0.1\,\nabla F_k(w)',32).move_to([0,2.8,0])
        axes, curves, points, trackers, values, formulas = [],[],[],[],[],[]
        for x,col,mult,name in [(-3.5,A,1,'A'),(3.5,B,4,'B')]:
            ax = Axes(x_range=[.9,2.21,.2],y_range=[0,5.1,1],x_length=5.2,y_length=2.3,
                      tips=False,axis_config={'color':'#50596B','stroke_width':1.5}).move_to([x,-.05,0])
            curve = ax.plot(lambda w,m=mult:m*(w-2)**2,x_range=[.9,2.2],color=col,stroke_width=3)
            tracker=ValueTracker(1)
            point=always_redraw(lambda ax=ax,t=tracker,m=mult,c=col:Dot(ax.c2p(t.get_value(),m*(t.get_value()-2)**2),radius=.085,color=c))
            val=DecimalNumber(1,num_decimal_places=2,font_size=40,color=col).move_to([x+.4,-1.95,0])
            val.add_updater(lambda obj,t=tracker:obj.set_value(t.get_value()))
            prefix=math('w_'+name+'=',34,col).next_to(val,LEFT,.15)
            f=math(r'F_A(w)=(w-2)^2' if name=='A' else r'F_B(w)=(2w-4)^2',30,col).move_to([x,1.55,0])
            data=words('One example: (1, 2)' if name=='A' else 'Three copies of (2, 4)',23,MUTED).move_to([x,-2.55,0])
            axes.append(VGroup(ax,math('w',23).next_to(ax.x_axis,RIGHT,.1),math('F_'+name,23).next_to(ax.y_axis,UP,.1)))
            curves.append(curve); points.append(point);trackers.append(tracker);values.append(VGroup(prefix,val,data));formulas.append(f)
        self.play(FadeIn(update,*formulas,*values),*[Create(ax) for ax in axes],run_time=1.5)
        self.play(*[Create(c) for c in curves],*[FadeIn(p) for p in points],run_time=1.8)
        self.wait(2)
        say('First step: gradients -2 and -8 give different local updates.')
        self.play(trackers[0].animate.set_value(1.2),trackers[1].animate.set_value(1.8),run_time=3.2,rate_func=ease)
        self.wait(2.5)
        say('Second step: both gradients are now -1.6. The endpoints are 1.36 and 1.96.')
        self.play(trackers[0].animate.set_value(1.36),trackers[1].animate.set_value(1.96),run_time=3.2,rate_func=ease)
        self.wait(3)
        # Continuous dot motion visualizes each discrete step, not additional optimization steps.
        for p in points: p.clear_updaters()
        for v in values:v[1].clear_updaters()
        stage('Return the trained models', 'Clients send their final model parameters; their training examples stay local.')
        results=[math(r'w_A=1.36',40,A).move_to([-3.5,-1.95,0]),math(r'w_B=1.96',40,B).move_to([3.5,-1.95,0])]
        self.play(*[FadeOut(g) for g in [update,*axes,*curves,*points,*formulas,*values]],*[FadeIn(r) for r in results],run_time=1)
        self.play(labels[0].animate.move_to([-3.5,-.8,0]),labels[1].animate.move_to([3.5,-.8,0]),
                  results[0].animate.move_to([-3.5,-1.45,0]),results[1].animate.move_to([3.5,-1.45,0]),
                  FadeIn(server,server_label),run_time=1.5,rate_func=ease)
        uploads=[r.copy() for r in results]
        self.play(uploads[0].animate.scale(.7).move_to([-1.3,.55,0]),uploads[1].animate.scale(.7).move_to([1.3,.55,0]),run_time=2.8,rate_func=ease)
        self.wait(2)

        stage('The average has a geometry', 'Full participation: one example at A, three at B. Their weights are 1/4 and 3/4.')
        self.play(FadeOut(server,server_label,*uploads,*labels),
                  results[0].animate.move_to([-3.6,2.25,0]),results[1].animate.move_to([3.6,2.25,0]),run_time=1.2,rate_func=ease)
        line=NumberLine(x_range=[1.2,2.11,.1],length=10,include_numbers=True,font_size=23,color=MUTED).move_to(DOWN*.35)
        self.play(Create(line),run_time=1.3)
        da=Dot(line.n2p(1.36),color=A,radius=.1);db=Dot(line.n2p(1.96),color=B,radius=.1)
        weights=VGroup(math(r'\frac14',38,A).next_to(da,UP,.4),math(r'\frac34',38,B).next_to(db,UP,.4))
        self.play(TransformFromCopy(results[0],da),TransformFromCopy(results[1],db),FadeIn(weights),run_time=1.7,rate_func=ease)
        equation=math(r'w_{t+1}=\frac14\,(1.36)+\frac34\,(1.96)=1.81',39).move_to(UP*1.25)
        self.play(Write(equation),run_time=2.5)
        self.wait(2)
        say('The weighted mean is 1.81: three times closer to B than to A.')
        merged=Dot(line.n2p(1.81),radius=.11,color=GLOBAL)
        ghosts=[da.copy(),db.copy()]
        self.add(*ghosts)
        self.play(*[g.animate.move_to(merged).set_color(GLOBAL) for g in ghosts],run_time=3,rate_func=ease)
        self.remove(*ghosts);self.add(merged)
        mean=math('1.81',38,GLOBAL).next_to(merged,DOWN,.7)
        left=BraceBetweenPoints(line.n2p(1.36)+DOWN*.9,line.n2p(1.81)+DOWN*.9,direction=DOWN,color=A)
        right=BraceBetweenPoints(line.n2p(1.81)+DOWN*.9,line.n2p(1.96)+DOWN*.9,direction=DOWN,color=B)
        distances=VGroup(left,right,math('0.45',26,A).next_to(left,DOWN,.12),math('0.15',26,B).next_to(right,DOWN,.12))
        # Mean label sits above the line; braces reserve the lower region.
        mean.next_to(merged,UP,.28)
        self.play(FadeIn(mean),Create(left),Create(right),FadeIn(*distances[2:]),run_time=1.3)
        self.poster_time=round(self.time+.5,3)
        self.wait(4)
        stage('One round becomes the next', 'Broadcast w = 1.81. Repeat local training and aggregation until the chosen stopping rule.')
        nextmodel=math('1.81',36,GLOBAL).move_to(server)
        self.play(*[FadeOut(g) for g in [line,da,db,weights,equation,distances,*results,mean]],
                  merged.animate.move_to(server.get_center()),FadeIn(server[0],server_label),run_time=1.5,rate_func=ease)
        self.play(FadeOut(merged),FadeIn(nextmodel),*[Create(n) for n in nodes],
                  labels[0].animate.next_to(nodes[0],DOWN,.2),labels[1].animate.next_to(nodes[1],DOWN,.2),run_time=1)
        finalcopies=[math('1.81',29,col).move_to(server) for col in [A,B]]
        self.play(*[MoveAlongPath(p,path) for p,path in zip(finalcopies,paths)],*[Create(p) for p in paths],run_time=2.8,rate_func=ease)
        self.play(*[p.animate.move_to(n) for p,n in zip(finalcopies,nodes)],run_time=.65,rate_func=ease)
        self.wait(2)
        say('Keeping data local is not a privacy guarantee: model updates can still reveal information.')
        self.wait(4)
        self.cues[-1]['end']=round(self.time,3)
        Path(os.environ['MINIM_TIMELINE_PATH']).write_text(json.dumps({'duration':self.time,'cues':self.cues,'chapters':self.chapters,'poster_time':self.poster_time}))
