from __future__ import division
from rpi_ws281x import *
import multiprocessing as mp
from ctypes import Structure, c_int

import picamera
import picamera.array
import numpy as np

#number of lights on each side
TOP_LIGHTS = 35
SIDE_LIGHTS = 21

#pixels of edges of image
CAMERA_TOP = 51
CAMERA_BOT = 169
CAMERA_LT = 31
CAMERA_RT = 250
CAMERA_LB = 5
CAMERA_RB = 285

TOP_COUNT = CAMERA_RT-CAMERA_LT
RIGHT_COUNT = int(105/3)
LEFT_COUNT = int(78/3)
BOT_COUNT = CAMERA_RB - CAMERA_LB
TOTAL_LIGHTS = (TOP_LIGHTS+SIDE_LIGHTS)*2

#data structure to store pixel
class Pixel(Structure) :
    _fields_=[('r',c_int), ('g',c_int), ('b', c_int)]

class MyAnalysis(picamera.array.PiRGBAnalysis):
    def __init__(self, camera, topRow, botRow, leftCol, rightCol):
        super(MyAnalysis, self).__init__(camera)
        self.topRow = topRow
        self.botRow = botRow
        self.leftCol = leftCol
        self.rightCol = rightCol

    def analyse(self, a):
        #get 
        self.topRow[:] = a[CAMERA_TOP,CAMERA_LT:CAMERA_RT].flatten()[:]
        self.botRow[:] = a[CAMERA_BOT ,CAMERA_LB:CAMERA_RB].flatten()[:]
        #print(len(np.diagonal((a[80:175,7:50])).flatten()))

        self.rightCol[:] = np.diagonal(np.fliplr(a[CAMERA_TOP:CAMERA_BOT,CAMERA_RT:CAMERA_RB])).flatten()[:]
        #print("right",len(np.diagonal(np.fliplr(a[CAMERA_TOP:CAMERA_BOT,CAMERA_RT:CAMERA_RB])).flatten()))
        self.leftCol[:] = np.diagonal(a[CAMERA_TOP:CAMERA_BOT,CAMERA_LB:CAMERA_LT]).flatten()[:]
        #print("left",len(np.diagonal(a[CAMERA_TOP:CAMERA_BOT,CAMERA_LB:CAMERA_LT]).flatten()))

def getTopRight(topInput, rightInput, output) :
    while True :
        #print(rightInput[0], rightInput[35], rightInput[70])
        for i in range(0,TOP_LIGHTS) :
            val = int((TOP_COUNT)/(0.0+TOP_LIGHTS) * i)*3

            output[i+SIDE_LIGHTS].r = int((topInput[val]+topInput[val+1])/2)
            output[i+SIDE_LIGHTS].g = int((topInput[val+TOP_COUNT]+topInput[val+TOP_COUNT+1])/2)
            output[i+SIDE_LIGHTS].b = int((topInput[val+(2*TOP_COUNT)]+topInput[val+(2*TOP_COUNT+1)])/2)
            print(topInput[val], " ",topInput[val+TOP_COUNT], " ", topInput[val+(2*TOP_COUNT)])
        for i in range(SIDE_LIGHTS) :
            output[i+TOP_LIGHTS+SIDE_LIGHTS].r = int(rightInput[i])
            output[i+TOP_LIGHTS+SIDE_LIGHTS].g = int(rightInput[i+RIGHT_COUNT])
            output[i+TOP_LIGHTS+SIDE_LIGHTS].b = int(rightInput[i+(RIGHT_COUNT*2)])
def getBotLeft(botInput, leftInput, output) :
    while True :
        for i in range(0,TOP_LIGHTS) :
            val = int((BOT_COUNT)/(0.0+TOP_LIGHTS) * i)*3
            output[TOTAL_LIGHTS-1-i].r = int((botInput[val]+botInput[val+3]+botInput[val+6])/3)
            output[TOTAL_LIGHTS-1-i].g = int((botInput[val+1]+botInput[val+BOT_COUNT+4]+botInput[val+BOT_COUNT+7])/3)
            output[TOTAL_LIGHTS-1-i].b = int((botInput[val+2]+botInput[val+5]+botInput[val+8])/3)
    
        for i in range(0,SIDE_LIGHTS) :
            output[i].r = int(leftInput[i])
            output[i].g = int(leftInput[i+LEFT_COUNT])
            output[i].b = int(leftInput[i+(LEFT_COUNT*2)])

def setColors(strip, input, size) :
    while True :
        x = 23
        print(input[x].r, " ", input[x].g, " ", input[x].b)
        for i in range(size) :
            strip.setPixelColor(i, Color(input[i].r, input[i].g, input[i].b))
        strip.show()