# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 00:51:25 2019

@author: Daan
"""
import pygame as pg
import numpy as np
import matplotlib.pyplot as plt
from PGFunc import RandomSignal

#settings
fps = 60
duration = 60 #[s]
#aspectRatio = 4/3
screenSize=[640,480]
targetSize = 46
refSize = 36
predSize = 26
lowestFreq  = 2   #[rad/s]
highestFreq = 6  #[rad/s]

#Todo in an approximate ordinal scale
#Implement dynamics settings
#Implement (basic arrow) controls
#Implement other display types
#Implement predictor
#Clean up random signal class/function code
#Implement setting an exact forcing function (and steal the one from HMSLab)
#Implement ----\  type function for frequency (line with steep drop at end)
#Implement Settings GUI
#Implement tracking/showing of score
#Implement second dimension


dynamics = 0 #0 - Proportional (position)
             #1 - Integrator (speed)
             #2 - Double Integrator (acceleration)
             #3 - Triple Integrator (change in acceleration)
             
display  = 0 #0 - Error
             #1 - Pursuit
             #2 - Shows signal

freqList = [2,3,4,5,6,7] #rad/s
lowMagFreqList = [8,9,10] #rad/s
lowMagMag = 0.25

#useful variables
xc = screenSize[0]/2 #centre X
yc = screenSize[1]/2 #centre Y
stepSize = 1/fps


highestMag = 0.8 * screenSize[0]/2

#forcingFunction = RandomSignal(duration,lowestFreq=lowestFreq,highestFreq=highestFreq,highestMag=highestMag, random = 1)
forcingFunction = RandomSignal(duration,lowMagFreqList=lowMagFreqList,freqList=freqList,highestMag=highestMag, lowMagMag=lowMagMag)
forcingFunction.plot()

pg.init()

#colors
green = pg.Color(0,200,0)    
white = pg.Color(255,255,255)
yellow = pg.Color(255,255,0)

#initialize stuff
screen = pg.display.set_mode(screenSize)
clock = pg.time.Clock()
font = pg.font.SysFont("arial",30)

ref = pg.Rect((xc-refSize/2,yc-refSize/2),(refSize,refSize))
pred = pg.Rect((xc-predSize/2,yc-predSize/2),(predSize,predSize))

tc = 0 #keep track of current time

running = True
while running: 
    #Check for quit
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    #Reset screen to black
    screen.fill((0,0,0))
        
    #Progress time and draw fps counter
    dt = clock.tick(fps) #in ms
    tc+=(dt/1000) 
    realFPS = clock.get_fps()
    fpsRend = font.render(str(int(realFPS)), True, white)
    screen.blit(fpsRend,(50,50))
    
    #get forcing function value
    xt=forcingFunction.getAtTime(tc,scale=1)
    
    #replace target object with object at new position
    target = pg.Rect((xt+xc-targetSize/2,yc-targetSize/2),(targetSize,targetSize))        

    #Draw target
    pg.draw.rect(screen,green,target,1)
    
    #Draw ref    
    pg.draw.rect(screen,white,ref,1)
    #Draw pred
#    pg.draw.rect(screen,yellow,pred,1)
    
    pg.display.flip()

#close stuff
pg.display.quit()
pg.quit()
    

            



