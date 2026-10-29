import json, math, sys, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from story import S
import sound
try:
    import scenes as _sc; SPECS=getattr(_sc,'SPECS',{})
except Exception: SPECS={}
PAGEK=('logrules','newrules','margins')
def is_page(img): return img.split('_')[0] in PAGEK or SPECS.get(img,{}).get('kind')=='page'
def smooth(x,k):
    c=np.cumsum(np.concatenate([[0],x])); y=(c[k:]-c[:-k])/k; pad=len(x)-len(y); return np.concatenate([np.full(pad//2,y[0]),y,np.full(pad-pad//2,y[-1])])
FPS=30; W,H=1920,1080; IW,IH=2880,1620; SR=sound.SR; LEAD=0.4
AD='audio2'
meta=json.load(open(AD+'/meta.json'))
# ---------- timeline ----------
segs=[]; t=LEAD; hud=None
for i,(v,txt,sh,ex) in enumerate(S):
    d=ex.get('dur') if v=='C' else meta[str(i)]
    pause=ex.get('pause',0.35 if v!='C' else 0.0)
    if 'hud' in ex: hud=ex['hud']
    segs.append(dict(i=i,v=v,start=t,dur=d,end=t+d+pause,shots=sh,cap=ex.get('cap'),hud=None if v=='C' or i>=len(S)-2 else hud,sfx=ex.get('sfx')))
    t+=d+pause
TOTAL=t+0.8
REDSEGS=[s['i'] for s in segs if any(x.split(':')[0].endswith('_red') or SPECS.get(x.split(':')[0],{}).get('tint')=='red' for x in s['shots'].split('|'))] or [97,98,99]
json.dump(dict(total=TOTAL,segs=segs),open('out/timeline.json','w'),indent=0)
def build_audio():
    n=int(TOTAL*SR)+SR; voice=np.zeros(n); fx=np.zeros(n); mus=np.zeros(n)
    for s in segs:
        if s['v']=='C': continue
        a,sr=sf.read(f"{AD}/seg{s['i']:03d}.wav"); a=a/(np.sqrt((a**2).mean())+1e-9)*0.10
        if s['v']=='R': a=sound.radio_fx(a)*0.30
        else: a=sound.verb(sound.lpf(a,9500,1)*0.6+a*0.4,0.35,0.12)[:len(a)+int(0.3*SR)]
        i=int(s['start']*SR); voice[i:i+len(a)]+=a
    for s in segs:
        if not s['sfx']: continue
        name,_,off=s['sfx'].partition('@'); off=float(off or 0)
        a=sound.SFX[name]()*sound.VOL[name]; i=int((s['start']+off)*SR); fx[i:i+len(a)]+=a[:n-i]
    # ambience: wind bed
    bed=sound.wind(TOTAL+1)[:n]*0.06 if False else np.tile(sound.wind(20),int(TOTAL/20)+2)[:n]*0.06
    # music: dark pad, muted on shocks; warm pad at resolution
    dark=sound.pad(TOTAL+1)[:n]; warm=sound.pad(TOTAL+1,(110,138.59,164.81),True)[:n]
    gain=np.ones(n)*0.16; wsw=np.zeros(n)
    resolve=TOTAL*0.86
    for s in segs:
        if s['sfx'] and s['sfx'].split('@')[0] in ('knock3','alarm','gen_off','stall'):
            a,b=int(s['start']*SR),int(s['end']*SR); gain[a:b]=0.0
    for s in segs:
        if s['i'] in REDSEGS[:3]: gain[int(s['start']*SR):int(s['end']*SR)]=0.0   # twist reveal: silence
    gain=smooth(gain,int(1.0*SR))
    wsw[int(resolve*SR):]=1; wsw=smooth(wsw,4*SR)
    mus=(dark*(1-wsw)+warm*wsw)*gain
    # duck music under voice
    venv=smooth(np.abs(voice),SR//4); duck=1-0.45*np.clip(venv/0.05,0,1)
    tone=sound.lpf(np.random.default_rng(9).normal(0,1,n),250)*0.004
    mix=voice+fx*0.55+mus*duck+bed+tone
    mix=mix/ max(1,np.abs(mix).max()/0.95)
    st=np.stack([mix,mix],1); st[:,1]=np.roll(mix,int(0.0004*SR))  # slight width
    sf.write('out/mix.wav',st,SR,subtype='PCM_16'); print('audio',TOTAL)
# ---------- video ----------
FB=ImageFont.truetype('/root/.fonts/BebasNeue-Regular.ttf',92); FH=ImageFont.truetype('/root/.fonts/BebasNeue-Regular.ttf',50)
def overlay_cap(text):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    w=d.textlength(text,font=FB); x=(W-w)/2; y=120
    d.text((x,y),text,font=FB,fill=(235,226,190,255),stroke_width=6,stroke_fill=(25,26,28,255)); return im
def overlay_hud(text):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); w=d.textlength(text,font=FH)
    d.rounded_rectangle((60,52,60+w+56,52+76),18,fill=(30,33,38,190)); d.text((88,62),text,font=FH,fill=(205,180,106,255)); return im
FS=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',50)
def chunks(t,mx=40):
    w=t.split(); out=[];cur=''
    for x in w:
        if cur and (len(cur)+1+len(x)>mx or cur[-1] in '.?!'): out.append(cur); cur=x
        else: cur=(cur+' '+x).strip()
    out.append(cur); return out
SUBS=[]
for s_ in segs:
    if s_['v']=='C' or s_['i']==len(S)-1: continue
    tx=S[s_['i']][1]
    for a_,b_ in [('Three oh seven A M','3:07 AM'),('three oh seven','3:07'),('Three oh four A M','3:04 AM'),('Three oh two A M','3:02 AM'),('two fifty-eight','2:58'),('three eleven','3:11')]: tx=tx.replace(a_,b_)
    cs=chunks(tx); tot=sum(len(c) for c in cs); t0=s_['start']
    for c in cs:
        d=s_['dur']*len(c)/tot; SUBS.append((t0,t0+d,c,s_['v'])); t0+=d
def write_srt(path):
    f=lambda x:f"{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int(x*1000%1000):03d}"
    open(path,'w').write('\n'.join(f"{k+1}\n{f(a)} --> {f(b)}\n{('Ruth: ' if v=='R' else '')+c}\n" for k,(a,b,c,v) in enumerate(SUBS)))
subcache={}
def overlay_sub(c,v):
    key=(c,v)
    if key in subcache: return subcache[key]
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); w=d.textlength(c,font=FS)
    d.rounded_rectangle(((W-w)/2-28,H-152,(W+w)/2+28,H-72),14,fill=(16,17,20,175))
    d.text(((W-w)/2,H-140),c,font=FS,fill=(250,247,238,255) if v=='N' else (232,212,140,255),stroke_width=5,stroke_fill=(18,18,20,255))
    if len(subcache)>40: subcache.pop(next(iter(subcache)))
    subcache[key]=im; return im
def ease(x): return x*x*(3-2*x)
def shot_frames(spec,nf,seed):
    parts=spec.split(':'); img=parts[0]; mv=parts[1] if len(parts)>1 else 'still'
    if len(parts)>2: cx,cy,z=[float(v) for v in parts[2].split(',')]
    else: cx,cy,z=960,540,None
    zf=z or 1.12; r=np.random.default_rng(seed)
    out=[]
    for f in range(nf):
        p=f/max(nf-1,1); e=ease(p); dx=dy=0
        if mv=='zin': Z=zf*0.88+(zf-zf*0.88)*e; X,Y=cx,cy
        elif mv=='zout': Z=zf-(zf-zf*0.88)*e; X,Y=cx,cy
        elif mv=='zin_fast': q=ease(min(1,p/0.35)); Z=max(1,zf*0.7)+(zf-max(1,zf*0.7))*q; X,Y=cx,cy
        elif mv=='zin_slow': Z=zf*0.95+zf*0.05*e; X,Y=cx,cy
        elif mv in('pl','pr','pu','pd'):
            Z=max(zf,1.18); sx=(1920-1920/Z)/2*0.85; sy=(1080-1080/Z)/2*0.85; sgn=1 if mv in('pl','pu') else -1
            X=cx+(sgn*sx*(1-2*e) if mv in('pl','pr') else 0); Y=cy+(sgn*sy*(1-2*e) if mv in('pu','pd') else 0)
        elif mv=='shake':
            Z=zf+0.03; X,Y=cx,cy; amp=14*max(0,1-p*1.3); dx,dy=r.normal(0,amp,2)
        else: Z=(z or 1.0)*(1+0.012*e); X,Y=cx,cy
        out.append((X+dx,Y+dy,max(Z,1.0)))
    return img,out
cache={}
def getimg(name):
    if name not in cache:
        if len(cache)>5: cache.pop(next(iter(cache)))
        cache[name]=Image.open(f'img/{name}.png').convert('RGB')
    return cache[name]
def render(a=0,b=None):
    total_frames=int(TOTAL*FPS); b=b or total_frames
    cmd=['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',f'out/video_{a:06d}.mp4']
    pr=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    black=np.zeros((H,W,3),np.uint8)
    # build per-frame plan
    plan=[None]*total_frames
    for si,s in enumerate(segs):
        f0=int(s['start']*FPS); f1=int(segs[si+1]['start']*FPS) if si+1<len(segs) else total_frames
        if si==0: f0=0
        if s['v']=='C': spec_list=[f"card{s['i']:03d}:zin_slow"]
        else: spec_list=s['shots'].split('|')
        n=len(spec_list); L=f1-f0
        for k,spec in enumerate(spec_list):
            g0=f0+L*k//n; g1=f0+L*(k+1)//n
            img,cams=shot_frames(spec,g1-g0,s['i']*10+k)
            for j,c in enumerate(cams): plan[g0+j]=(img,c,s,g0+j-f0,g1-(g0+j))
    caps={}; huds={}; sub_i=[0]
    for fi in range(a,b):
        if plan[fi] is None: pr.stdin.write(black.tobytes()); continue
        img,(X,Y,Z),s,since,left=plan[fi]
        im=getimg(img); cw,ch=IW/Z,IH/Z; X*=1.5; Y*=1.5
        x0=max(0,min(X-cw/2,IW-cw)); y0=max(0,min(Y-ch/2,IH-ch))
        fr=im.resize((W,H),Image.BILINEAR,box=(x0,y0,x0+cw,y0+ch))
        if s['v']=='C':
            fade=min(1,since/8,left/6)
            if fade<1: fr=Image.blend(Image.new('RGB',(W,H)),fr,fade)
        if fi<12: fr=Image.blend(Image.new('RGB',(W,H)),fr,fi/12)
        if fi>total_frames-40: fr=Image.blend(Image.new('RGB',(W,H)),fr,max(0,(total_frames-fi)/40))
        fr=fr.convert('RGBA')
        if s['hud'] and img.split('_')[0] not in ('logrules','newrules','margins'):
            o=huds.get(s['hud']) or huds.setdefault(s['hud'],overlay_hud(s['hud'])); fr.alpha_composite(o)
        if s['cap'] and since>6:
            o=caps.get(s['cap']) or caps.setdefault(s['cap'],overlay_cap(s['cap']))
            al=min(1,(since-6)/6)
            fr.alpha_composite(o if al>=1 else Image.blend(Image.new('RGBA',(W,H)),o,al))
        tt=fi/FPS
        while SUBS and sub_i[0]<len(SUBS)-1 and SUBS[sub_i[0]][1]<tt: sub_i[0]+=1
        a_,b_,c_,v_=SUBS[sub_i[0]]
        if is_page(img):
            if 'lb' not in huds: huds['lb']=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(huds['lb']).rectangle((0,H-175,W,H),fill=(30,33,38,255))
            fr.alpha_composite(huds['lb'])
        if a_<=tt<b_+0.25: fr.alpha_composite(overlay_sub(c_,v_))
        pr.stdin.write(fr.convert('RGB').tobytes())
        if fi%300==0: open('out/progress.txt','w').write(f'{fi}/{total_frames}')
    pr.stdin.close(); pr.wait(); open('out/progress.txt','w').write(f'DONE {a}-{b}')
if __name__=='__main__':
    if sys.argv[1]=='audio': build_audio()
    if sys.argv[1]=='video': render(*[int(x) for x in sys.argv[2:]])
    if sys.argv[1]=='srt': write_srt('out/kestrel_ridge.en.srt')
    if sys.argv[1]=='info': print('total',TOTAL, int(TOTAL*FPS),'frames')
