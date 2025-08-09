import numpy as np
N=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def midi_to_note_name(m:int)->str: return f"{N[m%12]}{m//12-1}"
def midi_to_freq(m:int,a4=440.0)->float: import math; return a4*(2**((m-69)/12))
def freq_to_midi_cents(f:float,a4=440.0):
    if f<=0: return None,None
    import numpy as np
    mf=69+12*np.log2(f/a4); nm=int(round(mf)); return nm,(mf-nm)*100
