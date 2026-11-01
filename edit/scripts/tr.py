import sys,json
from faster_whisper import WhisperModel
m=WhisperModel("large-v3",device="cpu",compute_type="int8")
import numpy as np, subprocess
def load(n):
    raw=open(n+".wav","rb").read()[44:]
    return np.frombuffer(raw,np.int16).astype(np.float32)/32768
for name in sys.argv[1:]:
    segs,info=m.transcribe(load(name),language="ms",word_timestamps=True,vad_filter=False,initial_prompt="Video tutorial dalam Bahasa Melayu Malaysia, campur English.")
    out=[]
    for s in segs:
        out.append({"start":s.start,"end":s.end,"text":s.text,"words":[{"w":w.word,"s":w.start,"e":w.end} for w in s.words]})
        print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}",flush=True)
    json.dump(out,open(name+".json","w"),ensure_ascii=False,indent=1)
