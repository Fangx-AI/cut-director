"""Original deterministic six-second accent bed; standard library only."""
import math
import random
import struct
import wave
from pathlib import Path
import argparse

def create(path):
    rate=48000
    rng=random.Random(12)
    samples=[]
    for n in range(rate*6):
        t=n/rate
        beat=t%0.5
        major=t%1.5
        # Short kick + quiet offbeat hat + a three-note accent. No sampled music.
        kick=0.40*math.exp(-beat*26)*math.sin(2*math.pi*(53*beat+1.8*(1-math.exp(-beat*35))))
        hat=(rng.random()*2-1)*0.035*math.exp(-((t+0.25)%0.5)*90)
        chord=sum(math.sin(2*math.pi*f*major) for f in (220,277.18,329.63))/3
        tone=0.16*chord*(1-math.exp(-major*180))*math.exp(-major*5)
        fade=min(1,(6-t)/0.10)
        samples.append(struct.pack('<h',round(max(-1,min(1,(kick+hat+tone)*fade))*32767)))
    with wave.open(str(path),'wb') as out:
        out.setnchannels(1);out.setsampwidth(2);out.setframerate(rate);out.writeframes(b''.join(samples))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('output',type=Path);args=parser.parse_args()
    create(args.output)
