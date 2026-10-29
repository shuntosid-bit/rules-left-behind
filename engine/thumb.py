"""Auto thumbnail in one of two house styles (A/B test for a month):
  rules: the left-behind rules page with the key rule circled + scared face + big time/hook
  alone: the place at night, tiny lit building, two big words + one small line
Usage: python3 thumb.py meta.json <style>   -> out/thumbnail.jpg"""
import json, sys, io, os, re
import cairosvg, numpy as np
from PIL import Image, ImageDraw, ImageFont
from artlib import *
import kit
from scenes_ep1_lib import page, mountains, station, snowfall
from story import S
import scenes
W,H=1280,720; BB=os.path.expanduser('~/.fonts/BebasNeue-Regular.ttf')
meta=json.load(open(sys.argv[1])); style=sys.argv[2] if len(sys.argv)>2 else 'rules'
th=meta.get('thumb',{}); hook=(meta.get('short',{}).get('hook') or meta['title']).upper().split()
SPECS=getattr(scenes,'SPECS',{})
def png(s,w=1920,h=1080,mode='RGB'): return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode(),output_width=w,output_height=h))).convert(mode)
def txt_(im,xy,s,size,fill,stroke=10,anchor='la'):
    ImageDraw.Draw(im).text(xy,s,font=ImageFont.truetype(BB,size),fill=fill,stroke_width=stroke,stroke_fill=(15,15,18),anchor=anchor)
def fit(im,xy,s,size,fill,maxw,stroke=10):
    f=ImageFont.truetype(BB,size)
    while ImageDraw.Draw(im).textlength(s,font=f)>maxw and size>40: size-=6; f=ImageFont.truetype(BB,size)
    txt_(im,xy,s,size,fill,stroke)
def finish(im):
    a=np.asarray(im).astype(np.float32); yy,xx=np.mgrid[0:H,0:W]
    v=1-0.30*(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2); a=a*np.clip(v,0.55,1)[...,None]
    a+=np.random.default_rng(1).normal(0,3,a.shape[:2])[...,None]
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
face=png(svg(figure(960,1500,5.2,expr='scared',look=-1,arms=((10,-5),(-10,5)))),mode='RGBA')
if style=='rules':
    pg=next((v for v in SPECS.values() if v.get('kind')=='page'),None)
    title=(pg or {}).get('title','RULES'); lines=[re.sub(r'\s+',' ',l) for l in (pg or {}).get('lines',['1. Keep the door shut.','2. DO NOT ANSWER.','3. Keep the radio on.'])][:3]
    key=next((i for i,l in enumerate(lines) if re.search(r"\b(NOT|NEVER|DON'?T|DO NOT)\b",l.upper())),min(1,len(lines)-1))
    KF=os.path.expanduser('~/.fonts/Kalam-Bold.ttf')
    def sized(l,maxw):
        for sz in range(100,54,-4):
            if ImageFont.truetype(KF,sz).getlength(l)<=maxw: return l,sz
        w=l.split()
        while w and ImageFont.truetype(KF,56).getlength(' '.join(w)+'…')>maxw: w.pop()
        return ' '.join(w)+'…',56
    L=[(250,title[:14],120,'Kalam',P['ch'],0)]
    for i,l in enumerate(lines):
        t,sz=sized(l,1150 if i==0 else 930); L.append((430+i*180,t,sz,'Kalam',P['ch'],-1))
    o=page(L)+f'<ellipse cx="760" cy="{430+key*180-30}" rx="560" ry="105" fill="none" stroke="#C0402F" stroke-width="16" transform="rotate(-3 760 {430+key*180-30})"/>'
    im=png(svg(o)).resize((W,H)); f=face.resize((int(W*.70),int(H*.70))); im.paste(f,(600,245),f)
    big=th.get('rules_text') or ' '.join(hook[:2])
    ImageDraw.Draw(im).rectangle((0,560,700,720),fill=(20,22,26)); fit(im,(40,568),big,150,(242,217,138),640)
else:
    ex=next((dict(v) for v in SPECS.values() if v.get('kind')=='exterior'),{'kind':'exterior','setting':'mountain','building':'hut'})
    ex.update(time='night',weather=ex.get('weather') if ex.get('weather') in('snow','storm','rain','fog') else 'snow',lit=True); ex.pop('figure',None); ex.pop('tint',None)
    if ex.get('weather') not in ('snow','storm','rain'): ex['weather']='snow'
    sv=kit.render(ex); i0=sv.index('</defs>')+7; sv=sv[:i0]+'<rect width="1920" height="1080" fill="#1A222C"/><g transform="translate(470,40)">'+sv[i0:-6]+'</g></svg>'
    im=png(sv).resize((W,H))
    l1=th.get('line1') or hook[0]; l2=th.get('line2') or (hook[1] if len(hook)>1 else '')
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(ov).rectangle((0,0,760,520),fill=(14,17,22,190)); im=Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB')
    fit(im,(50,60),l1,165,(242,217,138),680); fit(im,(50,225),l2,165,(232,90,70),680)
    if th.get('sub') or len(hook)>2: fit(im,(54,410),(th.get('sub') or ' '.join(hook[2:])),62,(235,232,222),680,6)
im=finish(im); im.save('out/thumbnail.jpg',quality=92); print('thumbnail',style)
