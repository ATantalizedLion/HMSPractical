# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 00:51:25 2019

@author: Daan
"""
import pygame as pg
import numpy as np
import matplotlib.pyplot as plt








lowestFreq =1
highestFreq =10
duration = 120 #[s]
stepSize = 0.1
highestMag = 0.9
fundamentalFrequency = 2*np.pi/duration #rad/s

#setup matrices
a = np.zeros((duration))
t = np.arange(duration,step=stepSize)

#Get random coefficient for set frequencies
a[lowestFreq:highestFreq] = np.random
b[lowestFreq:highestFreq] = 
c[lowestFreq:highestFreq] = 


#    numpy.fft.ifft(a, n=None, axis=-1, norm=None)
#    a[0] should contain the zero frequency term,
#    a[1:n//2] should contain the positive-frequency terms,
#    a[n//2 + 1:] should contain the negative-frequency terms, in increasing order starting from the most negative frequency.
#    n = Length of the transformed axis of the output.
s = np.fft.ifft(a,(len(t))) #get signal
s = s.real #dispose of imag part
scaleFact = max(abs(s.real)) #scale magnitude to 1
s = highestMag * s / scaleFact #scale magnitude to give magnitude
    









#def getRandomSignal(lowestFreq, highestFreq, ,duration, stepSize=0.1, highestMag=1):
##    lowestFreq=1
##    highestFreq=10
##    duration = 120 #[s]
##    stepSize = 0.1
##    highestMag = 0.9
#    #setup matrices
#    a = np.zeros((duration))
#    t = np.arange(duration,step=stepSize)
#    
#    #Get random coefficient for set frequencies
#    a[lowestFreq:highestFreq] = np.random
#    b[lowestFreq:highestFreq] = 
#    c[lowestFreq:highestFreq] = 
#    
#    
#    #    numpy.fft.ifft(a, n=None, axis=-1, norm=None)
#    #    a[0] should contain the zero frequency term,
#    #    a[1:n//2] should contain the positive-frequency terms,
#    #    a[n//2 + 1:] should contain the negative-frequency terms, in increasing order starting from the most negative frequency.
#    #    n = Length of the transformed axis of the output.
#    s = np.fft.ifft(a,(len(t))) #get signal
#    s = s.real #dispose of imag part
##    scaleFact = max(abs(s.real)) #scale magnitude to 1
##    s = highestMag * s / scaleFact #scale magnitude to give magnitude
#    
#    return s,t
#
##settings
#lowestFreq=1
#highestFreq=10
#duration = 120 #[s]
#stepSize = 0.1
#highestMag = 0.9
#
#s,t = getRandomSignal(lowestFreq, highestFreq, duration, stepSize, highestMag)
#
##plt.plot(t,s)
##plt.show()
#
#sp = np.fft.rfft(s)
#freq = np.fft.rfftfreq(s.shape[-1])
#plt.plot(freq, sp.real, freq, sp.imag)
#plt.show()