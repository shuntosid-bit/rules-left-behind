import json, os, re, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
from story import S
k=Kokoro('models/kokoro-v1.0.onnx','models/voices-v1.0.bin')
N=0.65*k.get_voice_style('am_michael')+0.35*k.get_voice_style('am_fenrir')
R=0.8*k.get_voice_style('af_heart')+0.2*k.get_voice_style('af_bella')
os.makedirs('audio2',exist_ok=True); mp='audio2/meta.json'
meta=json.load(open(mp)) if os.path.exists(mp) else {}
def fix(t): return t.replace('three oh seven','three-oh-seven').replace(' A M.',' a.m.').replace('...',', ')
for i,(v,t,sh,ex) in enumerate(S):
    if v=='C' or str(i) in meta: continue
    w=len(t.split())
    sp=(0.86 if w<=6 else 0.92 if w<=14 else 0.97) if v=='N' else 1.02
    a,sr=k.create(fix(t),voice=N if v=='N' else R,speed=sp,lang='en-us')
    idx=np.where(np.abs(a)>0.01)[0]; a=a[max(idx[0]-240,0):idx[-1]+2400]
    sf.write(f'audio2/seg{i:03d}.wav',a,sr); meta[str(i)]=len(a)/sr; json.dump(meta,open(mp,'w'))
print('TTSDONE')
