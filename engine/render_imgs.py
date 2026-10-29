import cairosvg, io, sys, numpy as np
from PIL import Image, ImageFilter
import scenes
W,H=2880,1620
rng=np.random.default_rng(1)
grain=rng.normal(0,1,(H//2,W//2)).astype(np.float32)
grain=np.array(Image.fromarray(grain).resize((W,H),Image.BILINEAR))
yy,xx=np.mgrid[0:H,0:W]; vig=1-0.22*(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)**1.3; vig=np.clip(vig,0.45,1)[...,None]
def finish(png):
    a=np.asarray(Image.open(io.BytesIO(png)).convert('RGB')).astype(np.float32)
    a=a*vig+grain[...,None]*3.5
    return np.clip(a,0,255).astype(np.uint8)
def red(a):
    g=a.astype(np.float32).mean(2,keepdims=True); t=np.concatenate([g*1.05+28,g*.55,g*.5],2)
    return np.clip(t*.92,0,255).astype(np.uint8)
from story import S
names=[n for n in sys.argv[1:]] or list(scenes.D)
for n in names:
    a=finish(cairosvg.svg2png(bytestring=scenes.D[n]().encode(),output_width=W,output_height=H))
    Image.fromarray(a).save(f'img/{n}.png')
for b in ['ext_night','logrules','photo_hal','headache','tempchart','ruth','drift2']:
    if b in names: Image.fromarray(red(np.asarray(Image.open(f'img/{b}.png')))).save(f'img/{b}_red.png')
for b in getattr(scenes,'RED',()):
    Image.fromarray(red(np.asarray(Image.open(f'img/{b}.png')))).save(f'img/{b}.png')
for i,(v,t,sh,ex) in enumerate(S):
    if v=='C' and (not sys.argv[1:]):
        a=finish(cairosvg.svg2png(bytestring=scenes.card(t,ex.get('sub','')).encode(),output_width=W,output_height=H)); Image.fromarray(a).save(f'img/card{i:03d}.png')
print('rendered',len(names))
