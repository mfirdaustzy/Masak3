import numpy as np,wave,sys
R=48000; out=sys.argv[1]; rng=np.random.default_rng(7)
def save(n,x):
    x=x/ (np.abs(x).max()+1e-9)*0.89; d=(x*32767).astype(np.int16)
    w=wave.open(f"{out}/{n}.wav","wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(R); w.writeframes(d.tobytes()); w.close()
def t(d): return np.arange(int(R*d))/R
def env(n,a,r): 
    e=np.ones(n); A=int(R*a); e[:A]=np.linspace(0,1,A) if A else 1; e*=np.exp(-np.arange(n)/(R*r)); return e
def lp(x,k):  # simple one-pole lowpass, k in 0..1
    y=np.zeros_like(x); s=0
    for i in range(len(x)): s+=k*(x[i]-s); y[i]=s
    return y
def bandsweep(d,f0,f1):
    n=int(R*d); x=rng.standard_normal(n); f=np.geomspace(f0,f1,n)
    # resonant sweep via moving lowpass
    y=np.zeros(n); s=0; s2=0
    for i in range(n):
        k=min(1,2*np.pi*f[i]/R); s+=k*(x[i]-s); s2+=k*(s-s2); y[i]=s-s2*0.5
    return y
# whoosh
n=int(R*0.45); w=bandsweep(0.45,300,4000)*np.sin(np.linspace(0,np.pi,n))**2; save("whoosh",w)
n=int(R*0.25); save("whoosh_s",bandsweep(0.25,500,5000)*np.sin(np.linspace(0,np.pi,n))**2)
# pop
tt=t(0.12); f=np.geomspace(900,300,len(tt)); save("pop",np.sin(2*np.pi*np.cumsum(f)/R)*env(len(tt),0.002,0.03))
# ding
tt=t(1.2); save("ding",(np.sin(2*np.pi*1318*tt)+0.4*np.sin(2*np.pi*2637*tt)+0.2*np.sin(2*np.pi*3951*tt))*env(len(tt),0.003,0.35))
# chime (two notes)
a=(np.sin(2*np.pi*1046*t(1.4))+0.3*np.sin(2*np.pi*2093*t(1.4)))*env(int(R*1.4),0.003,0.4)
b=(np.sin(2*np.pi*1568*t(1.4))+0.3*np.sin(2*np.pi*3136*t(1.4)))*env(int(R*1.4),0.003,0.45)
x=np.zeros(int(R*1.6)); x[:len(a)]+=a; x[int(R*0.12):int(R*0.12)+len(b)]+=b; save("chime",x)
# bass hit / boom
tt=t(0.9); f=np.geomspace(120,40,len(tt)); boom=np.sin(2*np.pi*np.cumsum(f)/R)*env(len(tt),0.002,0.25)
boom+=0.3*lp(rng.standard_normal(len(tt)),0.05)*env(len(tt),0.001,0.04); save("boom",np.tanh(boom*2))
# riser
n=int(R*1.0); r=bandsweep(1.0,200,6000)*np.linspace(0,1,n)**2; tt=t(1.0); r+=0.4*np.sin(2*np.pi*np.cumsum(np.geomspace(200,900,n))/R)*np.linspace(0,1,n)**2; save("riser",r)
# buzzer (wrong)
tt=t(0.35); save("buzz",np.sign(np.sin(2*np.pi*140*tt))*0.5*env(len(tt),0.005,0.2)*lp(np.ones(len(tt)),1))
# chop (knife on board)
tt=t(0.12); ch=lp(rng.standard_normal(len(tt)),0.35)*env(len(tt),0.0005,0.015)+0.6*np.sin(2*np.pi*220*tt)*env(len(tt),0.0005,0.03); 
x=np.zeros(int(R*0.75))
for o in (0,0.25,0.5): x[int(R*o):int(R*o)+len(ch)]+=ch
save("chop",x)
# sprinkle
x=np.zeros(int(R*0.7)); g=rng.standard_normal(int(R*0.004))
for _ in range(60):
    p=int(rng.uniform(0,0.65)*R); x[p:p+len(g)]+=g*rng.uniform(0.2,1)
x=x-lp(x,0.3); save("sprinkle",x*np.linspace(1,0.3,len(x)))
# tick
tt=t(0.04); save("tick",np.sin(2*np.pi*2500*tt)*env(len(tt),0.0005,0.006))
# blender (short)
tt=t(0.8); bl=np.sign(np.sin(2*np.pi*np.cumsum(np.linspace(80,190,len(tt)))/R))*0.4+0.6*lp(rng.standard_normal(len(tt)),0.2)
save("blender",bl*np.sin(np.linspace(0,np.pi,len(tt)))**0.5)
# splash/pour
n=int(R*0.8); sp=bandsweep(0.8,2500,600)*env(n,0.01,0.3); save("splash",sp)
