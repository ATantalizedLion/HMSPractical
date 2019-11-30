# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 02:18:55 2019

@author: d
"""
import numpy as np
import matplotlib.pyplot as plt

class RandomSignal():
        
        def generateRandomCoeff(self):
            #f = f0 * k
            maxk = int(self.highestFreq/self.fundamentalFrequency)
            mink = int(self.lowestFreq/self.fundamentalFrequency)
                        
            #setup matrices
            self.a = np.zeros(maxk+1)
            self.b = np.zeros(maxk+1)
        
            #Get random coefficient for set frequencies
            self.a[mink:maxk] = np.random.uniform(-1,1,maxk-mink)
            if self.cosines == 1:
                self.b[mink:maxk] = np.random.uniform(-1,1,maxk-mink)

        def genFromList(self):
            #f = f0 * k
            klist = []
            for f in self.freqList:
                klist.append(int(f/self.fundamentalFrequency))
                
            self.a = np.zeros(len(klist))
            self.b = np.zeros(len(klist))
            
            for i in range(len(self.a)):
                self.a[0:len(klist)] = np.random.uniform(-1,1,len(klist))
                if self.cosines == 1:
                    self.b[0:len(klist)] = np.random.uniform(-1,1,len(klist))
                
        def genSignal(self):
            self.t = np.arange(self.duration,step=self.stepSize)
            self.x = np.zeros(self.duration*int(1/self.stepSize))
            
            for i in range(len(self.t)):
                for k in range(len(self.a)):
                    self.x[i] += self.a[k]*np.sin(k*self.fundamentalFrequency*self.t[i])+self.b[k]*np.cos(k*self.fundamentalFrequency*self.t[i])
            
            #scale to highest mag
            self.scaleFactor = self.highestMag / max(abs(self.x))
            self.x = self.x * self.scaleFactor

            return self.x,self.t
            
        def getAtTime(self,t,scale=1):
            y = 0
            for k in range(len(self.a)):
                    y += self.a[k]*np.sin(k*self.fundamentalFrequency*t)+self.b[k]*np.cos(k*self.fundamentalFrequency*t)
            if scale == 1:
                return y * self.scaleFactor
            else:
                return y
        
        def plot(self):
            plt.plot(self.t,self.x)
            plt.show()
        
        def __init__(self,
                     duration,
                     highestMag=1,
                     stepSize=0.01,
                     
                     freqList = [], 
                     lowestFreq=0,
                     highestFreq=0,
                     
                     #Settings you don't really need to touch
                     cosines=0,
                     random=0,
                     autoGenSignal=1):
            #signal properties
            self.duration = duration        
            self.stepSize = stepSize
            self.highestMag = highestMag
            
            #Top 2 or bottom 1 is used
            self.lowestFreq = lowestFreq
            self.highestFreq = highestFreq
            self.freqList = freqList
            
            #generation settings
            self.random = random
            self.cosines = cosines
            self.autoGenSignal = autoGenSignal
            
            self.fundamentalFrequency = 2 * np.pi/duration #rad/s
            
            if len(self.freqList)!=0:
                self.genFromList()
                if self.autoGenSignal == 1:
                    self.genSignal()        
                
            if random == 1:
                self.generateRandomCoeff()
                if self.autoGenSignal == 1:
                    self.genSignal()                              