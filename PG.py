# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 00:51:25 2019

@author: Daan
"""
import pygame as pg
import numpy as np
import matplotlib.pyplot as plt
from PGFunc import RandomSignal, ForcingFunction

#settings
fps = 60
duration = 60 #[s]

#aspectRatio = 4/3
screenSize=[640,480]
targetSize = 46
refSize = 36
predSize = 26

#Todo in an approximate ordinal scale
#Tune (basic arrow) controls
#Implement other display types
#Implement predictor
#Implement ----\  type function for frequency (line with steep drop at end)
#Implement Settings GUI
#Implement tracking/showing of score
#Implement second dimension


dynamics = 2 #0 - Proportional (position)
             #1 - Integrator (speed)
             #2 - Double Integrator (acceleration)
             #3 - Triple Integrator (change in acceleration)
             
display  = 0 #0 - Compensatory
             #1 - Pursuit
             #2 - Shows signal

predictor = 1   #0 no predictor
                #1 single predictor
                #2 secondary predictor

predTime = 0.5 #seconds

controls = 0 #0Keyboard

freqList = [2,3,4,5,6,7] #rad/s
lowMagFreqList = [8,9,10] #rad/s
lowMagMag = 0.25

#useful variables
xc = screenSize[0]/2 #centre X
yc = screenSize[1]/2 #centre Y
stepSize = 1/fps


scaleToMag = 0.8 

forcingFunction = ForcingFunction(randomizePhase=0,scaleToMag=scaleToMag)
duration = forcingFunction.duration
#lowestFreq  = 2   #[rad/s]
#highestFreq = 6  #[rad/s]
#forcingFunction = RandomSignal(duration,lowMagFreqList=lowMagFreqList,freqList=freqList,highestMag=highestMag, lowMagMag=lowMagMag)
#forcingFunction.plot()

pg.init()

#initialize stuff
screen = pg.display.set_mode(screenSize)
clock = pg.time.Clock()
font = pg.font.SysFont("arial",30)
userInputX = 0

tc = 0 #keep track of current time
ts = 0 #time since start running signal
xf = forcingFunction.getAtTime(0) * screenSize[0]/2 #starting point of forcing function

xi = 0 #pos start at 0
vi = 0 #velocity start at 0
ai = 0 #acceleration start at 0
a2i = 0 #change in accleration 
userInputH = 0 #Horizontal Input gain

xGain = 10*screenSize[0]/640 #scale to screen size, ten is there to increase sensitivity
yGain = 10*screenSize[1]/480 #scale to screen size, ten is there to increase sensitivity

countDown = 5 #count 5 sec before start

inpLim = 15 # Max in or output magnitude


pg.key.set_repeat(50)

xiHist=[]
xrHist=[]
tcHist=[]

running = True
while running:
    #Reset screen to black
    screen.fill((0,0,0))
    #Check for events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                userInputH += -0.1
            if event.key == pg.K_RIGHT:
                userInputH += 0.1
                
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                userInputH = 0
            if event.key == pg.K_RIGHT:
                userInputH = 0

    if dynamics == 0:
        userInputX += userInputH
    if dynamics > 0:
        userInputX += userInputH
        if userInputX < -inpLim:
            userInputX = -inpLim
        if userInputX > inpLim:
            userInputX = inpLim

    inpRend = font.render(str(round(userInputX,2)), True, pg.Color('white'))
    screen.blit(inpRend,(xc,screenSize[1]-50))
    
#    draw input bar
    barLength = screenSize[0]/4
    barHeight = 22
    barframe = pg.Rect((xc-barLength/2,screenSize[1]-50-barHeight/2),(barLength,barHeight))

    pg.draw.rect(screen,pg.Color('white'),barframe,1)
            
    
    #Progress time and draw fps counter
    dTicks = clock.tick(fps) #in ms
    dt = dTicks/1000
    tc += dt
    realFPS = clock.get_fps()
    fpsRend = font.render(str(int(realFPS)), True, pg.Color('white'))
    screen.blit(fpsRend,(50,50))
     
    if countDown > 0:
        countingDown = font.render(str(round(countDown)), True, pg.Color('white'))
        screen.blit(countingDown,(xc,yc))
        countDown -= dt
        userInputX = 0
        userInputY = 0
        
    else: #countdown over, start program
        ts+=dt
        #get forcing function value
    xf=forcingFunction.getAtTime(ts) * screenSize[0]/2
    xf=0
    if dynamics == 0: #pos
        xi = userInputX*xGain
        xiT = font.render("Xi: "+str(round(xi)), True, pg.Color('white'))
        screen.blit(xiT,(50,screenSize[1]-50))

    elif dynamics == 1:
        vi = userInputX*xGain
        xi += vi * dt
        xiT = font.render("Xi: "+str(round(xi)), True, pg.Color('white'))
        screen.blit(xiT,(50,screenSize[1]-50))
        if predictor == 1:
            xps = vi * predTime 
            
    elif dynamics == 2:
        ai = userInputX*xGain
        vi += ai * dt
        xi += vi * dt
        xiT = font.render("Xi: "+str(round(xi)), True, pg.Color('white'))
        screen.blit(xiT,(50,screenSize[1]-50))
        if predictor == 1:
            xps = 0.5 * ai * predTime**2 + vi * predTime
            
    elif dynamics == 3:
        a2i = userInputX*xGain
        ai += a2i * dt
        vi += ai * dt
        xi += vi * dt
        xiT = font.render("Xi: "+str(round(xi)), True, pg.Color('white'))
        screen.blit(xiT,(50,screenSize[1]-50))
        if predictor == 1:
            xps = (1/6) * a2i **3 + 0.5 * ai * predTime**2+ vi * predTime 
        
    if countDown < 0:
        tcHist.append(tc)
        xiHist.append(-xi)
        xrHist.append(xf)
        
    if display == 0: #compensatory
        xt = 0
        xr = xf
        xp = xps
        
    elif display == 1: #pursuit
        xt = xf
        xr = 0
        xp = xps

    #replace target object with object at new position    
    ref = pg.Rect((xi + xr + xc-refSize/2,yc-refSize/2),(refSize,refSize))
    target = pg.Rect((  xt + xc-targetSize/2,yc-targetSize/2),(targetSize,targetSize))
#    pred2 = pg.Rect((xp+xc-predSize/2,yc-predSize/2),(predSize,predSize))

    #Draw target
    pg.draw.rect(screen,pg.Color('white'),target,1)
    
    #Draw ref    
    pg.draw.rect(screen,pg.Color('green'),ref,1)

    #Draw pred
    if predictor > 0:
        pred = pg.Rect((xi+xp+xc-predSize/2,yc-predSize/2),(predSize,predSize))
        pg.draw.rect(screen,pg.Color('yellow'),pred,1)
    
    pg.display.flip()

    if tc > duration:
        running = False

pg.display.quit()
pg.quit()

plt.plot(tcHist,xiHist)
plt.plot(tcHist,xrHist)
plt.show()

    

            



