# -*- coding: utf-8 -*-
"""
Created on Sat May 23 16:15:19 2020

@author: Aniruddha
"""

# Initialization of Libaraies and Variables.
import pyaudio as pad
import numpy as np
import pylab as plb
import time as t
import wavio
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

# Function defination to display the plot.
def soundplot(Audio_in):
    t1=t.time()
    data = np.fromstring(Audio_in.read(F),dtype=np.int16)
  
    data = data * np.hanning(len(data)) # smooth the FFT by windowing data
    fft = abs(np.fft.fft(data).real)
    fft = fft[:int(len(fft)/2)] # keep only first half
    freq = np.fft.fftfreq(F,1.0/Fs)
    freq = freq[:int(len(freq)/2)] # keep only first half
    freqPeak = freq[np.where(fft==np.max(fft))[0][0]]+1
    print("peak frequency: %d Hz"%freqPeak)
    if(freqPeak >= 1300):
         butter_lowpass(1300,F,data)
         #wavio.write("recorded.wav",data,F,sampwidth=2)
         plb.figure(i)
         plb.plot(data)
         plb.title(i)
         plb.grid()
         plb.axis([0,len(data),-2**16/2,2**16/2])
        # plb.savefig("03.png",dpi=50)
         for v in plb.get_fignums():
            plb.figure(v)
            plb.savefig('zfigure%d.png' % v)
            img = cv2.imread('zfigure%d.png' % v)
            path = 'filtered_images'
            cv2.imwrite(os.path.join(path , 'zfigure%d.png') %v,img)
            cv2.waitKey(0)
         plb.close('all')
         print("took %.02f ms"%((t.time()-t1)*1000))
       
    else:
        plb.figure(i)
        fig=plb.plot(data)
        plb.title(i)
        plb.grid()
        plb.axis([0,len(data),-2**16/2,2**16/2])
        for v in plb.get_fignums():
          plb.figure(v)
          plb.savefig('zfigure%d.png' % v)
          img = cv2.imread('zfigure%d.png' % v)
          path = 'filtered_images'
          cv2.imwrite(os.path.join(path , 'zfigure%d.png') %v,img)
          cv2.waitKey(0)
        plb.close('all')
        image_folder = 'filtered_images'
        video_name = 'filter_video.avi'
    
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
    
    
    
def butter_lowpass(cutoff, sample_rate, data,order=6):
 """
    Parameters
    ----------
    cutoff : int or float
        frequency in Hz that acts as cutoff for filter.
        All frequencies below cutoff are filtered out.

    sample_rate : int or float
        sample rate of the supplied signal
    order : int
        filter order, defines the strength of the roll-off
        around the cutoff frequency. Typically orders above 6
        are not used frequently.
        default : 2    
    Returns
    -------
    out : tuple
        numerator and denominator (b, a) polynomials
        of the defined Butterworth IIR filter.

    Examples
    --------
    we can specify the cutoff and sample_rate as ints or floats.

    >>> b, a = butter_highpass(cutoff = 2, sample_rate = 100, order = 2)
    >>> b, a = butter_highpass(cutoff = 4.5, sample_rate = 12.5, order = 5)
    """
 nyq = 0.5 * sample_rate
 normal_cutoff = cutoff / nyq
 b, a = butter(order, normal_cutoff, btype='low', analog=True)
 data = filtfilt(b, a, data)
 print("filtered")
 return data
       

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
    