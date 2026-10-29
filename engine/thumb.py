"""Thumbnail: first exterior/door/clock shot + big hook text."""
import json, sys
from PIL import Image, ImageDraw, ImageFont
from story import S
import scenes
meta=json.load(open(sys.argv[1])); hook=meta['short']['hook'] or meta['title'][:24].upper()
specs=getattr(scenes,'SPECS',{})
pick=next((sh.split(':')[0] for v,t,sh,e in S if v!='C' and specs.get(sh.split(':')[0],{}).get('kind') in ('exterior','closeup')), None) or next(sh.split(':')[0] for v,t,sh,e in S if v!='C')
im=Image.open(f'img/{pick}.png').resize((1280,720)); d=ImageDraw.Draw(im)
F=ImageFont.truetype(__import__('os').path.expanduser('~/.fonts/BebasNeue-Regular.ttf'),130)
words=hook.split(); lines=[' '.join(words[:3]),' '.join(words[3:])] if len(words)>3 else [hook]
for i,l in enumerate(lines): d.text((50,40+i*130),l,font=F,fill=(227,211,154),stroke_width=8,stroke_fill=(20,20,22))
im.save('out/thumbnail.jpg',quality=90); print('thumb',pick)
