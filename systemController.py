import multiprocessing as mp
from rpi_ws281x import *
import picamera
import picamera.array
import numpy as np
#import lights
import lights_desktop as lights

topRow = mp.Array('i',range(lights.TOP_COUNT*3), lock = False)
botRow = mp.Array('i', range(lights.BOT_COUNT*3), lock = False )
leftCol = mp.Array('i', range(lights.LEFT_COUNT*3), lock = False)
rightCol = mp.Array('i',range(lights.RIGHT_COUNT*3), lock = False)

LED_COUNT = lights.TOTAL_LIGHTS
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

output = mp.Array(lights.Pixel, LED_COUNT, lock = False)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

strip.begin()


t = mp.Process(target = lights.getTopRight, args = (topRow, rightCol, output))
b = mp.Process(target = lights.getBotLeft, args = (botRow, leftCol, output))
s = mp.Process(target = lights.setColors, args = (strip, output, LED_COUNT))

t.start()
b.start()
s.start()

with picamera.PiCamera() as camera:
    camera.resolution = (288, 176)
    camera.framerate = 30
    output = lights.MyAnalysis(camera, topRow, botRow, leftCol, rightCol)
    camera.start_recording(output, 'rgb')
    try:
        while True : 
            camera.wait_recording(1)
    finally:
        camera.stop_recording()
