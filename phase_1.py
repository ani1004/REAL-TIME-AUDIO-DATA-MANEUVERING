# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:30:32 2020

@author: Aniruddha
"""

import pyaudio as pad
import numpy as np
import pylab as plb
import time as t
#import wavio
from scipy.signal import butter, filtfilt, iirnotch, savgol_filter
import cv2
import os


Fs = 44100
F = int(Fs/20) 
FORMAT = pad.paInt16
"""
Here,
    'F' variable specifies the number of frames per buffer.
    'Fs' variable defines time resolution of the recording device (Hz) / Sampling Frequency.
    'FORMAT' variable defines sampling size and format.
"""
def soundplot(Audio_in):
    t1=t.time()
    data = np.fromstring(Audio_in.read(F),dtype=np.int16)
    plb.figure(i)
    plb.plot(data)
    plb.title(i)
    plb.grid()
    plb.axis([0,len(data),-2**16/2,2**16/2])
    for v in plb.get_fignums():
            plb.figure(v)
            plb.savefig('zfigure%d.png' % v)
            img = cv2.imread('zfigure%d.png' % v)
            path = 'unfiltered_images'
            cv2.imwrite(os.path.join(path , 'zfigure%d.png') %v,img)
            cv2.waitKey(0)
    plb.close('all')
    image_folder = 'unfiltered_images'
    video_name = 'unfilter_video.avi'

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    
    video = cv2.VideoWriter(video_name, 0, 1, (width,height))
    
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))
    
    cv2.destroyAllWindows()
    video.release()
    print("took %.02f ms"%((t.time()-t1)*1000))
      #for a in range(10): #to it a few times just to see
    
    
# Main Code
if __name__=="__main__":
    s=pad.PyAudio()
    Audio_in=s.open(format=FORMAT,channels=1,rate=Fs,input=True,
                  frames_per_buffer=F)
    for i in range(int(10*Fs/F)): #do this for 10 seconds
        soundplot(Audio_in)
       
   
    Audio_in.stop_stream()
    Audio_in.close()
    s.terminate()
    