from artlib import *
import random
D={}
def sc(f): D[f.__name__]=f; return f
def nightsky(c1=P['night'],c2=P['night2']): return grad('sky',c1,c2), '<rect width="1920" height="1080" fill="url(#sky)"/>'
def mountains(col=P['blueD'],col2='#33404D',snowcap=True,base=820):
    o=poly([(0,base),(260,520),(470,700),(760,420),(1050,690),(1330,480),(1650,720),(1920,560),(1920,1080),(0,1080)],col2,sw=0)
    o+=poly([(0,base+60),(380,640),(700,820),(1100,600),(1500,830),(1920,700),(1920,1080),(0,1080)],col,sw=0)
    if snowcap: o+=poly([(760,420),(820,470),(790,480),(760,455),(720,485),(700,470)],P['snowS'],sw=0,op=.6)+poly([(1330,480),(1390,530),(1350,525),(1320,510),(1290,535)],P['snowS'],sw=0,op=.6)
    return o
def station(x,y,s=1,lit=True,drift=0,clearvent=False,smoke=False,night=True):
    o=''
    wall=P['concrete'] if not night else '#6F6C66'
    o+=rect(0,0,520,260,wall,sw=7)
    o+=rect(-10,-22,540,26,P['snow'],sw=6)
    o+=rect(60,90,90,170,P['brownD'],sw=6)+ell(135,180,6,6,P['yel'])  # door
    o+=rect(230,80,120,90,P['yel'] if lit else '#3A4048',sw=6)+line(290,80,290,170,4)+line(230,125,350,125,4)
    o+=line(420,-22,420,-360,8)+line(420,-360,380,-22,3,op=.6)+line(420,-360,470,-22,3,op=.6)+line(395,-250,445,-250,5)+line(400,-150,440,-150,5)
    o+=ell(420,-366,8,8,P['red'])
    o+=rect(520,150,46,22,P['steel'],sw=5)  # vent pipe north wall
    if smoke: o+=''.join(ell(600+i*28,140-i*30,18+i*6,14+i*4,'#B9B6AE',op=.55-.1*i) for i in range(4))
    if clearvent: o+=''.join(rect(560+j*0,100+k*0,0,0,'none') for j in range(0) for k in range(0))+rect(540,190,110,70,P['snow'],P['snowS'],5)+rect(540,110,110,40,P['snow'],P['snowS'],5)+rect(620,150,30,40,P['snow'],P['snowS'],5)
    if drift>0:
        h=[0,190,300][drift]
        o+=f'<path d="M{430},{262} Q{560},{262-h*.9} {760},{262-h} L{900},{262-h*.6} L{1000},262 Z" fill="{P["snow"]}" stroke="{P["snowS"]}" stroke-width="6"/>'
    o+=rect(-200,258,1300,40,P['snow'],sw=0)
    return f'<g transform="translate({x},{y}) scale({s})">{o}</g>'
def paperbg(c=P['paper']): return f'<rect width="1920" height="1080" fill="{c}"/>'+''.join(line(0,y,1920,y,2,'#B9AE96',.35,0) for y in range(120,1080,80))
def card_bg(): return '<rect width="1920" height="1080" fill="#1E2126"/>'
@sc
def ext_night():
    d,b=nightsky(); return svg(b+mountains()+station(700,560)+snowfall(220,2,slant=4),d)
@sc
def ext_calm():
    d,b=nightsky('#1C2430','#34404E'); r=random.Random(3)
    stars=''.join(ell(r.uniform(0,1920),r.uniform(0,500),r.uniform(1,3),r.uniform(1,3),P['yelL'],op=r.uniform(.3,.9)) for _ in range(140))
    return svg(b+stars+circ(1560,170,60,P['yelL'],sw=0)+mountains()+station(700,560,drift=1),d)
@sc
def ext_wide():
    d,b=nightsky('#2A3340','#4E5C6A')
    lights=''.join(ell(150+i*13%90,960+(i*7)%40,3,3,P['yelL'],op=.9) for i in range(18))
    return svg(b+mountains('#3E4C5C','#33404D',True,860)+lights+station(1150,440,.45)+snowfall(120,4,op=.5),d)
@sc
def heli_drop():
    d=grad('sky','#B7B4AA','#D8D2C2');b='<rect width="1920" height="1080" fill="url(#sky)"/>'
    h='<g transform="translate(1250,240)">'+ell(0,0,170,70,P['gg'],P['ch'],7)+rect(140,-20,330,30,P['gg'],sw=6)+rect(450,-60,30,80,P['gg'],sw=6)+rect(-80,-30,90,45,'#A8B4BC',sw=5)+line(-260,-90,260,-90,9)+line(0,-70,0,-90,9)+line(-120,70,120,70,7)+line(-80,50,-90,70,6)+line(80,50,90,70,6)+'</g>'
    bag=lambda hd:rect(hd[0]-30,hd[1]-10,70,40,P['ggD'],sw=5)
    return svg(b+mountains('#8C98A0','#A3ACB0',True,800)+station(250,600,night=False,lit=False)+h+''.join(line(1150+i*40,880,1230+i*55,800,4,P['snowS'],.7,6) for i in range(8))+figure(920,920,1.5,arms=((15,-10),(-25,20)),expr='neutral',look=1,hold=bag)+snowfall(80,5,op=.6),d)
@sc
def heli_day30():
    d=grad('sky','#9FB0BE','#D7D9CF');b='<rect width="1920" height="1080" fill="url(#sky)"/>'
    h='<g transform="translate(1500,230) scale(.25)">'+ell(0,0,170,70,P['gg'],P['ch'],10)+rect(140,-20,330,30,P['gg'],sw=8)+line(-260,-90,260,-90,12)+'</g>'
    return svg(b+circ(300,180,70,P['yelL'],sw=0,op=.9)+mountains('#7F8F9C','#97A4AE',True,820)+station(400,600,lit=False,clearvent=True,drift=1,night=False)+h+figure(1640,940,1.5,arms=((30,-20),(-150,10)),expr='smile',look=1),d)
@sc
def ending():
    d=grad('sky','#2F3A48','#C9A86A');b='<rect width="1920" height="1080" fill="url(#sky)"/>'
    return svg(b+mountains('#2E3946','#3A4756',True,840)+station(620,560,clearvent=True,smoke=True,drift=1),d)
@sc
def map():
    o=paperbg()
    o+=rect(260,300,560,360,'#E2D6BC',sw=8)+line(540,300,540,660,5)+line(260,480,540,480,5)
    o+=txt(400,410,'BUNK',44)+txt(400,590,'RADIO',44)+txt(680,500,'GENERATOR',40)
    o+=rect(200,540,60,90,P['brown'],sw=5)+txt(130,600,'DOOR',40)
    o+=rect(820,470,40,18,P['steel'],sw=4)
    o+=pl([(200,600),(150,600),(150,800),(1490,800)],7,P['brown'],1,'22 14')+txt(820,860,'ROPE LINE — 40 M',42,P['brownD'])
    o+=circ(1560,800,70,'#D4C8AA',sw=6)+line(1560,730,1560,870,5)+txt(1560,915,'INSTRUMENTS',40)
    o+=line(1750,180,1750,90,6)+pl([(1730,120),(1750,85),(1770,120)],6)+txt(1750,230,'N',56)
    o+=txt(960,190,'KESTREL RIDGE STATION',70,P['ch'],ls=4)
    return svg(o)
@sc
def field_noon():
    d=grad('sky','#B4B5AF','#D9D4C6');b='<rect width="1920" height="1080" fill="url(#sky)"/>'
    o=b+mountains('#8E9AA2','#A6AFB3',True,760)+rect(0,820,1920,260,P['snow'],sw=0)
    o+=rect(1250,520,190,150,'#ECE8DE',sw=7)+''.join(line(1260,540+i*24,1430,540+i*24,4,P['snowS'],1,0) for i in range(5))+line(1270,670,1260,830,7)+line(1420,670,1430,830,7)
    o+=line(1600,820,1600,330,8)+line(1560,330,1640,330,6)+''.join(circ(1560+80*i,330,16,P['steel'],sw=4) for i in range(2))
    o+=pl([(0,760),(600,830),(1040,885)],6,P['brown'])
    clip=lambda h:rect(h[0]-10,h[1]-40,50,62,P['beigeL'],sw=5)
    o+=figure(1100,900,1.7,arms=((10,-5),(-60,-70)),expr='relief',hold=clip)
    return svg(o,d)
def desk_room(dark=True):
    o=f'<rect width="1920" height="1080" fill="{"#3A3D40" if dark else "#8C8574"}"/>'
    o+=rect(1350,150,360,300,'#1F2630',sw=8)+line(1530,150,1530,450,6)+line(1350,300,1710,300,6)+snowfall(40,8,op=.7).replace('<path','<path transform="translate(0,0)"') if False else f'<rect width="1920" height="1080" fill="{"#3A3D40" if dark else "#8C8574"}"/>'+rect(1350,150,360,300,'#1F2630',sw=8)+line(1530,150,1530,450,6)+line(1350,300,1710,300,6)
    o+=rect(0,820,1920,260,'#2E2F31',sw=0)
    return o
@sc
def radiodesk():
    o=desk_room()
    o+=f'<circle cx="760" cy="420" r="420" fill="url(#lamp)"/>'
    o+=figure(1230,830,1.95,sit=True,arms=((40,-60),(-60,-50)),expr='focused',look=-1,headset=True)
    o+=rect(380,700,1100,40,P['brown'],sw=7)+line(430,740,430,1000,10)+line(1430,740,1430,1000,10)
    o+=rect(480,520,380,180,P['ggD'],sw=7)+''.join(circ(540+i*90,640,26,P['beige'],sw=5) for i in range(4))+rect(520,550,300,50,'#2A3A2E',sw=5)+txt(670,588,'BASE 4.140',38,P['yelL'])
    o+=rect(940,650,320,50,P['beigeL'],sw=5)+line(1100,650,1100,700,4)
    o+=line(900,700,880,560,6)+ell(880,550,20,14,P['ch'])
    return svg(o,rgrad('lamp',P['yel'],.35))
@sc
def radio():
    o='<rect width="1920" height="1080" fill="#33363A"/>'+rect(260,220,1400,640,P['ggD'],sw=10)
    o+=rect(340,300,700,200,'#24342A',sw=8)+txt(690,440,'BASE 4.140 MHZ',96,P['yelL'],ls=4)
    o+=''.join(circ(420+i*200,680,64,P['beige'],sw=7)+line(420+i*200,680,420+i*200+30,640,6) for i in range(4))
    o+=rect(1160,300,420,480,'#4A5548',sw=8)+''.join(line(1190,330+i*36,1550,330+i*36,8,P['ch'],.7,0) for i in range(13))
    o+=''.join(f'<path d="M{1640+i*50},{400-i*30} Q{1700+i*60},540 {1640+i*50},{680+i*30}" fill="none" stroke="{P["yelL"]}" stroke-width="7" opacity="{.7-i*.18}"/>' for i in range(3))
    return svg(o)
@sc
def ruth():
    o='<rect width="1920" height="1080" fill="#6B6458"/>'+f'<circle cx="900" cy="380" r="520" fill="url(#lamp)"/>'
    o+=rect(1250,140,480,330,'#2B3340',sw=8)+''.join(ell(1300+i*37%400,380+(i*13)%60,4,4,P['yelL']) for i in range(22))+line(1490,140,1490,470,6)
    o+=rect(180,170,500,330,P['beigeL'],sw=6)+pl([(220,420),(330,300),(420,380),(520,250),(640,330)],5,P['brown'])+ell(560,280,14,14,P['red'])+txt(430,220,'SECTOR 4',40)
    o+=rect(0,800,1920,280,'#4D4840',sw=0)+figure(860,890,2.0,who='ruth',sit=True,arms=((40,-70),(50,-80)),expr='worried',look=1,headset=True)
    o+=rect(300,760,1400,40,P['brown'],sw=7)+rect(1180,640,280,120,P['ggD'],sw=6)+''.join(circ(1230+i*60,720,18,P['beige'],sw=4) for i in range(4))+rect(560,720,120,40,'#E9E3D5',sw=4)+ell(520,740,30,22,P['brown'],P['ch'],4)
    return svg(o,rgrad('lamp',P['yelL'],.4))
@sc
def photo_hal():
    o='<rect width="1920" height="1080" fill="#8B7A62"/>'+''.join(ell(random.Random(i).uniform(0,1920),random.Random(i+50).uniform(0,1080),6,6,'#7A6A54',op=.6) for i in range(200))
    ph='<g transform="translate(960,540) rotate(-4)">'+rect(-330,-390,660,780,'#EFE9DC',sw=6)+rect(-280,-340,560,540,'#9AA8B2',sw=5)+mountains_small()+figure(0,160,1.0,who='hal',arms=((20,-10),(-25,20)),expr='smile')+txt(0,320,'HAL — KESTREL, MAY',70,P['ch'],'Patrick Hand')+'</g>'
    return svg(o+ph+circ(940,170,18,P['red'],sw=4))
def mountains_small(): return poly([(-280,60),(-150,-120),(-40,10),(90,-160),(280,40),(280,200),(-280,200)],'#7C8C98',sw=0)
def page(lines,hole=None,extra=''):
    o='<rect width="1920" height="1080" fill="#2C2E31"/>'+rect(150,50,1620,1000,'#EDE6D2',sw=6,a=1)
    o+=''.join(line(220,y,1700,y,2,'#9FB0BE',.6,0) for y in range(150,1040,70))+line(330,50,330,1050,3,P['red'],.6,0)
    if hole: o+=f'<path d="M{hole[0]-60},{hole[1]-8} l30,-22 l40,10 l35,-14 l15,30 l-30,22 l-50,-6 l-35,10 Z" fill="#2C2E31"/>'
    for (y,s,size,font,col,rot) in lines: o+=txt(370,y,s,size,col,font,'start',rot)
    return o+extra
@sc
def logrules():
    L=[(260,'RULES',110,'Kalam',P['ch'],0),(410,'1. Keep the door shut at night.',84,'Kalam',P['ch'],-1),(570,'2. If you hear knocking, DO NOT ANSWER.',74,'Kalam',P['ch'],-1.5),(730,'3. Keep the radio on.',84,'Kalam',P['ch'],-1)]
    return svg(page(L,hole=(1520,655))+line(370,600,1500,592,7,P['ch'],.8,2)+line(370,615,1500,606,4,P['ch'],.5,2))
@sc
def newrules():
    L=[(170,'RULES',66,'Kalam',P['ch'],0),(250,'1. Keep the door shut at night.',52,'Kalam',P['ch'],-1),(330,'2. If you hear knocking, DO NOT ANSWER.',52,'Kalam',P['ch'],-1.5),(410,'3. Keep the radio on.',52,'Kalam',P['ch'],-1),
       (530,'— New rules —',60,'Patrick Hand',P['blueD'],0),(650,'1. Keep the door shut at night. But keep the vent clear.',62,'Patrick Hand',P['blueD'],0),(790,'2. If you hear knocking, check the generator.',62,'Patrick Hand',P['blueD'],0),(930,'3. Keep the radio on. Trust the alarm, not the logbook.',62,'Patrick Hand',P['blueD'],0)]
    return svg(page(L,hole=(1640,300)))
@sc
def margins():
    o='<rect width="1920" height="1080" fill="#2C2E31"/>'+rect(120,60,820,960,'#EDE6D2',sw=6,a=1)+rect(980,60,820,960,'#E8E0CA',sw=6,a=1)
    o+=''.join(line(170,y,900,y,2,'#9FB0BE',.5,0)+line(1030,y,1760,y,2,'#9FB0BE',.5,0) for y in range(200,1000,90))
    o+=rect(150,120,1620,860,'none',sw=0)+txt(170,330,'WK1  Quiet up here. Good coffee.',56,P['blueD'],'Patrick Hand','start',0)
    o+=txt(170,600,'WK2  Headache again. Altitude.',58,P['blueD'],'Patrick Hand','start',-3)
    o+=txt(1010,430,'WK3  They knock at 3.',62,P['ch'],'Kalam','start',-7)+txt(1080,520,"I don't answer.",62,P['ch'],'Kalam','start',-9)
    o+=txt(1160,820,'so tired',70,P['ch'],'Kalam','start',-14,.7)
    return svg(o)
def clock(t):
    o='<rect width="1920" height="1080" fill="#15181C"/>'+f'<circle cx="960" cy="560" r="560" fill="url(#g)"/>'
    o+=rect(560,420,800,320,'#2A2C2F',sw=9)+rect(620,470,680,220,'#191A1B',sw=6)+txt(960,660,t,220,P['yel'],ls=12)
    o+=rect(420,740,1080,60,P['brownD'],sw=7)
    return svg(o,rgrad('g',P['yel'],.22))
for t in ['03:07','03:04','03:11','03:02']: D['clock'+t.replace(':','')[1:] if False else 'clock'+t.replace(':','').lstrip('0')]=(lambda t=t:clock(t))
@sc
def knockdoor():
    o='<rect width="1920" height="1080" fill="#1E2227"/>'+rect(640,140,640,900,'#4A4E52',sw=10)+rect(860,240,200,150,'#0F1215',sw=8)+ell(1200,620,18,18,P['steel'],P['ch'],5)+line(640,1040,1280,1040,6,P['yel'],.25,0)
    for i,r in enumerate([140,220,300]): o+=f'<path d="M{960-r},{560} A{r},{r*.7} 0 0 1 {960+r},{560}" fill="none" stroke="{P["yelL"]}" stroke-width="{9-2*i}" opacity="{.6-i*.15}"/>'
    return svg(o)
@sc
def bed():
    o='<rect width="1920" height="1080" fill="#22272D"/>'+rect(1380,180,240,200,'#3C4A58',sw=8)+f'<path d="M1380,380 L1620,380 L1200,1000 L700,1000 Z" fill="#3C4A58" opacity=".35"/>'
    o+=rect(500,720,1000,120,P['brownD'],sw=8)+rect(470,600,60,300,P['brownD'],sw=7)
    o+=figure(900,860,2.1,sit=True,arms=((30,-30),(25,-40)),expr='scared',look=-1)
    o+=f'<path d="M560,760 Q900,690 1460,760 L1480,800 L540,800 Z" fill="{P["gg"]}" stroke="{P["ch"]}" stroke-width="7"/>'
    return svg(o)
@sc
def window_temp():
    o='<rect width="1920" height="1080" fill="#5A574F"/>'+rect(420,140,1080,780,'#2B3542',sw=12)+snowfall(160,9,slant=5).replace('opacity','opacity')
    o+=line(960,140,960,920,10)+line(420,530,1500,530,10)
    o+=rect(1100,240,90,420,'#ECE8DE',sw=6)+line(1145,280,1145,600,14,P['blueD'],1,0)+ell(1145,620,26,26,P['blueD'],P['ch'],5)+txt(1260,520,'-25',90,P['yelL'])
    o+=''.join(f'<path d="M{420+i*40},{920} q20,-40 40,0" fill="none" stroke="#DDE3E6" stroke-width="5" opacity=".7"/>' for i in range(27))
    return svg(o)
def genroom_base(stall=False,who=True):
    o='<rect width="1920" height="1080" fill="#3B3A36"/>'+f'<circle cx="900" cy="200" r="600" fill="url(#bulb)"/>'+line(900,0,900,150,4)+circ(900,175,26,P['yelL'],sw=4)
    o+=rect(0,860,1920,220,'#2B2B29',sw=0)
    o+=rect(420,500,640,360,P['gen'],sw=9)+rect(470,560,220,140,'#2E3A30',sw=6)+''.join(circ(520+i*60,780,18,P['beige'],sw=4) for i in range(3))+''.join(line(760,540+i*30,1020,540+i*30,6,P['ch'],.6,0) for i in range(9))
    o+=pl([(1000,500),(1000,330),(1880,330)],22,P['steel'])+pl([(1000,500),(1000,330),(1880,330)],22,P['ch'],.25)
    o+=rect(1860,250,60,160,'#555149',sw=6)
    o+=rect(1180,560,300,300,'#6E7568',sw=8)+rect(1360,600,90,60,P['beigeL'],sw=4)+line(1405,650,1430,615,5,P['red'])
    o+=rect(240,320,110,130,'#ECE8DE',sw=6)+''.join(line(258,345+i*16,332,345+i*16,4,P['ch'],.5,0) for i in range(3))+txt(295,435,'CO ALARM',22,P['ch'])
    if stall:
        o+=''.join(f'<path d="M{400-i*30},{480+i*40} q-30,40 0,80" fill="none" stroke="{P["yelL"]}" stroke-width="7" opacity=".7"/>' for i in range(3))+''.join(f'<path d="M{1080+i*30},{480+i*40} q30,40 0,80" fill="none" stroke="{P["yelL"]}" stroke-width="7" opacity=".7"/>' for i in range(3))
        o+=''.join(ell(1000+r*1.3,320-r*0.4,40+r*.3,26+r*.2,'#8E8B84',op=.45) for r in range(0,240,60))+''.join(ell(1300+r,340+r*.2,30,22,'#8E8B84',op=.35) for r in range(0,400,90))
    return o
@sc
def genroom(): return svg(genroom_base(),rgrad('bulb',P['yelL'],.35))
@sc
def genstall():
    flash=lambda h:poly([(h[0],h[1]),(h[0]+40,h[1]-14),(h[0]+40,h[1]+14)],P['yelL'],sw=4)
    return svg(genroom_base(True)+figure(1640,1060,1.7,arms=((20,-10),(-80,-10)),expr='scared',look=-1,hold=flash),rgrad('bulb',P['yelL'],.35))
@sc
def fuel():
    o=paperbg()+rect(260,250,360,560,P['gg'],sw=8)+txt(440,580,'400 L',130,P['beigeL'])
    o+=txt(960,470,'÷ 12 L A DAY',90)+pl([(780,560),(1140,560)],10)+pl([(1110,530),(1145,560),(1110,590)],10)
    o+=txt(1500,600,'33 DAYS',170,P['brownD'])
    return svg(o)
@sc
def fuel_end():
    o=paperbg()+rect(760,220,400,620,P['gg'],sw=9)+rect(766,800,388,34,P['ggD'],sw=0)+txt(960,560,'17 L',170,P['ch'])
    return svg(o)
@sc
def sink():
    o='<rect width="1920" height="1080" fill="#5F6A70"/>'+rect(500,600,920,260,'#B9BDBC',sw=9)+rect(560,640,800,150,'#8E9494',sw=6)
    o+=pl([(960,600),(960,380),(1120,380)],26,P['steel'])+pl([(960,600),(960,380),(1120,380)],8,'#DCE6EA',.8)+poly([(1110,400),(1130,400),(1120,520)],'#DCE6EA',sw=4)+poly([(1080,390),(1095,390),(1088,460)],'#DCE6EA',sw=3)
    o+=''.join(line(940,420+i*40,980,440+i*40,5,'#E9F0F2',.9,0) for i in range(4))
    return svg(o)
@sc
def snowwater():
    o=paperbg()
    for i in range(10):
        x,y=170+(i%5)*190,330+(i//5)*240; o+=poly([(x,y),(x+140,y),(x+120,y+150),(x+20,y+150)],P['steel'],sw=6)+f'<path d="M{x-5},{y+5} Q{x+70},{y-90} {x+145},{y+5} Z" fill="{P["snow"]}" stroke="{P["ch"]}" stroke-width="5"/>'
    o+=pl([(1170,520),(1380,520)],12)+pl([(1340,480),(1385,520),(1340,560)],12)
    o+=poly([(1440,400),(1700,400),(1660,680),(1480,680)],P['steel'],sw=7)+poly([(1452,470),(1688,470),(1662,670),(1478,670)],P['blue'],sw=0)
    return svg(o)
@sc
def pot():
    o='<rect width="1920" height="1080" fill="#4A4740"/>'+f'<circle cx="960" cy="700" r="500" fill="url(#heat)"/>'+rect(0,880,1920,200,'#36342F',sw=0)
    o+=rect(760,560,460,320,'#6A5F52',sw=8)+''.join(line(800,600+i*30,1180,600+i*30,6,P['red'],.6,0) for i in range(8))
    o+=rect(860,450,260,110,P['steel'],sw=7)+f'<path d="M870,455 Q990,380 1110,455 Z" fill="{P["snow"]}" stroke="{P["ch"]}" stroke-width="5"/>'
    o+=''.join(f'<path d="M{920+i*60},430 q-25,-50 0,-100 q25,-50 0,-100" fill="none" stroke="#DCD8CE" stroke-width="7" opacity=".6"/>' for i in range(3))
    o+=figure(560,1020,1.9,arms=((20,-10),(-55,-40)),expr='neutral',look=1)
    return svg(o,rgrad('heat',P['red'],.25))
@sc
def headache():
    o='<rect width="1920" height="1080" fill="#5C6066"/>'+rect(1240,160,300,240,'#AEB4B6',sw=8)+f'<path d="M1240,400 L1540,400 L1300,1000 L800,1000 Z" fill="#AEB4B6" opacity=".2"/>'
    o+=rect(420,830,900,110,P['brownD'],sw=8)+f'<path d="M440,820 Q800,790 1300,830 L1310,850 L440,850 Z" fill="{P["gg"]}" stroke="{P["ch"]}" stroke-width="6"/>'
    o+=figure(860,840,2.0,sit=True,arms=((-150,-30),(150,30)),expr='pain')
    o+=''.join(f'<path d="M{760+i*90},{560-abs(i-1)*20} l20,-30 l15,20 l20,-30" fill="none" stroke="{P["red"]}" stroke-width="6" opacity=".7"/>' for i in range(3))
    return svg(o)
@sc
def whiteout():
    o='<rect width="1920" height="1080" fill="#D7D7D1"/>'+''.join(line(random.Random(i).uniform(-200,1920),random.Random(i+9).uniform(0,1080),random.Random(i).uniform(-200,1920)+160,random.Random(i+9).uniform(0,1080)+40,random.Random(i).uniform(4,14),'#F2F1EC',.7,4) for i in range(90))
    o+=pl([(0,905),(820,890)],7,P['brown'])+pl([(985,888),(1400,870),(1920,850)],7,P['brown'])
    o+=f'<g opacity=".55">{figure(900,920,1.7,arms=((15,-10),(-15,10)),expr="worried",look=1)}</g>'
    return svg(o+''.join(line(random.Random(i).uniform(-200,1920),random.Random(i+3).uniform(0,1080),random.Random(i).uniform(-200,1920)+200,random.Random(i+3).uniform(0,1080)+50,random.Random(i).uniform(6,18),'#F5F4F0',.6,4) for i in range(30)))
@sc
def mast_ice():
    d,b=nightsky()
    o=b+rect(0,820,1920,260,'#6F6C66',sw=7)+rect(0,800,1920,30,P['snow'],sw=5)+line(960,820,960,80,14)+''.join(line(900,200+i*120,1020,200+i*120,7) for i in range(5))
    o+=''.join(poly([(x,y),(x+30,y+10),(x+10,y+50)],'#DDE6EA',sw=4) for x,y in [(990,300),(930,460),(1010,600),(970,720)])
    o+=''.join(f'<path d="M{980-r},{805} A{r},{r*.4} 0 0 1 {980+r},{805}" fill="none" stroke="{P["yelL"]}" stroke-width="5" opacity=".5"/>' for r in (60,110))
    return svg(o+snowfall(120,11,slant=3),d)
@sc
def tempchart():
    T=[(3,-27,1),(4,-20,0),(5,-28,1),(8,-17,0),(11,-31,1),(13,-24,0),(14,-32,1)]
    o=paperbg()+txt(960,170,'COLDEST NIGHTS',90)+line(220,300,1700,300,6)
    for i,(n,tc,k) in enumerate(T):
        x=280+i*200; h=(-tc-10)*24
        o+=rect(x,300,120,h,P['blueD'] if k else P['blue'],sw=6)+txt(x+60,270,'NIGHT '+str(n),40,P['brownD'])+txt(x+60,300+h+60,str(tc)+'°',48)
        if k: o+=circ(x+60,300+h+150,42,P['yel'],sw=6)+txt(x+60,300+h+168,'KNOCK',30)
    return svg(o)
def detector(state):
    o='<rect width="1920" height="1080" fill="#4A4842"/>'
    if state=='alarm': o+=f'<circle cx="960" cy="540" r="600" fill="url(#rg)"/>'
    o+=rect(620,190,680,700,'#ECE8DE',sw=10)+''.join(line(690,260+i*40,1230,260+i*40,8,P['ch'],.4,0) for i in range(3))+txt(960,860,'CO ALARM',40,P['ch'])
    o+=rect(720,520,480,200,'#1E2420',sw=8)
    if state=='off': o+=rect(760,740,400,90,'#2A2826',sw=6)+txt(960,800,'NO BATTERY',30,'#8E8A80')
    if state=='alarm':
        o+=txt(960,670,'280 PPM',150,'#E06A55',ls=4)+''.join(f'<path d="M{1340+i*60},{360-i*40} Q{1420+i*70},540 {1340+i*60},{720+i*40}" fill="none" stroke="#E06A55" stroke-width="10" opacity="{.8-i*.2}"/>' for i in range(3))+''.join(f'<path d="M{580-i*60},{360-i*40} Q{500-i*70},540 {580-i*60},{720+i*40}" fill="none" stroke="#E06A55" stroke-width="10" opacity="{.8-i*.2}"/>' for i in range(3))
    if state=='zero': o+=txt(960,670,'0 PPM',150,'#9DB28E',ls=4)
    return svg(o,rgrad('rg','#C0402F',.45))
D['detector_off']=lambda:detector('off'); D['detector_alarm']=lambda:detector('alarm'); D['detector_zero']=lambda:detector('zero')
@sc
def cosym():
    o=paperbg()
    o+=ell(330,330,120,70,'none',P['ch'],8)+circ(330,330,36,P['ch'],sw=0)+line(200,430,460,230,12,P['red'])+txt(330,500,'NO COLOR',60)
    o+=f'<path d="M820,240 q-60,130 -10,170 q40,20 70,-10" fill="none" stroke="{P["ch"]}" stroke-width="10"/>'+line(700,430,960,230,12,P['red'])+txt(830,500,'NO SMELL',60)
    for i,(lab,ico) in enumerate([('HEADACHE','pain'),('CONFUSION','worried'),('SLEEP','tired')]):
        x=360+i*600; o+=figure(x,930,.8,arms=((10,-5),(-10,5)),expr=ico)+txt(x,1010,lab,56)
        if i<2: o+=pl([(x+130,820),(x+430,820)],10)+pl([(x+400,790),(x+435,820),(x+400,850)],10)
    o+=f'<g transform="translate(1600,520)">'+''.join(ell(0,0,90-k*20,90-k*20,'none',P['red'],5,.6) for k in range(3))+txt(0,25,'Zz',70,P['red'])+'</g>' if False else ''
    return svg(o)
@sc
def codiag():
    o=paperbg()+rect(260,280,1100,520,'#D4C9B0',sw=10)+line(820,280,820,800,6)
    o+=rect(940,560,300,240,P['gen'],sw=7)+pl([(1100,560),(1100,450),(1440,450)],20,P['steel'])
    o+=f'<path d="M1300,800 Q1420,300 1800,280 L1900,800 Z" fill="{P["snow"]}" stroke="{P["snowS"]}" stroke-width="8"/>'+txt(1600,600,'BURIED',64,P['blueD'])+txt(1280,420,'EXHAUST',44)
    for k,(a,b) in enumerate([(1180,500),(780,540),(420,600)]):
        o+=pl([(a+120,b-20),(a+60,b+10),(a,b)],9,P['red'],.75)+poly([(a-10,b-2),(a+18,b-18),(a+14,b+14)],P['red'],sw=0,op=.75)
    o+=rect(200,600,60,180,P['brown'],sw=6)+txt(160,560,'SHUT',40,P['red'])
    return svg(o)
@sc
def drift1():
    d=grad('sky','#8F979C','#B9BCB8'); return svg('<rect width="1920" height="1080" fill="url(#sky)"/>'+station(300,560,lit=True,drift=1,night=False)+snowfall(260,12,slant=6,op=.8),d)
@sc
def drift2():
    d=grad('sky','#7E868C','#A9ADAA'); return svg('<rect width="1920" height="1080" fill="url(#sky)"/>'+station(300,560,lit=True,drift=2,night=False)+snowfall(300,13,slant=7,op=.85),d)
@sc
def confused():
    o=desk_room()+f'<circle cx="760" cy="420" r="420" fill="url(#lamp)"/>'+figure(1250,830,1.95,sit=True,arms=((40,-60),(-140,-20)),expr='tired',tilt=12)+rect(380,700,1100,40,P['brown'],sw=7)
    o+=''.join(rect(560+i*170,600+(i%2)*14,150,100,P['beigeL'],sw=4)+txt(635+i*170,665+(i%2)*14,f'-{28+i}°',44) for i in range(4))
    o+=''.join(txt(635+i*170+14,665+(i%2)*14+10,f'-{28+i}°',44,P['ch'],op=.35) for i in range(4))
    o+=''.join(f'<path d="M{1180+i*40},{620-i*20} q30,-30 60,0 q30,30 60,0" fill="none" stroke="{P["yelL"]}" stroke-width="6" opacity=".6"/>' for i in range(3))
    return svg(o,rgrad('lamp',P['yel'],.3))
@sc
def heater():
    o='<rect width="1920" height="1080" fill="#3E3B36"/>'+rect(1250,160,500,500,'#1F2630',sw=10)+snowfall(60,15,slant=4)+txt(1500,420,'-32',140,P['yelL'])
    o+=rect(260,260,720,560,'#6A5F52',sw=9)+circ(620,540,180,P['beigeL'],sw=9)+txt(620,330,'HEAT',60)
    o+=line(620,540,760,420,18,P['red'])+txt(470,700,'LOW',44)+txt(780,720,'MAX',52,P['red'])
    return svg(o)
@sc
def hallway():
    o='<rect width="1920" height="1080" fill="#16191C"/>'+poly([(0,0),(700,330),(700,750),(0,1080)],'#22272B',sw=0)+poly([(1920,0),(1220,330),(1220,750),(1920,1080)],'#22272B',sw=0)
    o+=rect(1380,380,190,360,'#3B3F42',sw=8)+txt(1475,420,'GEN',40,P['yel'])
    o+=f'<path d="M520,620 L1600,380 L1600,760 Z" fill="{P["yelL"]}" opacity=".18"/>'
    o+=''.join(f'<path d="M{1475-r},{560} A{r},{r} 0 0 1 {1475+r},{560}" fill="none" stroke="{P["yelL"]}" stroke-width="6" opacity="{.5-k*.12}"/>' for k,r in enumerate((150,230,310)))
    flash=lambda h:poly([(h[0],h[1]),(h[0]+40,h[1]-14),(h[0]+40,h[1]+14)],P['yelL'],sw=4)
    o+=figure(450,1020,1.9,arms=((20,-10),(-80,-5)),legs=((20,10),(-25,10)),expr='worried',look=1,hold=flash)
    return svg(o)
@sc
def dooropen():
    d,b=nightsky(); r=random.Random(5)
    o=b+''.join(ell(r.uniform(0,1920),r.uniform(0,700),2,2,P['yelL'],op=.7) for _ in range(90))+rect(0,0,560,1080,'#3A3833',sw=0)+rect(1360,0,560,1080,'#3A3833',sw=0)+rect(560,0,800,80,'#3A3833',sw=0)
    o+=rect(560,80,800,1000,'none',sw=12)+rect(1360,80,90,1000,P['brownD'],sw=8)
    o+=''.join(f'<path d="M{700+i*90},{200+i*40} q-200,80 -500,{40+i*60}" fill="none" stroke="#D9E4EA" stroke-width="8" opacity=".55"/>' for i in range(6))
    o+=figure(960,1060,2.1,arms=((-150,30),(150,-30)),expr='relief')+snowfall(80,6,slant=-6)
    return svg(o,d)
@sc
def dig():
    d,b=nightsky()
    o=b+rect(0,0,900,820,'#4D4A44',sw=8)+f'<path d="M500,1080 Q900,520 1920,380 L1920,1080 Z" fill="{P["snow"]}" stroke="{P["snowS"]}" stroke-width="8"/>'
    o+=rect(1380,640,240,70,P['steel'],sw=7)+rect(1560,640,60,70,'#2A2A28',sw=5)+''.join(poly([(1580+i*8,650),(1600+i*8,650),(1590+i*8,700)],'#DDE6EA',sw=3) for i in range(3))
    o+=f'<path d="M1300,780 L1700,620 L1760,760 Z" fill="{P["yelL"]}" opacity=".2"/>'
    sh=lambda h:line(h[0],h[1],h[0]+120,h[1]+90,9,P['brownD'])+poly([(h[0]+110,h[1]+80),(h[0]+170,h[1]+100),(h[0]+130,h[1]+150)],P['steel'],sw=5)
    o+=figure(1060,940,1.8,arms=((-60,-40),(-70,-30)),legs=((15,20),(-30,15)),expr='focused',look=1,hold=sh)+pl([(0,900),(600,860),(1080,780)],6,P['brown'])
    return svg(o+snowfall(100,17,slant=4),d)
@sc
def pipeclear():
    d,b=nightsky('#28313C','#3C4855')
    o=b+rect(0,0,1100,1080,'#55524B',sw=8)+rect(1100,0,820,1080,P['snow'],sw=0)
    o+=rect(760,470,420,90,P['steel'],sw=8)+ell(1180,515,22,40,'#1F1F1E')
    for j in range(3):
        for k in range(4): o+=rect(1120+k*150,580+j*110-((k+j)%2)*10,140,100,'#E8E6DF',P['snowS'],5)
    o+=''.join(rect(1120+k*150,340-((k)%2)*10,140,100,'#E8E6DF',P['snowS'],5) for k in range(4))
    o+=''.join(ell(1260+i*70,500-i*40,30+i*10,20+i*6,'#B9B6AE',op=.4) for i in range(4))
    return svg(o,d)
@sc
def endcard():
    o=card_bg()+poly([(760,620),(900,430),(990,540),(1060,470),(1160,620)],P['gg'],sw=6)+rect(925,520,70,60,P['yel'],sw=5)
    o+=txt(960,780,'SUBSCRIBE FOR MORE STORIES',96,P['yelL'],ls=6)
    return svg(o)
def card(title,subt=''):
    return svg(card_bg()+txt(960,560,title,170,P['yelL'],ls=10)+(txt(960,680,subt,72,'#9C9A92',ls=8) if subt else '')+line(760,600 if not subt else 720,1160,600 if not subt else 720,4,P['yel'],.4,0))
