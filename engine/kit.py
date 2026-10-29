"""Scene kit: draws any shot from a JSON spec, in the channel's house style.
Kinds: exterior, interior, character, closeup, page, info. Optional "tint":"red" for reinterpretation reprises."""
import random, math
from artlib import *
from scenes_ep1_lib import mountains, station, page as _page, clock as _clock, paperbg, nightsky, snowfall
SKY={'night':('#20262E','#2C3540'),'dusk':('#2F3A48','#8A7A60'),'day':('#9FB0BE','#D7D9CF')}
def _sky(t): c1,c2=SKY.get(t,SKY['night']); return grad('sky',c1,c2),'<rect width="1920" height="1080" fill="url(#sky)"/>'
def terrain(setting,t):
    dark=t=='night'; o=''
    if setting=='mountain': o+=mountains('#3E4C5C' if dark else '#7F8F9C','#33404D' if dark else '#97A4AE')
    elif setting=='forest':
        r=random.Random(5)
        for k in range(40):
            x=r.uniform(-50,1970); h=r.uniform(180,380); y=r.uniform(700,820)
            o+=poly([(x,y-h),(x+70,y),(x-70,y)],'#2F3B33' if dark else P['ggD'],sw=4)
        o+=rect(0,820,1920,260,'#2A332D' if dark else '#8C9A7E',sw=0)
    elif setting=='coast':
        o+=rect(0,700,1920,380,'#2B3A4A' if dark else P['blue'],sw=0)+''.join(f'<path d="M{x},{760+(x%3)*60} q40,-20 80,0" fill="none" stroke="#B9C6CF" stroke-width="5" opacity=".6"/>' for x in range(0,1920,170))
        o+=poly([(0,860),(700,780),(1000,1080),(0,1080)],'#4A4740' if dark else '#9C8F78',sw=5)
    elif setting=='desert':
        o+=f'<path d="M0,800 Q500,690 1000,790 T1920,760 L1920,1080 L0,1080 Z" fill="{"#5A4E3E" if dark else "#C9B48A"}" stroke="{P["ch"]}" stroke-width="5"/>'
    elif setting=='city':
        r=random.Random(9)
        for k in range(16):
            x=k*125; h=r.uniform(250,600); o+=rect(x,820-h,115,h,'#2B3038' if dark else '#8E959C',sw=5)
            o+=''.join(rect(x+20+j*40,840-h+i*70,22,30,P['yel'] if (dark and r.random()<.35) else ('#1F2329' if dark else '#B8C2C8'),sw=0) for i in range(int(h/80)) for j in range(2))
        o+=rect(0,820,1920,260,'#26292E' if dark else '#7A7C7E',sw=0)
    else: o+=rect(0,800,1920,280,'#3B443A' if dark else '#A3A98E',sw=0)
    return o
def weather(w):
    if w=='snow': return snowfall(220,2,slant=4)
    if w=='storm': return snowfall(320,3,slant=8,op=.9)
    if w=='rain': return snowfall(260,4,col='#9FB3C2',slant=3,op=.7)
    if w=='fog': return ''.join(rect(-50,y,2020,70,'#D8DCDC',sw=0,op=.18) for y in range(300,1000,110))
    return ''
def building(kind,lit=True,night=True):
    if kind=='none': return ''
    if kind=='tower':
        o=rect(860,260,200,560,'#B9B3A6' if not night else '#7A766E',sw=7)+rect(830,200,260,70,P['ch'],sw=6)+rect(880,140,160,70,P['yel'] if lit else '#3A4048',sw=6)
        if lit and night: o+=poly([(1040,170),(1920,60),(1920,300)],P['yelL'],sw=0,op=.18)
        return o+rect(930,700,60,120,P['brownD'],sw=5)
    if kind=='house':
        return f'<g transform="translate(700,560)">'+rect(0,0,520,260,'#8C8070' if not night else '#6F665C',sw=7)+poly([(-30,0),(260,-170),(550,0)],P['brownD'],sw=7)+rect(60,90,90,170,P['brown'],sw=6)+rect(260,80,120,90,P['yel'] if lit else '#3A4048',sw=6)+'</g>'
    return station(700,560,lit=lit,night=night)
def fig_spec(f):
    if not f: return ''
    P_={'stand':dict(),'walk':dict(arms=((25,-10),(-25,10)),legs=((20,10),(-25,10))),'sit':dict(sit=True,arms=((30,-30),(25,-40))),
        'point':dict(arms=((15,-10),(-95,0))),'hold_head':dict(sit=True,arms=((-150,-30),(150,30))),'arms_up':dict(arms=((-150,30),(150,-30))),
        'crouch':dict(legs=((70,-120),(60,-110)),arms=((40,-60),(-30,-60))),'reach':dict(arms=((20,-10),(-80,-5)))}
    kw=P_.get(f.get('pose','stand'),{})
    who=f.get('who','you'); who={'ally':'ruth','stranger':'hal'}.get(who,'you') if who!='you' else 'you'
    x=f.get('x',960); y=860 if kw.get('sit') else 1000
    return figure(x,y,f.get('scale',1.8),who=who,expr=f.get('expr','neutral'),look=f.get('look',0),**kw)
PROPS={}
def prop(fn): PROPS[fn.__name__]=fn; return fn
@prop
def desk(x): return rect(x-220,700,440,36,P['brown'],sw=6)+line(x-190,736,x-190,900,9)+line(x+190,736,x+190,900,9)
@prop
def radio(x): return desk(x)+rect(x-150,560,260,140,P['ggD'],sw=6)+''.join(circ(x-110+i*60,650,18,P['beige'],sw=4) for i in range(4))+rect(x-130,575,220,40,'#2A3A2E',sw=4)
@prop
def bed(x): return rect(x-300,760,600,90,P['brownD'],sw=7)+f'<path d="M{x-290},750 Q{x},720 {x+290},750 L{x+290},780 L{x-290},780 Z" fill="{P["gg"]}" stroke="{P["ch"]}" stroke-width="6"/>'
@prop
def door(x): return rect(x-110,380,220,520,'#4A4E52',sw=8)+ell(x+70,650,12,12,P['steel'],P['ch'],4)+rect(x-50,430,100,80,'#101315',sw=5)
@prop
def window(x): return rect(x-150,220,300,240,'#1F2630',sw=8)+line(x,220,x,460,6)+line(x-150,340,x+150,340,6)
@prop
def shelf(x): return rect(x-160,420,320,24,P['brown'],sw=5)+rect(x-160,560,320,24,P['brown'],sw=5)+''.join(rect(x-140+i*70,350+j*140,50,70,[P['red'],P['gg'],P['yel'],P['blue']][(i+j)%4],sw=4) for i in range(4) for j in range(2))
@prop
def generator(x): return rect(x-200,600,400,300,P['gen'],sw=8)+rect(x-170,650,150,100,'#2E3A30',sw=5)+''.join(line(x+10,640+i*30,x+180,640+i*30,6,P['ch'],.6,0) for i in range(7))+line(x+120,600,x+120,420,18,P['steel'])
@prop
def stove(x): return rect(x-150,640,300,260,'#6A5F52',sw=7)+''.join(circ(x-70+i*140,640,30,P['ch'],sw=4) for i in range(2))
@prop
def sink(x): return rect(x-180,680,360,220,'#B9BDBC',sw=7)+pl([(x,680),(x,560),(x+80,560)],18,P['steel'])
@prop
def table(x): return rect(x-200,720,400,30,P['brown'],sw=6)+line(x-170,750,x-170,900,9)+line(x+170,750,x+170,900,9)
@prop
def crate(x): return rect(x-110,700,220,200,'#9A7A55',sw=7)+line(x-110,700,x+110,900,5)+line(x+110,700,x-110,900,5)
@prop
def lamp(x): return line(x,0,x,250,4)+circ(x,280,30,P['yelL'],sw=5)
@prop
def phone(x): return desk(x)+rect(x-50,560,100,140,'#2A2C2F',sw=6)+rect(x-38,575,76,100,'#3E5560',sw=3)
@prop
def locker(x): return rect(x-120,330,240,570,'#6E7A80',sw=7)+line(x,330,x,900,5)+''.join(line(x-90,370+i*20,x-30,370+i*20,4) for i in range(3))
def interior(s):
    light=s.get('light','dim'); bg={'dark':'#1E2227','dim':'#3A3D40','day':'#8C8574'}[light]
    o=f'<rect width="1920" height="1080" fill="{bg}"/>'+rect(0,900,1920,180,'#2B2B29' if light!='day' else '#6E675A',sw=0)
    props=s.get('props',[])[:4]; slots=[300,760,1220,1620][:len(props)] if len(props)<4 else [260,720,1200,1650]
    figx=(s.get('figure') or {}).get('x')
    for p,x in zip(props,slots):
        if p in PROPS: o+=PROPS[p](x)
    if s.get('figure'):
        f=dict(s['figure'])
        if f.get('pose') in ('sit','hold_head') and 'bed' in props and 'x' not in f: f['x']=slots[props.index('bed')]
        f.setdefault('x',960); o+=fig_spec(f)
    if s.get('effect')=='knock': o+=''.join(f'<path d="M{960-r},540 A{r},{r*.7} 0 0 1 {960+r},540" fill="none" stroke="{P["yelL"]}" stroke-width="6" opacity="{.6-k*.15}"/>' for k,r in enumerate((140,220,300)))
    return o
def exterior(s):
    t=s.get('time','night'); d,b=_sky(t); o=b
    if t=='night': r=random.Random(3); o+=''.join(ell(r.uniform(0,1920),r.uniform(0,450),2,2,P['yelL'],op=.6) for _ in range(80)) if s.get('weather','clear')=='clear' else ''
    o+=terrain(s.get('setting','field'),t)+building(s.get('building','hut'),s.get('lit',True),t=='night')
    if s.get('figure'): f=dict(s['figure']); f.setdefault('x',1450); f.setdefault('scale',1.4); o+=fig_spec(f)
    return o+weather(s.get('weather','clear')),d
def character(s):
    bg={'dark':'#22272D','day':'#8C8574','red':'#4A2622'}.get(s.get('bg','dark'),'#22272D')
    f=dict(s.get('figure',{})); f.setdefault('x',960); f.setdefault('scale',2.3)
    return f'<rect width="1920" height="1080" fill="{bg}"/>'+rect(0,900,1920,180,'#1A1D21',sw=0,op=.6)+fig_spec(f)
def closeup(s):
    obj=s.get('object','clock'); t=str(s.get('text',''))[:14]; st=s.get('state','normal')
    if obj=='clock': return None,_clock(t or '03:00')
    o='<rect width="1920" height="1080" fill="#2B2C2E"/>'
    if obj=='door':
        o+=rect(640,140,640,900,'#4A4E52',sw=10)+rect(860,240,200,150,'#0F1215',sw=8)+ell(1200,620,18,18,P['steel'],P['ch'],5)
        if s.get('effect','knock')=='knock': o+=''.join(f'<path d="M{960-r},560 A{r},{r*.7} 0 0 1 {960+r},560" fill="none" stroke="{P["yelL"]}" stroke-width="{9-2*k}" opacity="{.6-k*.15}"/>' for k,r in enumerate((140,220,300)))
    elif obj in('device','radio','phone'):
        col={'alarm':'#E06A55','off':'#5A5852','normal':'#9DB28E'}[st] if st in('alarm','off','normal') else '#9DB28E'
        body={'device':'#ECE8DE','radio':P['ggD'],'phone':'#6B6F74'}[obj]
        o+=rect(520,200,880,680,body,sw=10)+rect(620,380,680,240,'#1E2420',sw=8)+txt(960,560,t,140,col,ls=4)
        if obj=='radio': o+=''.join(circ(700+i*170,760,50,P['beige'],sw=6) for i in range(4))
        if s.get('label'): o+=txt(960,300,str(s['label'])[:24],56,P['ch'] if obj=='device' else P['yelL'])
        if st=='alarm' or s.get('effect') in('ring','knock'): o+=''.join(f'<path d="M{1440+i*60},{360-i*40} Q{1520+i*70},540 {1440+i*60},{720+i*40}" fill="none" stroke="{col}" stroke-width="10" opacity="{.8-i*.2}"/>' for i in range(3))
    else:  # sign / note on wall
        o+=rect(560,180,800,700,'#EDE6D2',sw=8)
        for i,l in enumerate((s.get('lines') or [t])[:5]): o+=txt(960,330+i*120,str(l)[:26],78,P['ch'],'Kalam')
    return None,o
def pagek(s):
    L=[(220,str(s.get('title','RULES'))[:20],100,'Kalam',P['ch'],0)]
    font='Kalam' if s.get('style','hand')=='hand' else 'Patrick Hand'; col=P['ch'] if font=='Kalam' else P['blueD']
    for i,l in enumerate(s.get('lines',[])[:6]): L.append((360+i*130,str(l)[:44],70,font,col,-1 if font=='Kalam' else 0))
    return _page(L,hole=(1580,170) if s.get('hole') else None)
def info(s):
    t=s.get('type','equation'); o=paperbg()
    if t=='equation':
        o+=rect(220,280,400,500,P['gg'],sw=8)+txt(420,560,str(s.get('a',''))[:8],110,P['beigeL'])+txt(960,470,str(s.get('op',''))[:16],80)+pl([(780,560),(1140,560)],10)+pl([(1110,530),(1145,560),(1110,590)],10)+txt(1500,600,str(s.get('result',''))[:10],150,P['brownD'])
    elif t=='bars':
        it=s.get('items',[])[:7]; mx=max([abs(float(i.get('value',1))) for i in it]+[1])
        o+=txt(960,170,str(s.get('title',''))[:28],90)+line(220,300,1700,300,6)
        for k,i in enumerate(it):
            x=280+k*200; h=abs(float(i.get('value',0)))/mx*520
            o+=rect(x,300,120,h,P['blueD'] if i.get('highlight') else P['blue'],sw=6)+txt(x+60,270,str(i.get('label',''))[:10],38,P['brownD'])+txt(x+60,300+h+60,str(i.get('value',''))[:8],46)
    elif t=='flow':
        it=s.get('items',[])[:4]; n=len(it) or 1
        for k,lab in enumerate(it):
            x=260+k*(1400/max(n-1,1)) if n>1 else 960
            o+=rect(x-170,440,340,200,P['beigeL'],sw=7)+txt(x,560,str(lab)[:14],58)
            if k<n-1: o+=pl([(x+180,540),(x+1400/max(n-1,1)-180,540)],9)
        o+=txt(960,250,str(s.get('title',''))[:30],90)
    else:  # map
        rooms=s.get('rooms',['ROOM A','ROOM B','ROOM C'])[:4]
        o+=txt(960,190,str(s.get('title','MAP'))[:28],70,ls=4)+rect(260,300,700,380,'#E2D6BC',sw=8)
        for k,rn in enumerate(rooms):
            x=260+(k%2)*350; y=300+(k//2)*190; o+=rect(x,y,350,190,'none',sw=5)+txt(x+175,y+110,str(rn)[:12],44)
        o+=rect(200,560,60,90,P['brown'],sw=5)+txt(130,620,'DOOR',40)
        if s.get('path_label'):
            o+=pl([(200,620),(150,620),(150,820),(1490,820)],7,P['brown'],1,'22 14')+txt(820,880,str(s['path_label'])[:26],42,P['brownD'])+circ(1560,820,70,'#D4C8AA',sw=6)+txt(1560,935,str(s.get('target','')).upper()[:14],40)
    return o
def render(spec):
    k=spec.get('kind'); d=''
    if k=='exterior': body,d=exterior(spec)
    elif k=='interior': body=interior(spec)
    elif k=='character': body=character(spec)
    elif k=='closeup':
        d,full=closeup(spec)
        if d is None and full.startswith('<svg'): return full
        body=full
    elif k=='page': body=pagek(spec)
    elif k=='info': body=info(spec)
    else: body='<rect width="1920" height="1080" fill="#1E2126"/>'
    return svg(body,d or '')
