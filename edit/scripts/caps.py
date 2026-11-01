import json,re
e=json.load(open("edl.json")); W=[w for s in json.load(open("main.json")) for w in s["words"]]
chunks=[]
for c in e:
    print(f'#{c["id"]:2d} t0={c["t0"]:6.2f} dur={c["dur"]:5.2f} {c["sec"]}')
    if not c["cap"]: continue
    a0,a1=c["a"]
    ws=[w for w in W if w["s"]>=a0-0.05 and w["e"]<=a1+0.3]
    toks=re.findall(r"\[[^\]]+\][^\s]*|[^\s]+",c["cap"])
    s0=(ws[0]["s"] if ws else a0)-a0; s1=(ws[-1]["e"] if ws else a1)-a0
    if len(ws)==len(toks): times=[(w["s"]-a0) for w in ws]
    else: times=[s0+(s1-s0)*i/len(toks) for i in range(len(toks))]
    # group into chunks of <=3 words, break after commas
    grp=[];cur=[]
    for i,tk in enumerate(toks):
        cur.append((tk,times[i])); 
        if len(cur)>=3 or (tk.endswith(",") or tk.endswith("…")) and len(cur)>=2: grp.append(cur);cur=[]
    if cur: grp.append(cur)
    if len(grp)>1 and len(grp[-1])==1: x=grp.pop(); grp[-1]+=x
    for gi,g in enumerate(grp):
        st=c["t0"]+max(g[0][1],0)
        en=c["t0"]+(grp[gi+1][0][1] if gi+1<len(grp) else min(s1+0.35,c["dur"]))
        words=[{"t":x[0],"at":round(c["t0"]+x[1]-st,2)} for x in g]
        chunks.append({"s":round(st,2),"e":round(en,2),"w":words})
json.dump(chunks,open("caps.json","w"),ensure_ascii=False)
print(len(chunks)); [print(c["s"],c["e"]," ".join(x["t"] for x in c["w"])) for c in chunks]
