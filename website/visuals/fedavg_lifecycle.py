"""An original, captioned mathematical explanation of one FedAvg round.

Algorithm source: McMahan et al. (2017), Section 2 and Algorithm 1.
https://proceedings.mlr.press/v54/mcmahan17a.html
The two-client arithmetic is an invented teaching example, not a reproduction.
"""
import json
import re
from html import escape
import os
from pathlib import Path

import numpy as np
from manim import (
    Scene, VGroup, Text, MarkupText, RoundedRectangle, Rectangle, Circle, Line, Arrow,
    Dot, Axes, FadeIn, FadeOut, Create, GrowArrow, Transform, Indicate,
    MoveAlongPath, AnimationGroup, LaggedStart, UP, DOWN, LEFT, RIGHT,
    WHITE, config, smooth,
)

BG = '#101827'
PANEL = '#172337'
LINE = '#344761'
INK = '#EDF3FC'
MUTED = '#A8B8CF'
BLUE = '#82B9FF'
GOLD = '#F4C16B'
MINT = '#8ED8C4'
FONT = 'DejaVu Sans'
MONO = 'DejaVu Sans Mono'


def text(value, size=26, color=INK, mono=False):
    # Pango draws proper subscripts without requiring a system TeX installation.
    # Keep source identifiers readable while rendering mathematical notation.
    notation = re.compile(r'\b([Fwn])_(next|t|A|B)\b')
    if notation.search(value):
        markup = notation.sub(lambda match: match[1] + '<sub>' + ('t+1' if match[2] == 'next' else match[2]) + '</sub>', escape(value))
        return MarkupText(markup, font=MONO if mono else FONT, font_size=size, color=color)
    return Text(value, font=MONO if mono else FONT, font_size=size, color=color)


def label(value, point, size=26, color=INK, mono=False):
    return text(value, size, color, mono).move_to(point)


def panel(center, width, height, color=LINE):
    return RoundedRectangle(width=width, height=height, corner_radius=.16,
                            stroke_color=color, stroke_width=1.6,
                            fill_color=PANEL, fill_opacity=1).move_to(center)


class FedAvgLifecycle(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.cues = []
        self.heading = None
        self.caption = None
        self.progress = VGroup(*[
            Circle(radius=.055, stroke_width=0, fill_color=LINE, fill_opacity=1)
            .move_to([-5.93+i*.24, 3.55, 0]) for i in range(6)
        ])
        self.add(self.progress)
        corner = label('FEDAVG / ONE COMMUNICATION ROUND', [2.88,3.55,0], 15, MUTED)
        rule = Line([-6.3,3.28,0],[6.3,3.28,0], color=LINE, stroke_width=1)
        self.add(corner, rule)
        self.source = label('McMahan et al. · AISTATS 2017 · Algorithm 1  |  Original teaching example', [0,-3.65,0], 14, MUTED)
        self.add(self.source)

        self.stage(0, '01  Start from one shared model',
                   'Two honest clients participate. Their raw examples remain local.')
        server, clients, server_value, values, data = self.network()
        self.play(FadeIn(server, shift=DOWN*.12), run_time=.8)
        self.play(LaggedStart(*[FadeIn(client, shift=UP*.12) for client in clients], lag_ratio=.2), run_time=1)
        self.play(FadeIn(data), run_time=.7)
        tagline = label('Same architecture. Same starting parameter.', [0,-2.6,0], 23, MUTED)
        self.play(FadeIn(tagline), run_time=.6)
        self.wait(3)

        self.stage(1, '02  Broadcast the current model',
                   'The server sends w = 1 to both clients. Model parameters travel; training data do not.')
        self.play(FadeOut(tagline), run_time=.4)
        down_paths = self.paths(server[0], clients, downward=True)
        self.play(*[GrowArrow(path) for path in down_paths], run_time=.7)
        tokens = VGroup(*[self.token('1.00', BLUE).move_to(path.get_start()) for path in down_paths])
        self.play(FadeIn(tokens), run_time=.3)
        self.play(*[MoveAlongPath(token,path) for token,path in zip(tokens,down_paths)], run_time=2, rate_func=smooth)
        new_values = [label('w = 1.00', v.get_center(), 29, BLUE, True) for v in values]
        self.play(FadeOut(tokens), *[Transform(v,n) for v,n in zip(values,new_values)], run_time=.7)
        self.wait(3)

        self.stage(2, '03  Train locally, in parallel',
                   'Each client takes two full-batch gradient steps with learning rate 0.1.')
        self.play(FadeOut(server), FadeOut(clients), FadeOut(data), FadeOut(down_paths), run_time=.7)
        training, dots, axes, current, gradient, updates = self.training_panels()
        self.play(FadeIn(training), run_time=.8)
        shared = label('Model: ŷ = wx     Loss: (wx − y)²     Step: w ← w − 0.1 ∇F(w)', [0,2.30,0], 22, MUTED)
        self.play(FadeIn(shared), run_time=.6)
        self.wait(4)
        self.set_caption('Client A: gradient −2 gives 1.20. Client B: gradient −8 gives 1.80.')
        first_w = [1.2,1.8]
        first_grad = ['∇F = −2.00', '∇F = −8.00']
        first_update = ['1.00 − 0.1 × (−2) = 1.20', '1.00 − 0.1 × (−8) = 1.80']
        self.play(*[Transform(g,label(value,g.get_center(),22,color,True)) for g,value,color in zip(gradient,first_grad,[BLUE,GOLD])], run_time=.7)
        self.play(*[MoveAlongPath(dots[i], axes[i].plot(lambda u: (u-2)**2*(1 if i==0 else 4), x_range=[1,w], use_smoothing=False)) for i,w in enumerate(first_w)],
                  *[Transform(current[i],label(f'w = {w:.2f}',current[i].get_center(),28,[BLUE,GOLD][i],True)) for i,w in enumerate(first_w)],
                  *[Transform(updates[i],label(first_update[i],updates[i].get_center(),19,INK,True)) for i in range(2)], run_time=2)
        self.wait(4)
        self.set_caption('The next gradients are evaluated at different local parameters: 1.20 and 1.80.')
        self.wait(2)
        second_w = [1.36,1.96]
        second_update = ['1.20 − 0.1 × (−1.6) = 1.36', '1.80 − 0.1 × (−1.6) = 1.96']
        self.play(*[Transform(g,label('∇F = −1.60',g.get_center(),22,color,True)) for g,color in zip(gradient,[BLUE,GOLD])],run_time=.7)
        self.play(*[MoveAlongPath(dots[i], axes[i].plot(lambda u: (u-2)**2*(1 if i==0 else 4), x_range=[first_w[i],w], use_smoothing=False)) for i,w in enumerate(second_w)],
                  *[Transform(current[i],label(f'w = {w:.2f}',current[i].get_center(),28,[BLUE,GOLD][i],True)) for i,w in enumerate(second_w)],
                  *[Transform(updates[i],label(second_update[i],updates[i].get_center(),19,INK,True)) for i in range(2)],run_time=2)
        self.wait(4)
        self.set_caption('Averaging B’s three identical losses leaves the mean loss (2w − 4)².')
        self.wait(4)

        self.stage(3, '04  Return the trained parameters',
                   'Clients return 1.36 and 1.96. The server has not seen their raw examples.')
        self.play(FadeOut(training),FadeOut(shared),run_time=.7)
        server,clients,server_value,values,data=self.network(server_text='Waiting for models',client_values=['1.36','1.96'])
        self.play(FadeIn(server),FadeIn(clients),FadeIn(data),run_time=.8)
        up_paths=self.paths(server[0],clients,downward=False)
        self.play(*[GrowArrow(path) for path in up_paths],run_time=.7)
        tokens=VGroup(*[self.token(value,color).move_to(path.get_start()) for value,color,path in zip(['1.36','1.96'],[BLUE,GOLD],up_paths)])
        self.play(FadeIn(tokens),run_time=.3)
        self.play(*[MoveAlongPath(token,path) for token,path in zip(tokens,up_paths)],run_time=2)
        self.play(FadeOut(tokens),Transform(server_value,label('Two models received',server_value.get_center(),24,INK)),run_time=.6)
        self.wait(3)

        self.stage(4, '05  Average by sample count',
                   'Full participation: weights are 1/4 and 3/4. They reflect sample counts, not trust.')
        self.play(FadeOut(server),FadeOut(clients),FadeOut(data),FadeOut(up_paths),run_time=.7)
        count = label('n_A = 1       n_B = 3       n = 4', [0,2.2,0], 27, MUTED,True)
        identity=label('w_next = (n_A / n) w_A + (n_B / n) w_B',[0,1.4,0],27,INK,True)
        self.play(FadeIn(count),FadeIn(identity),run_time=.8)
        bar_a=Rectangle(width=2.5,height=.25,stroke_width=0,fill_color=BLUE,fill_opacity=1).move_to([-3.75,.55,0])
        bar_b=Rectangle(width=7.5,height=.25,stroke_width=0,fill_color=GOLD,fill_opacity=1).move_to([1.25,.55,0])
        weight_a=label('A · 25%',[-3.75,.02,0],23,BLUE)
        weight_b=label('B · 75%',[1.25,.02,0],23,GOLD)
        self.play(Create(bar_a),Create(bar_b),FadeIn(weight_a),FadeIn(weight_b),run_time=1)
        terms=VGroup(label('0.25 × 1.36',[-2.6,-.85,0],33,BLUE,True),label('+',[0,-.85,0],33,INK),label('0.75 × 1.96',[2.6,-.85,0],33,GOLD,True))
        self.play(FadeIn(terms,shift=UP*.1),run_time=.8)
        self.wait(3)
        products=VGroup(label('0.34',[-2.6,-.85,0],33,BLUE,True),label('+',[0,-.85,0],33,INK),label('1.47',[2.6,-.85,0],33,GOLD,True))
        self.play(Transform(terms,products),run_time=1)
        self.wait(1.5)
        result=label('w_next = 1.81',[0,-1.95,0],43,MINT,True)
        self.play(FadeIn(result,shift=UP*.15),run_time=.8)
        self.play(Indicate(result,color=MINT,scale_factor=1.035),run_time=1)
        self.wait(3)

        self.stage(5, '06  Begin the next round',
                   'The new global model is 1.81. Broadcast it again and repeat until the stopping rule is met.')
        self.play(*[FadeOut(item) for item in [count,identity,bar_a,bar_b,weight_a,weight_b,terms,result]],run_time=.7)
        server,clients,server_value,values,data=self.network(server_text='w_next = 1.81',client_values=['1.36','1.96'])
        self.play(FadeIn(server),FadeIn(clients),FadeIn(data),run_time=.8)
        down_paths=self.paths(server[0],clients,downward=True)
        self.play(*[GrowArrow(path) for path in down_paths],run_time=.7)
        tokens=VGroup(*[self.token('1.81',MINT).move_to(path.get_start()) for path in down_paths])
        self.play(FadeIn(tokens),run_time=.3)
        self.play(*[MoveAlongPath(token,path) for token,path in zip(tokens,down_paths)],run_time=2)
        self.play(FadeOut(tokens),*[Transform(value,label('w = 1.81',value.get_center(),29,MINT,True)) for value in values],run_time=.7)
        self.wait(3)
        self.set_caption('Keeping data local is not a privacy guarantee. This example assumes honest, synchronous clients.')
        self.wait(5)
        self.finish_cues()

    def stage(self,index,title,caption):
        heading=label(title,[0,2.86,0],31,INK)
        self.progress[index].set_fill([BLUE,BLUE,BLUE,GOLD,GOLD,MINT][index])
        if self.heading is None:self.play(FadeIn(heading),run_time=.6);self.heading=heading
        else:self.play(Transform(self.heading,heading),run_time=.6)
        self.set_caption(caption)

    def set_caption(self,caption):
        if self.cues:self.cues[-1]['end']=round(float(self.time),3)
        self.cues.append({'start':round(float(self.time),3),'text':caption})
        # Captions are also baked in so the silent explanation remains accessible
        # when the exported MP4 is played outside the website.
        if len(caption) <= 84:
            lines = caption
        else:
            split = min((i for i, char in enumerate(caption) if char == ' '), key=lambda i: abs(i - len(caption)/2))
            lines = caption[:split] + '\n' + caption[split+1:]
        new=label(lines,[0,-3.08,0],22,MUTED)
        if self.caption is None:self.add(new);self.caption=new
        else:self.remove(self.caption);self.add(new);self.caption=new

    def network(self,server_text='w_t = 1.00',client_values=None):
        center=[0,1.45,0]
        shape=panel(center,3.7,1.25)
        title=label('COORDINATING SERVER',[0,1.76,0],17,MUTED)
        value=label(server_text,[0,1.22,0],26,INK,mono=server_text.startswith('w'))
        server=VGroup(shape,title,value)
        clients=VGroup();values=[];data=VGroup()
        for i,(x,color,name,n,point) in enumerate([(-4,BLUE,'CLIENT A',1,'(x, y) = (1, 2)'),(4,GOLD,'CLIENT B',3,'3 copies of (2, 4)')]):
            card=panel([x,-.9,0],3.9,1.7,color)
            heading=label(name,[x,-.4,0],23,color)
            val=label('w = '+client_values[i] if client_values else 'Ready to receive',[x,-1.03,0],29 if client_values else 22,color,mono=bool(client_values))
            clients.add(VGroup(card,heading,val));values.append(val)
            data_panel=panel([x,-2.15,0],3.9,.6)
            description=label(f'n = {n} · {point}',[x,-2.15,0],18,MUTED)
            data.add(VGroup(data_panel,description))
        return server,clients,value,values,data

    def paths(self,server_shape,clients,downward):
        arrows=VGroup()
        for i,client in enumerate(clients):
            sign=-1 if i==0 else 1
            a=server_shape.get_bottom()+RIGHT*sign*.75
            b=client[0].get_top()
            if not downward:a,b=b,a
            arrows.add(Arrow(a,b,buff=.15,color=BLUE if i==0 else GOLD,stroke_width=2.6,max_tip_length_to_length_ratio=.09))
        return arrows

    def token(self,value,color):
        shape=RoundedRectangle(width=1.07,height=.48,corner_radius=.1,stroke_color=color,stroke_width=1.7,fill_color=BG,fill_opacity=1)
        return VGroup(shape,text(value,19,color,True))

    def training_panels(self):
        group=VGroup();dots=[];all_axes=[];current=[];gradients=[];updates=[]
        for i,(x,color,name,loss) in enumerate([(-3.35,BLUE,'CLIENT A · one example','F_A(w) = (w − 2)²'),(3.35,GOLD,'CLIENT B · three copies','F_B(w) = (2w − 4)²')]):
            card=panel([x,-.15,0],6.05,4.45)
            title=label(name,[x,1.66,0],22,color)
            formula=label(loss,[x,1.15,0],22,INK,True)
            axes=Axes(x_range=[.5,2.5,.5],y_range=[0,4.5,1],x_length=4.5,y_length=1.3,tips=False,axis_config={'stroke_color':LINE,'stroke_width':1.3}).move_to([x,.05,0])
            curve=axes.plot(lambda w:(w-2)**2*(1 if i==0 else 4),x_range=[.95,2.35],color=color,stroke_width=3)
            dot=Dot(axes.c2p(1,1 if i==0 else 4),radius=.065,color=color)
            axis_labels=VGroup(label('1',[axes.c2p(1,0)[0],axes.c2p(1,0)[1]-.17,0],14,MUTED),label('2',[axes.c2p(2,0)[0],axes.c2p(2,0)[1]-.17,0],14,MUTED),label('w',axes.get_right()+RIGHT*.18,16,MUTED),label('loss',axes.get_top()+UP*.11,14,MUTED))
            cur=label('w = 1.00',[x,-1.12,0],28,color,True)
            grad=label('Compute local gradient',[x,-1.67,0],22,MUTED,True)
            update=label('Both clients begin at w = 1',[x,-2.12,0],19,INK,True)
            group.add(card,title,formula,axes,curve,dot,axis_labels,cur,grad,update)
            dots.append(dot);all_axes.append(axes);current.append(cur);gradients.append(grad);updates.append(update)
        return group,dots,all_axes,current,gradients,updates

    def finish_cues(self):
        self.cues[-1]['end']=round(float(self.time),3)
        path=os.environ.get('MINIM_TIMELINE_PATH')
        if path:Path(path).write_text(json.dumps({'duration':round(float(self.time),3),'cues':self.cues},indent=2)+'\n')
