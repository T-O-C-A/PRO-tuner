import tkinter as tk
from tkinter import ttk, messagebox
import json, os, platform, time, webbrowser
from utils import midi_to_note_name, midi_to_freq, freq_to_midi_cents
from audio import Audio, HAVE_AUDIO
from updater import check_updates
APP_NAME='PRO-tuner'; BASE=os.path.dirname(__file__)
INSTR=os.path.join(BASE,'..','instruments','instruments.json')
VER=os.path.join(BASE,'..','version.json')
def load_json(p,d): 
    try: 
        with open(p,'r',encoding='utf-8') as f: return json.load(f)
    except Exception: return d
class App:
    def __init__(self,root):
        self.root=root
        try:
            s=ttk.Style(); sys=platform.system()
            if sys=='Darwin': s.theme_use('aqua')
            elif sys=='Windows': s.theme_use(s.theme_use())
            else: s.theme_use('clam')
        except Exception: pass
        self.ver=load_json(VER,{'version':'v0.0.0'})['version']
        root.title(f"{APP_NAME} {self.ver}"); root.geometry('1000x640'); root.after(50,self.splash)
        self.db=load_json(INSTR,{}); self.instrument=tk.StringVar(value=next(iter(self.db.keys()),''))
        self.tuning=tk.StringVar(value=''); self.sweet=tk.BooleanVar(value=False); self.a4=tk.DoubleVar(value=440.0)
        self.freq=tk.StringVar(value='—'); self.note=tk.StringVar(value='—'); self.conf=0.0
        self.audio=Audio(cb=self.on_pitch)
        top=ttk.Frame(root,padding=8); top.pack(fill='x')
        ttk.Label(top,text='Instrument:').pack(side='left'); self.cb_instr=ttk.Combobox(top,state='readonly',width=26,textvariable=self.instrument,values=list(self.db.keys())); self.cb_instr.pack(side='left',padx=6); self.cb_instr.bind('<<ComboboxSelected>>',self.on_instr)
        self.cb_tuning=ttk.Combobox(top,state='readonly',width=36,textvariable=self.tuning); self.cb_tuning.pack(side='left',padx=6)
        ttk.Checkbutton(top,text='Sweetened',variable=self.sweet).pack(side='left',padx=(12,6))
        ttk.Label(top,text='A4:').pack(side='left'); ttk.Spinbox(top,from_=415,to=466,increment=0.5,textvariable=self.a4,width=6).pack(side='left')
        ttk.Button(top,text='Start',command=self.start).pack(side='left',padx=6); ttk.Button(top,text='Stop',command=self.stop).pack(side='left')
        ttk.Button(top,text='Help',command=lambda:webbrowser.open_new_tab('https://t-o-c-a.github.io/PRO-tuner/howto_add_presets.md')).pack(side='right')
        mid=ttk.Frame(root,padding=8); mid.pack(fill='both',expand=True)
        ttk.Label(mid,text='Frequentie:').grid(row=0,column=0,sticky='w'); ttk.Label(mid,textvariable=self.freq,font=('Segoe UI',18,'bold')).grid(row=0,column=1,sticky='w',padx=8)
        ttk.Label(mid,text='Noot (+cent):').grid(row=1,column=0,sticky='w'); ttk.Label(mid,textvariable=self.note,font=('Segoe UI',18,'bold')).grid(row=1,column=1,sticky='w',padx=8)
        self.canvas=tk.Canvas(mid,height=260,bg='#0b1a2b',highlightthickness=0); self.canvas.grid(row=2,column=0,columnspan=4,sticky='ew',pady=12); mid.columnconfigure(3,weight=1)
        self.on_instr(); self.root.after(50,self.tick)
    def splash(self):
        sp=tk.Toplevel(self.root); sp.overrideredirect(True); w,h=480,280; x=(self.root.winfo_screenwidth()-w)//2; y=(self.root.winfo_screenheight()-h)//3; sp.geometry(f"{w}x{h}+{x}+{y}")
        cv=tk.Canvas(sp,width=w,height=h,bg='#0b1a2b',highlightthickness=0); cv.pack(fill='both',expand=True)
        cv.create_text(w//2,86,text='PRO-tuner',fill='#e6f5ff',font=('Segoe UI',28,'bold')); cv.create_text(w//2,120,text=self.ver,fill='#9bd3ff',font=('Segoe UI',12))
        st=cv.create_text(w//2,164,text='Checking for updates…',fill='#9bd3ff'); self.root.update(); upd=check_updates(self.ver); cv.itemconfigure(st,text=f"Update available: {upd['latest']}" if upd else 'Up to date / offline'); self.root.after(1200,sp.destroy)
    def on_instr(self,*_):
        d=self.db.get(self.instrument.get(),{}); t=list(d.get('tunings',{}).keys()); self.cb_tuning['values']=t; 
        if t: self.tuning.set(t[0])
    def start(self):
        if not HAVE_AUDIO: messagebox.showwarning('Audio','sounddevice/aubio niet beschikbaar.'); return
        if not self.audio.start(): messagebox.showerror('Audio','Kon de inputstream niet starten.'); return
        self.freq.set('…')
    def stop(self): self.audio.stop()
    def _offset(self,npc:str)->float:
        if not self.sweet.get(): return 0.0
        d=self.db.get(self.instrument.get(),{}); s=d.get('sweetened',{}); return float(s.get(npc, s.get('default',0.0)))
    def on_pitch(self,freq,conf):
        self.conf=conf; m,c=freq_to_midi_cents(freq,a4=self.a4.get())
        if m is None: return
        name=midi_to_note_name(m); off=self._offset(name[:-1]); c+=off; self.freq.set(f"{freq:.1f} Hz"); self.note.set(f"{name} ({c:+.1f}¢){' • offset '+str(off)+'¢' if off else ''}")
    def draw(self):
        w=self.canvas.winfo_width() or 900; h=self.canvas.winfo_height() or 260; self.canvas.delete('all'); cx=w//2; self.canvas.create_line(cx,0,cx,h,fill='#134e7a')
        import time; t=time.time(); speed=60*(self.conf or 0.5); bw=10
        for i in range(0,w,bw*3):
            x=int((i+(t*speed)%(bw*3))); self.canvas.create_rectangle(x,26,x+bw,h-26,fill='#12a0ff',outline='')
    def tick(self):
        try: self.audio.poll()
        except Exception: pass
        self.draw(); self.root.after(50,self.tick)
def run():
    root=tk.Tk(); App(root); root.mainloop()
if __name__=='__main__': run()
