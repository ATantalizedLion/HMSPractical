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
duration = 90 #[s]
screenSize=[640,480]
targetSize = 46
refSize = 36
predSize = 26
lowestFreq  = 2   #[rad/s]
highestFreq = 6  #[rad/s]

freqList = [2,3,4] #rad/s

#useful variables
xc = screenSize[0]/2 #centre X
yc = screenSize[1]/2 #centre Y
stepSize = 1/fps


highestMag = 0.8 * screenSize[0]/2

#forcingFunction = RandomSignal(lowestFreq,highestFreq,durations)
forcingFunction = RandomSignal(duration,freqList=freqList,highestMag=highestMag)

x = forcingFunction.x

pg.init()

#colors
green = pg.Color(0,200,0)    
white = pg.Color(255,255,255)
yellow = pg.Color(255,255,0)

#initialize stuff
screen = pg.display.set_mode(screenSize)
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms",30)

ref = pg.Rect((xc-refSize/2,yc-refSize/2),(refSize,refSize))
pred = pg.Rect((xc-predSize/2,yc-predSize/2),(predSize,predSize))

tc = 0

#plt.plot(t,x)
#plt.show()

running = True
while running: 
    #Check for quit
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    #Reset screen to black
    screen.fill((0,0,0))
        
    #Progress time
    dt = clock.tick(fps) #in ms
    realFPS = clock.get_fps()
    fpsRend = font.render(str(int(realFPS)), True, white)
    screen.blit(fpsRend,(50,50))
    
    tc+=(dt/100)
    
    xt=forcingFunction.getAtTime(tc,scale=1)
    
    target = pg.Rect((xt+xc-targetSize/2,yc-targetSize/2),(targetSize,targetSize))        

    #Draw target
    pg.draw.rect(screen,green,target,1)
    #Draw ref    
    pg.draw.rect(screen,white,ref,1)
    #Draw pred
#    pg.draw.rect(screen,yellow,pred,1)
    
#    fpscount = font.render(str(int(pg.time.Clock().get_fps())))

    pg.display.flip()

#close stuff
pg.display.quit()
pg.quit()
    

            



