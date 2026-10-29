"""Upload long + short for the next due, approved episode in queue.json.
Secrets (GitHub Actions -> Settings -> Secrets): YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN
Variable PUBLISH_PRIVACY: public (default) | unlisted | private
"""
import json, os, sys, datetime
ROOT=os.path.dirname(os.path.abspath(__file__))
def yt():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    c=Credentials(None,refresh_token=os.environ['YT_REFRESH_TOKEN'],client_id=os.environ['YT_CLIENT_ID'],
                  client_secret=os.environ['YT_CLIENT_SECRET'],token_uri='https://oauth2.googleapis.com/token',
                  scopes=['https://www.googleapis.com/auth/youtube.upload','https://www.googleapis.com/auth/youtube.force-ssl'])
    return build('youtube','v3',credentials=c)
from_http=None
def MediaFileUpload(*a,**k):
    from googleapiclient.http import MediaFileUpload as M; return M(*a,**k)
def upload(y,path,title,desc,tags,privacy,short=False):
    body={'snippet':{'title':title[:100],'description':desc,'tags':tags,'categoryId':'24','defaultLanguage':'en','defaultAudioLanguage':'en'},
          'status':{'privacyStatus':privacy,'selfDeclaredMadeForKids':False,'containsSyntheticMedia':False}}
    r=y.videos().insert(part='snippet,status',body=body,media_body=MediaFileUpload(path,chunksize=-1,resumable=True)).execute()
    print('uploaded',path,r['id'],r['status']['privacyStatus']); return r['id']
def due():
    q=json.load(open(os.path.join(ROOT,'queue.json'))); today=datetime.date.today().isoformat()
    for e in q:
        if e.get('approved',True) and e['publish_date']<=today and not e['long_video_id']: return q,e
    return q,None
if __name__=='__main__':
    mode=sys.argv[1]
    q,e=due()
    if mode=='next':
        print(e['episode'] if e else ''); sys.exit(0)
    if not e: print('nothing due'); sys.exit(0)
    out=os.path.join(ROOT,'work',e['episode'],'out'); m=json.load(open(os.path.join(ROOT,'episodes',e['episode'],'meta.json')))
    priv=os.environ.get('PUBLISH_PRIVACY','public') or 'public'
    y=yt()
    e['long_video_id']=upload(y,f'{out}/long.mp4',m['title'],m['description'],m['tags'],priv)
    try:
        y.captions().insert(part='snippet',body={'snippet':{'videoId':e['long_video_id'],'language':'en','name':'English'}},
                            media_body=MediaFileUpload(f'{out}/long.en.srt')).execute(); print('captions ok')
    except Exception as x: print('captions skipped:',x)
    try:
        y.thumbnails().set(videoId=e['long_video_id'],media_body=MediaFileUpload(f'{out}/thumbnail.jpg')).execute(); print('thumbnail ok')
    except Exception as x: print('thumbnail skipped (channel may need phone verification):',x)
    s=m['short']; e['short_video_id']=upload(y,f'{out}/short.mp4',s['title'],s['description']+f"\nFull video: https://youtu.be/{e['long_video_id']}",m['tags'],priv,True)
    json.dump(q,open(os.path.join(ROOT,'queue.json'),'w'),indent=2)
