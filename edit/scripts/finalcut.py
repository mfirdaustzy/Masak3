import json,subprocess,sys,os
S=sys.argv[1]; src=S+"/dl/video.bin"; e=json.load(open("edl.json"))
parts=[]
for c in e:
    v0,v1=c["v"]; sp=c["speed"]; d=c["dur"]; hold=c.get("hold") or 0; total=d+hold
    out=f"fc/{c['id']:02d}.mp4"
    vf=f"setpts=(PTS-STARTPTS)/{sp},fps=30"
    if hold: vf+=f",tpad=stop_mode=clone:stop_duration={hold}"
    cmd=["ffmpeg","-v","error","-y","-ss",str(v0),"-t",str(v1-v0),"-i",src]
    if c["a"]:
        a0,a1=c["a"]; cmd+=["-ss",str(a0),"-t",str(a1-a0),"-i",src]; af="[1:a]"
    else:
        af="[0:a]"+("atempo=2.0," if sp>=2 else "")+(f"atempo={sp/2}," if sp>2 else "")+"volume=0.5,"
    af+=f"aresample=48000,apad,atrim=0:{total:.3f},afade=t=in:d=0.04,afade=t=out:st={max(total-0.06,0):.3f}:d=0.06"
    cmd+=["-filter_complex",f"[0:v]{vf}[v];{af}[a]","-map","[v]","-map","[a]","-t",f"{total:.3f}","-c:v","libx264","-preset","medium","-crf","16","-pix_fmt","yuv420p","-c:a","pcm_s16le",out.replace(".mp4",".mov")]
    subprocess.run(cmd,check=True); parts.append(os.path.basename(out.replace(".mp4",".mov")))
open("fc/list.txt","w").write("".join(f"file '{p}'\n" for p in parts))
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","fc/list.txt","-c:v","copy","-af","highpass=f=70,afftdn=nf=-30,loudnorm=I=-16:TP=-1.5:LRA=9","-ar","48000","-c:a","aac","-b:a","192k","-movflags","+faststart",S+"/hf/cut.mp4"],check=True)
