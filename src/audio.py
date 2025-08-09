import numpy as np, queue
try:
    import sounddevice as sd, aubio
except Exception:
    sd=None; aubio=None
HAVE_AUDIO = sd is not None and aubio is not None
class Audio:
    def __init__(self,sr=44100,buffer=512,hop=256,algo='yinfft',silence=-35,cb=None):
        self.sr=sr; self.buffer=buffer; self.hop=hop; self.algo=algo; self.silence=silence; self.cb=cb
        self.q=queue.Queue(); self.stream=None; self._pitch=None; self._buf=np.empty((0,),np.float32)
        if HAVE_AUDIO:
            self._pitch=aubio.pitch(self.algo,self.buffer,self.hop,self.sr); self._pitch.set_unit('Hz'); self._pitch.set_silence(self.silence)
    def _on(self,indata,frames,time,status):
        s=indata[:,0].astype(np.float32); self._buf=np.concatenate([self._buf,s])
        while len(self._buf)>=self.hop:
            c=self._buf[:self.hop]; self._buf=self._buf[self.hop:]
            f=float(self._pitch(c)[0]) if HAVE_AUDIO else 0.0
            conf=float(self._pitch.get_confidence()) if HAVE_AUDIO else 0.0
            if f>40.0: self.q.put((f,conf))
    def start(self,device=None):
        if not HAVE_AUDIO: return False
        try:
            self.stream=sd.InputStream(device=device,channels=1,samplerate=self.sr,blocksize=self.hop,callback=self._on); self.stream.start(); return True
        except Exception: return False
    def stop(self):
        if self.stream:
            try: self.stream.stop(); self.stream.close()
            except Exception: pass
            self.stream=None
    def poll(self):
        while not self.q.empty():
            f,c=self.q.get_nowait()
            if self.cb: self.cb(f,c)
