"""Validate an AI-written episode JSON and turn it into episodes/<slug>/ (story.py, scenes.py, meta.json, thumbnail)."""
import json, re, os, hashlib
KINDS={'exterior','interior','character','closeup','page','info'}
MOVES={'zin','zout','zin_fast','zin_slow','pl','pr','pu','pd','still','shake'}
SFX={'knock3','wind','click','static_long','gen','stall','gen_off','alarm','heli','door','shovel','hit','pencil','steps'}
def validate(ep):
    err=[]
    for k in ('title','premise','segments','short','description','tags'):
        if k not in ep: err.append('missing '+k)
    if err: return err
    segs=ep['segments']; words=sum(len(s.get('text','').split()) for s in segs if s.get('voice')!='C')
    if not 1050<=words<=1650: err.append(f'narration words {words} (need 1100-1600)')
    if not 70<=len(segs)<=170: err.append(f'segments {len(segs)} (need 80-160)')
    if sum(1 for s in segs if s.get('voice')=='C')<4: err.append('need >=4 title cards (voice C)')
    for i,s in enumerate(segs):
        if s.get('voice') not in ('N','R','C'): err.append(f'seg {i} bad voice')
        if s.get('voice')!='C':
            if not s.get('text'): err.append(f'seg {i} empty text')
            sh=s.get('shot') or {}
            if sh.get('kind') not in KINDS: err.append(f'seg {i} bad shot kind {sh.get("kind")}')
        if s.get('move','still') not in MOVES: s['move']='still'
        if s.get('sfx') and s['sfx'].split('@')[0] not in SFX: s['sfx']=None
    r=ep['short'].get('ranges',[])
    if not r or any(not(0<=a<=b<len(segs)) for a,b in r): err.append('short.ranges invalid')
    return err
def write(ep,root,slug):
    d=os.path.join(root,'episodes',slug); os.makedirs(d,exist_ok=True)
    specs={}; S=[]
    for s in ep['segments']:
        ex={}
        for k in ('hud','cap','sfx','pause'):
            if s.get(k) not in (None,''): ex[k]=s[k]
        if s['voice']=='C':
            ex['dur']=float(s.get('dur',2.0)); ex['sub']=s.get('sub',''); ex.setdefault('sfx','hit')
            S.append(('C',s.get('text','')[:22].upper(),'card',ex)); continue
        sh=s['shot']; key='k'+hashlib.md5(json.dumps(sh,sort_keys=True).encode()).hexdigest()[:10]
        specs[key]=sh; S.append((s['voice'],s['text'],f"{key}:{s.get('move','still')}",ex))
    S.append(('N','Subscribe for more stories.','end_card:still',dict(pause=2.0)))
    specs['end_card']={'kind':'endcard'}
    open(os.path.join(d,'story.py'),'w').write('TITLE='+json.dumps(ep['title'])+'\nS='+json.dumps(S,indent=0).replace('true','True').replace('false','False').replace('null','None')+'\n')
    open(os.path.join(d,'scenes.py'),'w').write('import json, kit\nfrom scenes_ep1_lib import endcard, card\nSPECS=json.loads('+repr(json.dumps(specs))+')\nD={k:(lambda k=k:(endcard() if SPECS[k].get("kind")=="endcard" else kit.render(SPECS[k]))) for k in SPECS}\nRED={k for k,v in SPECS.items() if v.get("tint")=="red"}\n')
    sh=ep['short']; meta={'title':ep['title'][:100],'description':ep['description']+'\n\nAn original animated survival mystery from Rules Left Behind.','tags':ep['tags'][:15],'premise':ep['premise'],'thumb':ep.get('thumb',{}),
          'short':{'ranges':sh['ranges'],'hook':sh.get('hook','')[:40].upper(),'title':(sh.get('title') or ep['title'])[:90]+' #shorts','description':sh.get('description','')+'\nFull story on the channel: Rules Left Behind.\n#shorts #survival #mystery'}}
    json.dump(meta,open(os.path.join(d,'meta.json'),'w'),indent=2)
    return d
