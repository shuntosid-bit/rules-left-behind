import numpy as np
SR=24000
rng=np.random.default_rng(3)
def t(d): return np.arange(int(d*SR))/SR
def env(n,a=.005,r=.2):
    e=np.ones(n); A=int(a*SR); Rr=int(r*SR)
    if A: e[:A]=np.linspace(0,1,A)
    if Rr: e[-Rr:]*=np.linspace(1,0,Rr)
    return e
from scipy.signal import lfilter, fftconvolve
def lp(x,c):
    a=np.exp(-2*np.pi*c/SR); return lfilter([1-a],[1,-a],x)
def lpf(x,c,n=2):
    for _ in range(n): x=lp(x,c)
    return x
def hp(x,c): return x-lpf(x,c,1)
def bp(x,lo,hi): return hp(lpf(x,hi),lo)
def verb(x,dec=1.2,mix=.35):
    n=int(dec*SR); ir=rng.normal(0,1,n)*np.exp(-np.linspace(0,7,n)); ir=lpf(ir,3000,1); ir/=np.abs(ir).sum()**.5*8
    y=fftconvolve(x,ir)[:len(x)+n]; out=np.zeros(len(y)); out[:len(x)]=x*(1-mix); return out+y*mix
def norm(x,p=.9): return x/(np.abs(x).max()+1e-9)*p
def thud(f=70,d=.45):
    tt=t(d); x=np.sin(2*np.pi*f*tt*(1-0.25*tt))*np.exp(-tt*9)+lpf(rng.normal(0,1,len(tt)),900)*np.exp(-tt*40)*1.6
    return x
def knock3():
    out=np.zeros(int(2.6*SR))
    for k,o in enumerate([0,.62,1.24]): s=thud(68-k*3); i=int(o*SR); out[i:i+len(s)]+=s
    return norm(verb(out,1.4,.4),.95)
def wind(d=6):
    n=rng.normal(0,1,int(d*SR)); x=lpf(n,500); lfo=.6+.4*np.sin(2*np.pi*t(d)*.23+1)*np.sin(2*np.pi*t(d)*.07)
    whist=bp(n,700,1100)*0.35*(0.5+0.5*np.sin(2*np.pi*t(d)*.4))
    return norm((x+whist)*lfo*env(len(n),1.2,1.5),.8)
def click():
    x=np.zeros(int(.6*SR)); x[:60]=rng.normal(0,1,60); x[60:]+=bp(rng.normal(0,.25,len(x)-60),800,3000)*np.exp(-t(.6)[60:]*6)
    return norm(x,.6)
def static_long(d=3.0):
    n=bp(rng.normal(0,1,int(d*SR)),500,3500); crack=(rng.random(len(n))>.9985)*rng.normal(0,4,len(n))
    return norm((n+crack)*env(len(n),.05,.6),.7)
def gen_hum(d=4,stall=False):
    tt=t(d); f=50
    x=sum(np.sin(2*np.pi*f*h*tt)/h**1.2 for h in range(1,9))+lpf(rng.normal(0,.6,len(tt)),400)
    x*=1+.25*np.sin(2*np.pi*12.5*tt)
    if stall:
        e=np.ones(len(tt)); 
        for c in (1.2,2.4,3.4): i=int(c*SR); e[i:i+int(.35*SR)]*=np.linspace(.1,1,int(.35*SR))
        x*=e
    return norm(x*env(len(tt),.4,.6),.6)
def stall():
    a=gen_hum(4.5,True); 
    for o in (3.0,3.6,4.2):
        s=thud(55,.5)*1.4; i=int(o*SR); a[i:i+len(s)]+=s[:len(a)-i]
    return norm(a,.9)
def gen_off():
    tt=t(3); f=50*np.exp(-tt*.7); ph=2*np.pi*np.cumsum(f)/SR
    x=sum(np.sin(h*ph)/h for h in range(1,7))*np.exp(-tt*1.4)
    return norm(x,.6)
def alarm(d=4):
    tt=t(d); sq=np.sign(np.sin(2*np.pi*3100*tt)); gate=((tt*4)%1)<.55
    return norm(lpf(sq*gate,6000,1)*env(len(tt),.01,.2),.42)
def heli(d=5):
    tt=t(d); n=lpf(rng.normal(0,1,len(tt)),700); am=(np.sin(2*np.pi*17*tt)>.6).astype(float); am=lpf(am,120,1)
    return norm(n*(0.3+am)*env(len(tt),1.5,1.8),.7)
def door():
    tt=t(2.2); f=180+90*np.sin(2*np.pi*.8*tt); ph=2*np.pi*np.cumsum(f)/SR
    cr=np.sign(np.sin(ph))*np.exp(-tt*1.5)*.15; wh=lpf(rng.normal(0,1,len(tt)),1200)*np.clip(tt-.5,0,1)*env(len(tt),.1,.8)
    return norm(lpf(cr,2500)+wh,.7)
def crunches(n=6,gap=.5,f=2500):
    out=np.zeros(int((n*gap+.6)*SR))
    for k in range(n):
        s=bp(rng.normal(0,1,int(.25*SR)),400,f)*np.exp(-t(.25)*14); i=int(k*gap*SR+rng.uniform(0,.08)*SR); out[i:i+len(s)]+=s
    return norm(out,.6)
def hit():
    tt=t(2.5); x=np.sin(2*np.pi*42*tt)*np.exp(-tt*2.2)+lpf(rng.normal(0,1,len(tt)),300)*np.exp(-tt*5)*.8
    return norm(verb(x,2,.5),.85)
def pencil(): return norm(crunches(5,.32,6000)*.6,.4)
def steps(): return norm(sum(np.pad(thud(110,.3)*.5,(int(k*.55*SR),0))[:int(2.6*SR)] if True else 0 for k in range(4)) if False else crunches(4,.55,1500),.5)
SFX=dict(knock3=knock3,wind=lambda:wind(7),click=click,static_long=static_long,gen=lambda:gen_hum(4),stall=stall,gen_off=gen_off,
         alarm=alarm,heli=heli,door=door,shovel=lambda:crunches(7,.55,3000),hit=hit,pencil=pencil,steps=steps)
VOL=dict(knock3=1.0,wind=.45,click=.5,static_long=.55,gen=.35,stall=.7,gen_off=.4,alarm=.4,heli=.45,door=.5,shovel=.5,hit=.55,pencil=.35,steps=.4)
def pad(d,chord=(110,130.81,164.81),bright=False):
    tt=t(d); x=np.zeros(len(tt))
    for k,f in enumerate(chord):
        for det in (-.6,.6): x+=np.sin(2*np.pi*(f+det)*tt+k)*(0.5+0.5*np.sin(2*np.pi*(0.05+0.02*k)*tt+k))
    if bright: x+=0.3*np.sin(2*np.pi*chord[-1]*2*tt)*(0.5+0.5*np.sin(2*np.pi*.03*tt))
    x+=0.4*lpf(rng.normal(0,1,len(tt)),180)
    return norm(lpf(x,900),.5)
def radio_fx(x):
    y=bp(x,320,3200); y=np.tanh(y*3)/3; y+=bp(rng.normal(0,.012,len(y)),800,3000)
    return norm(y,.85)
