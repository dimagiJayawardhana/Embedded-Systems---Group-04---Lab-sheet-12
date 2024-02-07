# Import necessary libraries
from Adafruit_AMG88xx import Adafruit_AMG88xx
import pygame
import os
import math
import time
import numpy as np
from scipy.interpolate import griddata
from colour import Color

# Define constants
MINTEMP = 26  # Low range of the sensor (blue on screen)
MAXTEMP = 32  # High range of the sensor (red on screen)
COLORDEPTH = 1024  # Number of color values

# Set up the framebuffer for Pygame
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()

# Initialize the sensor
sensor = Adafruit_AMG88xx()

# Define grid points
points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]

# Define screen dimensions
height = 240
width = 240

# Define color range
blue = Color("indigo")
colors = list(blue.range_to(Color("red"), COLORDEPTH))
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]

# Set up display
displayPixelWidth = width / 30
displayPixelHeight = height / 30
lcd = pygame.display.set_mode((width, height))

# Initialize display
lcd.fill((255,0,0))
pygame.display.update()
pygame.mouse.set_visible(False)
lcd.fill((0,0,0))
pygame.display.update()

# Utility functions
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Let the sensor initialize
time.sleep(.1)

# Main loop
while True:
    # Read the pixels from the sensor
    pixels = sensor.readPixels()
    # Map pixel values to color range
    pixels = [map(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]
    # Perform interpolation
    bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')
    # Draw pixels on screen
    for ix, row in enumerate(bicubic):
        for jx, pixel in enumerate(row):
            pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, COLORDEPTH - 1)], (displayPixelHeight * ix, displayPixelWidth * jx, displayPixelHeight, displayPixelWidth))
    pygame.display.update()
