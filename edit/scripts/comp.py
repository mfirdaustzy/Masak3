import json,html,re,sys
S=sys.argv[1]; caps=json.load(open("caps.json")); END=63.1
els=[]; js=[]; n=[0]
def nid(p): n[0]+=1; return f"{p}{n[0]}"
def el(tag,cls,start,dur,inner,style="",extra=""):
    i=nid("e"); els.append(f'<{tag} id="{i}" class="clip {cls}" data-start="{start:.2f}" data-duration="{dur:.2f}" style="{style}" {extra}>{inner}</{tag}>'); return i
def sfx(name,at,vol=0.8,dur=1.6):
    i=nid("a"); els.append(f'<audio id="{i}" class="clip" data-start="{at:.2f}" data-duration="{dur:.2f}" src="sfx/{name}.wav" data-volume="{vol}"></audio>')
def T(s): js.append(s)
def kw(t): return re.sub(r"\[(.+?)\]",r'<b>\1</b>',html.escape(t))

# --- camera moves on video
T('tl.fromTo("#v",{scale:1},{scale:1.22,duration:4.9,ease:"power1.inOut"},0)')
T('tl.set("#v",{scale:1},4.9)')
T('tl.fromTo("#v",{scale:1},{scale:1.12,duration:1.55,immediateRender:false,ease:"power1.out"},15.45)')
T('tl.set("#v",{scale:1},17.0)')
T('tl.fromTo("#v",{scale:1},{scale:1.15,duration:4.0,immediateRender:false,ease:"none"},20.1)')
T('tl.set("#v",{scale:1},24.1)')
# shake at sardin drop
for k,(dx,dy) in enumerate([(14,-10),(-12,8),(10,6),(-6,-6),(0,0)]):
    T(f'tl.to("#v",{{x:{dx},y:{dy},scale:1.06,duration:0.07,ease:"none"}},{31.4+k*0.07:.2f})')
T('tl.to("#v",{scale:1,duration:0.6,ease:"power2.out"},31.8)')
T('tl.fromTo("#v",{scale:1.15},{scale:1,duration:4.5,immediateRender:false,ease:"power1.out"},55.65)')

# --- captions
for c in caps:
    words="".join(f'<span class="w" data-at="{w["at"]}">{kw(w["t"])}</span> ' for w in c["w"])
    i=el("div","cap",c["s"],max(c["e"]-c["s"],0.3),words)
    for j,w in enumerate(c["w"]):
        T(f'tl.fromTo("#{i} .w:nth-child({j+1})",{{opacity:0,y:18,scale:0.9}},{{opacity:1,y:0,scale:1,duration:0.16,ease:"back.out(2.5)"}},{c["s"]+w["at"]:.2f})')

# --- hook title
i=el("div","hook",0.25,4.55,'<div class="hk-s">hari ni kita</div><div class="hk-b">MASAK<br>SARDIN</div><div class="hk-c">tapi yang edit… <span class="claude"><i class="spark"></i>Claude</span></div>')
T(f'tl.fromTo("#{i} .hk-s",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.3,ease:"power3.out"}},0.25)')
T(f'tl.fromTo("#{i} .hk-b",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(2)"}},0.35)')
T(f'tl.fromTo("#{i} .hk-c",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"back.out(2)"}},2.6)')
T(f'tl.to("#{i} .claude",{{scale:1.18,duration:0.18,yoyo:true,repeat:1,ease:"power2.out"}},4.3)')
T(f'tl.to("#{i}",{{opacity:0,y:-80,duration:0.25,ease:"power2.in"}},4.55)')
sfx("whoosh",0.0,0.7); sfx("boom",0.35,0.9); sfx("pop",2.6,0.6); sfx("pop",4.33,0.7)

# --- step labels
steps=[(4.9,10.95,"STEP 1","BAHAN"),(10.95,18.6,"STEP 2","POTONG & BLEND"),(18.6,30.2,"STEP 3","TUMIS"),(30.2,42.7,"STEP 4","SARDIN"),(42.7,53.2,"STEP 5","PERASA")]
for s,e,a,b in steps:
    i=el("div","step",s,e-s,f'<div class="st-a">{a}</div><div class="st-b{" long" if len(b)>8 else ""}">{b}</div>')
    T(f'tl.fromTo("#{i}",{{opacity:0,y:-60}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.8)"}},{s+0.02:.2f})')
    T(f'tl.to("#{i}",{{opacity:0,y:-40,duration:0.2,ease:"power2.in"}},{e-0.2:.2f})')
    sfx("whoosh_s",s,0.6,0.5)

# --- pills (callouts)
def pill(txt,at,end,x,y,cls="",snd="pop"):
    i=el("div","pill "+cls,at,end-at,txt,f"left:{x}px;top:{y}px")
    T(f'tl.fromTo("#{i}",{{opacity:0,scale:0.3,rotation:-8}},{{opacity:1,scale:1,rotation:-3,duration:0.4,ease:"back.out(3)"}},{at:.2f})')
    T(f'tl.to("#{i}",{{opacity:0,scale:0.6,duration:0.15}},{end-0.15:.2f})')
    if snd: sfx(snd,at,0.6,0.5)
    return i
pill("cili merah",7.0,9.95,250,560)
pill("bawang merah",8.2,9.95,600,460)
b=pill('<s>bawang putih</s> ✕',9.0,9.95,330,1050,"bad",None); sfx("buzz",9.0,0.35,0.5)
T(f'tl.fromTo("#{b}",{{x:-10}},{{x:10,duration:0.06,repeat:5,yoyo:true,ease:"none"}},9.35)')
pill("serai",10.0,10.95,700,700)
sfx("chop",11.0,0.5,0.9)
sfx("blender",15.5,0.35,1.0)
pill("✔ cili siap blend",17.3,18.6,300,520,"ok","ding")
sfx("whoosh",18.6,0.4,0.6)
# speed badges
def badge(txt,s,e):
    i=el("div","badge",s,e-s,txt)
    T(f'tl.fromTo("#{i}",{{opacity:0,x:60}},{{opacity:1,x:0,duration:0.25,ease:"power3.out"}},{s:.2f})')
    k=s+0.3
    while k<e-0.2: sfx("tick",k,0.35,0.2); k+=0.5
badge("2× ⏩",24.1,26.2)
pill("serai",26.6,28.2,560,720)
badge("2× ⏩",28.2,30.2)
i=el("div","note",28.3,1.9,"tumis sampai wangi")
T(f'tl.fromTo("#{i}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)"}},28.3)')
# SARDIN big moment
sfx("riser",30.4,0.45,1.1); sfx("boom",31.4,1.0,1.0); sfx("splash",31.45,0.4,0.9)
i=el("div","big",31.4,2.6,"SARDIN!")
T(f'tl.fromTo("#{i}",{{opacity:0,scale:2.4,rotation:6}},{{opacity:1,scale:1,rotation:-4,duration:0.35,ease:"back.out(1.6)"}},31.4)')
T(f'tl.to("#{i}",{{scale:1.08,duration:0.5,yoyo:true,repeat:2,ease:"sine.inOut"}},31.8)')
T(f'tl.to("#{i}",{{opacity:0,scale:0.7,duration:0.2}},33.8)')
f1=el("div","flash",31.4,0.3,"")
T(f'tl.fromTo("#{f1}",{{opacity:0.85}},{{opacity:0,duration:0.28}},31.4)')
# timelapse
badge("5× ⏩",35.5,39.3)
for k,(t,word) in enumerate([(35.7,"kacau,"),(36.7,"kacau,"),(37.7,"kacau…")]):
    i=el("div",f"kacau k{k}",t,39.25-t,word)
    T(f'tl.fromTo("#{i}",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(3)"}},{t})')
    sfx("pop",t,0.5,0.4)
pill("air",41.2,42.7,700,520,"",None); sfx("splash",41.3,0.5,0.9)
i=el("div","big yel",44.92,1.1,"kunyit!")
T(f'tl.fromTo("#{i}",{{opacity:0,y:60,scale:0.5}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(2.5)"}},44.92)')
sfx("pop",44.92,0.7,0.4)
pill("✔ perasa",46.6,49.0,330,560,"ok",None); sfx("sprinkle",46.6,0.5,0.8)
pill("✔ garam",49.9,51.0,580,560,"ok",None); sfx("sprinkle",50.0,0.5,0.8)
pill("cili hidup",52.1,53.2,300,640)
# SIAP
f2=el("div","flash",55.3,0.4,"")
T(f'tl.fromTo("#{f2}",{{opacity:1}},{{opacity:0,duration:0.38}},55.3)')
i=el("div","big siap",55.3,2.0,"SIAP!<span class='spk s1'>✦</span><span class='spk s2'>✦</span><span class='spk s3'>✦</span>")
T(f'tl.fromTo("#{i}",{{opacity:0,scale:0.3}},{{opacity:1,scale:1,duration:0.45,ease:"elastic.out(1,0.55)"}},55.3)')
T(f'tl.fromTo("#{i} .spk",{{scale:0,rotation:0}},{{scale:1,rotation:180,duration:0.6,stagger:0.1,ease:"back.out(3)"}},55.4)')
T(f'tl.to("#{i}",{{opacity:0,y:-60,duration:0.25}},57.05)')
sfx("chime",55.3,0.7,1.6)
# credit card
i=el("div","card",57.2,3.0,'<div class="c-s">edited with</div><div class="c-b"><i class="spark"></i>Claude × HyperFrames</div>')
T(f'tl.fromTo("#{i}",{{opacity:0,y:80}},{{opacity:1,y:0,duration:0.4,ease:"back.out(2)"}},57.2)')
T(f'tl.to("#{i}",{{opacity:0,y:40,duration:0.2}},60.0)')
sfx("whoosh_s",57.2,0.5,0.5)
# end card
i=el("div","endbg",60.2,END-60.2,"")
T(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:1,duration:0.35}},60.2)')
i=el("div","end",60.3,END-60.3,'<div class="e-s">follow untuk resepi &amp; tips edit seterusnya</div><div class="e-b">@mfirdausrosli1</div><div class="e-btn">+ FOLLOW</div>')
T(f'tl.fromTo("#{i} > div",{{opacity:0,y:50}},{{opacity:1,y:0,duration:0.4,stagger:0.15,ease:"back.out(2)"}},60.3)')
T(f'tl.fromTo("#{i} .e-btn",{{scale:1}},{{scale:1.1,duration:0.35,yoyo:true,repeat:3,ease:"sine.inOut"}},61.0)')
sfx("pop",60.45,0.6,0.4); sfx("ding",60.9,0.4,1.2)

tpl=open("comp_template.html").read()
open(S+"/hf/index.html","w").write(tpl.replace("{{ELS}}","\n".join(els)).replace("{{JS}}",";\n".join(js)+";").replace("{{END}}",str(END)))
print(len(els),"elements")
