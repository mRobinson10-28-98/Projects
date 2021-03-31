import sys
import pygame as py
import math as m

sys.path.insert(0, '/Pygame Mechanism Module/Pygame-Mechanism-Module')

import Variables as v
from Point import Point
from CsvWriter import CsvWriter
from CsvReader import CsvReader
from Five_Bar_3DoF_Leg import Leg
from Screen import Screen
from Button import Button
from Mouse import Mouse

'''
fileWriteName = '/home/pi/Documents/Motor Control/Normal Walking Gait/03032021.csv'
fileReadName = '/home/pi/Documents/Motor Control/Normal Walking Gait/03032021.csv'
'''

fileWriteName = 'C:/Users/drunk/PycharmProjects/pythonProject/Pygame Mechanism Module/Pygame Mechanisms Projects/Csv Files/Walking Gaits/03132021.csv'
fileReadName = 'C:/Users/drunk/PycharmProjects/pythonProject/Pygame Mechanism Module/Pygame Mechanisms Projects/Csv Files/Walking Gaits/03132021.csv'

screen_dim_pix = 800
screen_dim_inch = 24

# Screen multiplier
multiplier = 1

# Link Lengths in inches (Thigh, crank, coupler, follower, calf, hip)
linkLength1 = 4.5
linkLength2 = 1.5
linkLength3 = 4.5
linkLength4 = 1.5
linkLength5 = 6.5 - linkLength4
linkLengthhip = 2

linkLength1 *= multiplier
linkLength2 *= multiplier
linkLength3 *= multiplier
linkLength4 *= multiplier
linkLength5 *= multiplier
linkLengthhip *= multiplier

screen = Screen(screen_dim_pix, screen_dim_inch)

leg1 = Leg(screen, linkLength1, linkLength2, linkLength3,
           linkLength4, linkLength5, linkLengthhip)

csvWriter = CsvWriter(screen, fileWriteName, leg1)
csvReader = CsvReader(screen, fileReadName)

mouse = Mouse(screen, 0, 0)

Point(screen, screen.inches_to_pixels(screen.origin_x), screen.inches_to_pixels(screen.origin_y + 3), 0, screen.points)

run = True
test = False
while run:
    screen.initialize()

    # Mouse Position
    keys = py.key.get_pressed()
    mouse_press = py.mouse.get_pressed()
    mouse_pos = py.mouse.get_pos()
    mouse.function(mouse_pos, mouse_press, leg1.lhipz)

    screen.check_key_commands(keys)

    # Calculate all position and force variables based on current point
    leg1.create()

    screen.draw([[leg1]])

py.quit()


