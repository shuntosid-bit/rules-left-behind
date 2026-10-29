# Vertical 1080x1920 Short cut from an approved long episode (hook + first knock + CTA)
import json, subprocess, numpy as np, soundfile as sf, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import make
from make import segs, SUBS, S, shot_frames, getimg, IW, IH, SR
import sound
W,H,FPS=1080,1920,30
PAGES=('logrules','newrules','margins')
RANGES=json.loads(sys.argv[1]) if len(sys.argv)>1 else [[0,4],[41,44]]
HOOK=sys.argv[2] if len(sys.argv)>2 else "SOMEONE KNOCKS AT 3:07 AM"
CTA_T=3.2
FT=ImageFont.truetype('/root/.fonts/BebasNeue-Regular.ttf',96); FS=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',58)
FC=ImageFont.truetype('/root/.fonts/BebasNeue-Regular.ttf',120); FC2=ImageFont.truetype('/root/.fonts/BebasNeue-Regular.ttf',64)
def wrap(d,t,f,mx):
    w=t.split();L=[];c=''
    for x in w:
        if d.textlength((c+' '+x).strip(),font=f)>mx and c: L.append(c);c=x
        else: c=(c+' '+x).strip()
    return L+[c]
# map short time -> long time
pieces=[]
for a,b in RANGES:
    t0=segs[a]['start']-(0.3 if a else 0.4); t1=segs[b]['end']; pieces.append((t0,t1))
dur=sum(b-a for a,b in pieces)+CTA_T
mix,sr=sf.read('out/mix.wav'); out=[]
for a,b in pieces:
    x=mix[int(a*sr):int(b*sr)].copy(); f=int(.03*sr); x[:f]*=np.linspace(0,1,f)[:,None]; x[-f:]*=np.linspace(1,0,f)[:,None]; out.append(x)
h=sound.hit()*0.5; h=np.stack([h,h],1)[:int(CTA_T*sr)]; out.append(np.vstack([h,np.zeros((int(CTA_T*sr)-len(h),2))]))
sf.write('out/short_audio.wav',np.vstack(out),sr)
def long_t(ts):
    for a,b in pieces:
        if ts<b-a: return a+ts
        ts-=b-a
    return None
def frame_at(t):
    for si,s in enumerate(segs):
        nxt=segs[si+1]['start'] if si+1<len(segs) else 1e9
        if s['start']<=t<nxt or (si==0 and t<s['start']): break
    specs=[f"card{s['i']:03d}:zin_slow"] if s['v']=='C' else s['shots'].split('|')
    L=nxt-s['start']; k=min(int((t-s['start'])/L*len(specs)),len(specs)-1)
    g0=s['start']+L*k/len(specs); g1=s['start']+L*(k+1)/len(specs)
    nf=max(int((g1-g0)*FPS),2); img,cams=shot_frames(specs[k],nf,s['i']*10+k)
    X,Y,Z=cams[min(int((t-g0)*FPS),nf-1)]; im=getimg(img)
    VF={'ext_wide':1265,'radiodesk':1050,'heli_drop':1000,'genstall':1300,'hallway':700,'dig':1150,'heli_day30':1500,'field_noon':1150}
    base=img.replace('_red','')
    if base in VF: X=VF[base]
    if make.is_page(base) or base.split('_')[0] in PAGES: Z=min(Z,1.08); X=960
    X*=1.5;Y*=1.5
    if make.is_page(img) or img.startswith('card') or img in('fuel','tempchart','snowwater','map','cosym','codiag') or make.SPECS.get(img,{}).get('kind')=='info':
        cw,ch=IW/Z,IH/Z; x0=max(0,min(X-cw/2,IW-cw)); y0=max(0,min(Y-ch/2,IH-ch))
        c=im.resize((W,int(W*9/16)),Image.BILINEAR,box=(x0,y0,x0+cw,y0+ch))
        bg=Image.new('RGB',(W,H),(30,33,38)); bg.paste(c,(0,(H-c.height)//2-60)); return bg,s
    ch=IH/Z; cw=ch*9/16; x0=max(0,min(X-cw/2,IW-cw)); y0=max(0,min(Y-ch/2,IH-ch))
    return im.resize((W,H),Image.BILINEAR,box=(x0,y0,x0+cw,y0+ch)),s
top=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(top)
d.rounded_rectangle((60,150,W-60,330),24,fill=(20,22,26,200))
for i,l in enumerate(wrap(d,HOOK,FT,880)): w=d.textlength(l,font=FT); d.text(((W-w)/2,172+i*92),l,font=FT,fill=(227,211,154,255))
cmd=['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-','-i','out/short_audio.wav','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','out/short_v1.mp4']
pr=subprocess.Popen(cmd,stdin=subprocess.PIPE); nfr=int(dur*FPS)
for fi in range(nfr):
    ts=fi/FPS; lt=long_t(ts)
    if lt is None:
        fr=Image.new('RGB',(W,H),(30,33,38)); dd=ImageDraw.Draw(fr)
        for i,l in enumerate(['WHO IS KNOCKING?','FULL STORY ON','RULES LEFT BEHIND']):
            f=FC if i!=1 else FC2; w=dd.textlength(l,font=f); dd.text(((W-w)/2,760+i*130),l,font=f,fill=(227,211,154) if i!=1 else (200,196,186))
        pr.stdin.write(fr.tobytes()); continue
    fr,s=frame_at(lt); fr=fr.convert('RGBA'); fr.alpha_composite(top)
    for a,b,c,v in SUBS:
        if a<=lt<b+0.2:
            o=Image.new('RGBA',(W,H),(0,0,0,0)); dd=ImageDraw.Draw(o); ls=wrap(dd,c,FS,900)
            y=1380; dd.rounded_rectangle((70,y-20,W-70,y+len(ls)*76+10),20,fill=(16,17,20,190))
            for i,l in enumerate(ls): w=dd.textlength(l,font=FS); dd.text(((W-w)/2,y+i*76),l,font=FS,fill=(250,247,238) if v=='N' else (232,212,140),stroke_width=4,stroke_fill=(18,18,20))
            fr.alpha_composite(o); break
    pr.stdin.write(fr.convert('RGB').tobytes())
pr.stdin.close(); pr.wait(); print('SHORT',round(dur,1))
