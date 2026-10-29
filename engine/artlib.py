import math, random
P=dict(beige='#D8CBB0',beigeL='#E6DCC6',paper='#E9E0CB',brown='#7A5E48',brownD='#5A4636',gg='#7D8C76',ggD='#5C6B58',
 blue='#6E8296',blueD='#3E4C5C',night='#20262E',night2='#2C3540',ch='#2A2B2E',yel='#CDB46A',yelL='#E3D39A',red='#A9483C',
 snow='#E6E3DA',snowS='#C4C8C6',concrete='#9C968A',concreteD='#77736A',skin='#E4D2B4',parka='#8A5A3C',beanie='#C2A04F',
 scarf='#7D8C76',pants='#45474C',ruthc='#6C7F93',hair='#8E8A84',gen='#7F8A6E',steel='#8C9096')
R=random.Random(7)
def J(a=2.2): return R.uniform(-a,a)
def pts2path(pts,closed=True,a=2.0):
    s='M'+' L'.join(f'{x+J(a):.1f},{y+J(a):.1f}' for x,y in pts)
    return s+(' Z' if closed else '')
def sub(pts,n=6):
    out=[]
    for i in range(len(pts)):
        x1,y1=pts[i];x2,y2=pts[(i+1)%len(pts)]
        for k in range(n): out.append((x1+(x2-x1)*k/n,y1+(y2-y1)*k/n))
    return out
def poly(pts,fill,st=P['ch'],sw=6,a=1.8,op=1,closed=True):
    return f'<path d="{pts2path(sub(pts) if closed else pts,closed,a)}" fill="{fill if closed else "none"}" stroke="{st}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" opacity="{op}"/>'
def rect(x,y,w,h,fill,st=P['ch'],sw=6,a=1.8,op=1): return poly([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],fill,st,sw,a,op)
def circ(cx,cy,r,fill,st=P['ch'],sw=6,a=1.2,op=1,n=36):
    return poly([(cx+r*math.cos(2*math.pi*i/n),cy+r*math.sin(2*math.pi*i/n)) for i in range(n)],fill,st,sw,a,op) if False else \
      f'<path d="{pts2path([(cx+r*math.cos(2*math.pi*i/n),cy+r*math.sin(2*math.pi*i/n)) for i in range(n)],True,a)}" fill="{fill}" stroke="{st}" stroke-width="{sw}" opacity="{op}"/>'
def ell(cx,cy,rx,ry,fill,st='none',sw=0,op=1): return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{st}" stroke-width="{sw}" opacity="{op}"/>'
def line(x1,y1,x2,y2,sw=10,st=P['ch'],op=1,bend=3):
    mx,my=(x1+x2)/2+J(bend),(y1+y2)/2+J(bend)
    return f'<path d="M{x1:.1f},{y1:.1f} Q{mx:.1f},{my:.1f} {x2:.1f},{y2:.1f}" fill="none" stroke="{st}" stroke-width="{sw}" stroke-linecap="round" opacity="{op}"/>'
def pl(pts,sw=6,st=P['ch'],op=1,dash=None,fill='none'):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{pts2path(pts,False,1.2)}" fill="{fill}" stroke="{st}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" opacity="{op}"{d}/>'
def txt(x,y,s,size=48,fill=P['ch'],font='Bebas Neue',anchor='middle',rot=0,op=1,ls=0):
    s=s.replace('&','&amp;')
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" opacity="{op}" letter-spacing="{ls}" transform="rotate({rot} {x} {y})">{s}</text>'
def _mix(c1,c2):
    h=lambda c:[int(c[i:i+2],16) for i in (1,3,5)]
    return '#%02x%02x%02x'%tuple((x+y)//2 for x,y in zip(h(c1),h(c2)))
def grad(id,c1,c2,vert=True):
    m=_mix(c1,c2); return f'<linearGradient id="{id}"><stop offset="0" stop-color="{m}"/><stop offset="1" stop-color="{m}"/></linearGradient>'
def _grad_old(id,c1,c2,vert=True): return f'<linearGradient id="{id}" x1="0" y1="0" x2="{0 if vert else 1}" y2="{1 if vert else 0}"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'
def rgrad(id,c,op=0.8): return f'<radialGradient id="{id}"><stop offset="0" stop-color="{c}" stop-opacity="0"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>'
def svg(body,defs=''): return f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080"><defs>{defs}</defs>{body}</svg>'
def snowfall(n=160,seed=1,col='#E6E3DA',op=.8,slant=0,ymax=1080):
    r=random.Random(seed);o=''
    for _ in range(n):
        x,y=r.uniform(0,1920),r.uniform(0,ymax);s=r.uniform(2,5)
        o+=line(x,y,x+slant*s,y+s*2.2,s,col,op*r.uniform(.4,1),0) if slant else ell(x,y,s,s,col,op=op*r.uniform(.4,1))
    return o
# ---------- character rig ----------
def limb(x,y,a1,a2,l1,l2,sw=11,col=P['ch']):
    r1,r2=math.radians(a1),math.radians(a1+a2)
    ex,ey=x+l1*math.sin(r1),y+l1*math.cos(r1); hx,hy=ex+l2*math.sin(r2),ey+l2*math.cos(r2)
    return line(x,y,ex,ey,sw,col,1,2)+line(ex,ey,hx,hy,sw,col,1,2),(hx,hy)
def face(cx,cy,expr,look=0):
    lx=look*8;o=''
    E=[(cx-17+lx,cy-2),(cx+17+lx,cy-2)]
    if expr in('scared','alarm'):
        for ex,ey in E: o+=ell(ex,ey,10,12,'#F4F0E6')+ell(ex+lx*.4,ey+1,6,6.5,P['ch'])
        o+=line(cx-26+lx,cy-24,cx-8+lx,cy-27,4,bend=1)+line(cx+8+lx,cy-27,cx+26+lx,cy-24,4,bend=1)
        o+=ell(cx+lx,cy+22,6,8,P['ch'])
    elif expr=='pain':
        o+=pl([(E[0][0]-8,E[0][1]-5),(E[0][0]+6,E[0][1]),(E[0][0]-8,E[0][1]+5)],4)+pl([(E[1][0]+8,E[1][1]-5),(E[1][0]-6,E[1][1]),(E[1][0]+8,E[1][1]+5)],4)
        o+=pl([(cx-12,cy+22),(cx-4,cy+18),(cx+4,cy+22),(cx+12,cy+18)],4)
    elif expr=='tired':
        for ex,ey in E: o+=ell(ex,ey+2,5,4,P['ch'])+line(ex-9,ey-3,ex+9,ey-3,4,bend=0)
        o+=line(cx-9+lx,cy+20,cx+9+lx,cy+21,4,bend=1)
    elif expr=='relief':
        for ex,ey in E: o+=f'<path d="M{ex-9},{ey+2} Q{ex},{ey-8} {ex+9},{ey+2}" fill="none" stroke="{P["ch"]}" stroke-width="4" stroke-linecap="round"/>'
        o+=f'<path d="M{cx-12},{cy+16} Q{cx},{cy+27} {cx+12},{cy+16}" fill="none" stroke="{P["ch"]}" stroke-width="4" stroke-linecap="round"/>'
    else:
        for ex,ey in E: o+=ell(ex,ey,5.5,6.5,P['ch'])
        if expr=='worried': o+=line(cx-25+lx,cy-17,cx-9+lx,cy-22,4,bend=0)+line(cx+9+lx,cy-22,cx+25+lx,cy-17,4,bend=0)+pl([(cx-9+lx,cy+21),(cx-3+lx,cy+18),(cx+3+lx,cy+21),(cx+9+lx,cy+18)],4)
        elif expr=='focused': o+=line(cx-25+lx,cy-18,cx-9+lx,cy-16,4,bend=0)+line(cx+9+lx,cy-16,cx+25+lx,cy-18,4,bend=0)+line(cx-8+lx,cy+19,cx+8+lx,cy+19,4,bend=0)
        elif expr=='smile': o+=f'<path d="M{cx-11+lx},{cy+15} Q{cx+lx},{cy+25} {cx+11+lx},{cy+15}" fill="none" stroke="{P["ch"]}" stroke-width="4" stroke-linecap="round"/>'
        else: o+=line(cx-7+lx,cy+19,cx+7+lx,cy+19,4,bend=1)
    return o
def figure(x,y,s=1.0,who='you',expr='neutral',look=0,arms=((15,-10),(-15,10)),legs=((6,0),(-6,0)),tilt=0,sit=False,hold=None,headset=False):
    """x,y = feet ground point. arms/legs: (angle,bend) for back/front. returns svg group"""
    o=''; hipy=-10; sh=(-92)
    torso_col={'you':P['parka'],'ruth':P['ruthc'],'hal':P['brown']}[who]
    if sit: legs=((80,-85),(70,-80)) if legs==((6,0),(-6,0)) else legs
    b_leg,_=limb(-10,hipy,legs[0][0],legs[0][1],50,52,12)
    f_leg,ft=limb(10,hipy,legs[1][0],legs[1][1],50,52,12)
    b_arm,_=limb(-24,sh,arms[0][0],arms[0][1],44,42,11)
    f_arm,hand=limb(24,sh,arms[1][0],arms[1][1],44,42,11)
    o+=b_arm+b_leg
    o+=poly([(-34,-104),(34,-104),(40,-4),(-40,-4)],torso_col,sw=6)
    if who=='you':
        o+=line(-38,-40,38,-40,5,P['yel'],.8,0)  # faded reflective band
        o+=poly([(-30,-112),(30,-112),(26,-96),(-26,-96)],P['scarf'],sw=5)
    if who=='ruth': o+=line(0,-104,0,-6,4,P['blueD'],.6,0)
    o+=f_leg+f_arm
    if hold: o+=hold(hand)
    hx,hy=0+tilt*0.6,-152
    g=f'<g transform="rotate({tilt} 0 -110)">'
    g+=circ(hx,hy,46,P['skin'],sw=6)
    if who=='you':
        g+=f'<path d="M{hx-48},{hy-8} Q{hx-46},{hy-62} {hx},{hy-64} Q{hx+46},{hy-62} {hx+48},{hy-8} Z" fill="{P["beanie"]}" stroke="{P["ch"]}" stroke-width="6"/>'+rect(hx-50,hy-20,100,18,P['yelL'],sw=5)+circ(hx+4,hy-70,12,P['yelL'],sw=5)
    if who=='ruth':
        g+=f'<path d="M{hx-52},{hy+30} Q{hx-58},{hy-50} {hx},{hy-52} Q{hx+58},{hy-50} {hx+52},{hy+30} L{hx+38},{hy+30} Q{hx+40},{hy-26} {hx},{hy-30} Q{hx-40},{hy-26} {hx-38},{hy+30} Z" fill="{P["hair"]}" stroke="{P["ch"]}" stroke-width="5"/>'
        g+=f'<circle cx="{hx-17}" cy="{hy-2}" r="14" fill="none" stroke="{P["ch"]}" stroke-width="4"/><circle cx="{hx+17}" cy="{hy-2}" r="14" fill="none" stroke="{P["ch"]}" stroke-width="4"/>'
    if who=='hal':
        g+=f'<path d="M{hx-40},{hy+14} Q{hx-38},{hy+62} {hx},{hy+64} Q{hx+38},{hy+62} {hx+40},{hy+14} Q{hx},{hy+36} {hx-40},{hy+14} Z" fill="{P["hair"]}" stroke="{P["ch"]}" stroke-width="5"/>'
        g+=f'<path d="M{hx-48},{hy-14} Q{hx},{hy-80} {hx+48},{hy-14} Z" fill="{P["brownD"]}" stroke="{P["ch"]}" stroke-width="5"/>'+line(hx+20,hy-16,hx+70,hy-12,9,P['brownD'],1,0)
    if headset: g+=f'<path d="M{hx-50},{hy} Q{hx},{hy-80} {hx+50},{hy}" fill="none" stroke="{P["ch"]}" stroke-width="7"/>'+rect(hx-58,hy-14,14,30,P['ch'])+line(hx-50,hy+12,hx-20,hy+38,5)
    g+=face(hx,hy+2,expr,look)+'</g>'
    o+=g
    return f'<g transform="translate({x},{y}) scale({s})">{o}</g>'
