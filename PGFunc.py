# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 02:18:55 2019

@author: d
"""
import numpy as np

def getRandomSignal(lowestFreq,highestFreq,duration,highestMag,stepSize=0.01):
    fundamentalFrequency = 2 * np.pi/duration #rad/s
    
    maxk = int(highestFreq/fundamentalFrequency)
    mink = int(lowestFreq/fundamentalFrequency)
    
    #setup matrices
    a = np.zeros(maxk+1)
    b = np.zeros(maxk+1)
    
    #Get random coefficient for set frequencies
    a[mink:maxk] = np.random.uniform(-1,1,maxk-mink)
    b[mink:maxk] = np.random.uniform(-1,1,maxk-mink)

    t = np.arange(duration,step=stepSize)
    x = np.zeros(duration*int(1/stepSize))
    
    for i in range(len(t)):
        for k in range(maxk-mink):
            x[i] += a[k]*np.cos(k*fundamentalFrequency*t[i])+b[k]*np.sin(k*fundamentalFrequency*t[i])
    
    #scale to highest mag
    scaleFact = highestMag / max(abs(x))
    x = x * scaleFact
    return x,t,a,b,fundamentalFrequency,scaleFact
    
def ft(a,b,t,fundamentalFrequency):
    x = 0
    for k in range(len(a)):
        x += a[k]*np.cos(k*fundamentalFrequency*t)+b[k]*np.sin(k*fundamentalFrequency*t)
    return x