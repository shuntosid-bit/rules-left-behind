"""Ask Gemini (free tier) to write today's episode, self-review it, validate, and add it to queue.json.
Env: GEMINI_API_KEY (GitHub Secret), GEMINI_MODEL (optional, default gemini-flash-latest)."""
import json, os, sys, re, datetime, urllib.request
sys.path.insert(0,os.path.dirname(__file__))
from episode_io import validate, write
import kit
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL=os.environ.get('GEMINI_MODEL') or 'gemini-flash-latest'
def gemini(prompt,temp=1.0):
    url=f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent'
    body={'contents':[{'parts':[{'text':prompt}]}],'generationConfig':{'temperature':temp,'responseMimeType':'application/json','maxOutputTokens':32000}}
    req=urllib.request.Request(url,json.dumps(body).encode(),{'Content-Type':'application/json','x-goog-api-key':os.environ['GEMINI_API_KEY']})
    r=json.load(urllib.request.urlopen(req,timeout=300)); t=r['candidates'][0]['content']['parts'][0]['text']
    return json.loads(re.sub(r'^```json|```$','',t.strip()))
SPEC=open(os.path.join(os.path.dirname(__file__),'story_spec.md')).read()
def main():
    q=json.load(open(os.path.join(ROOT,'queue.json')))
    past=[json.load(open(os.path.join(ROOT,'episodes',e['episode'],'meta.json'))).get('premise',e['episode']) for e in q if os.path.exists(os.path.join(ROOT,'episodes',e['episode'],'meta.json'))]
    prompt=SPEC.replace('{PAST}','\n'.join('- '+p for p in past[-60:]) or '- (none)').replace('{PROPS}',', '.join(sorted(kit.PROPS)))
    ep=None; last_err=[]
    for attempt in range(4):
        cand=gemini(prompt+('\n\nYour previous attempt failed validation: '+'; '.join(last_err[:8]) if last_err else ''))
        rev=gemini(SPEC_REVIEW+'\n\nEPISODE JSON:\n'+json.dumps(cand),0.4)
        cand=rev.get('episode',rev)
        last_err=validate(cand)
        if not last_err: ep=cand; break
        print('attempt',attempt,'failed:',last_err[:5])
    if not ep: sys.exit('could not produce a valid episode')
    n=len(q)+1; slug=f"ep{n:03d}-"+re.sub(r'[^a-z0-9]+','-',ep['title'].lower())[:40].strip('-')
    write(ep,ROOT,slug)
    q.append({'episode':slug,'approved':True,'publish_date':datetime.date.today().isoformat(),'long_video_id':None,'short_video_id':None})
    json.dump(q,open(os.path.join(ROOT,'queue.json'),'w'),indent=2); print(slug)
SPEC_REVIEW="""You are a strict story editor. Review the episode JSON below for: plot holes, broken logic in the survival mechanics, a twist that is not set up by earlier clues, factual errors in real-world safety information, anything unsafe to imitate (never give dangerous instructions), gore, real people or brands, and similarity to the 'Nobody Gets In' channel (no zombies-in-a-building sieges, no copying). Fix every problem directly in the JSON while keeping the exact same schema and length rules. Return ONLY {"episode": <fixed episode JSON>}."""
if __name__=='__main__': main()
