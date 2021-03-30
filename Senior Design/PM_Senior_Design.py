import sys
import pygame as py
import math as m

import Senior_Design_Variables as sd
from Iterator import Iterator

sys.path.insert(0, 'C:/Users/drunk/PycharmProjects/pythonProject/Pygame Mechanism Module/Pygame-Mechanism-Module')

import Variables as v
from Point import Point
from CsvWriter import CsvWriter
from CsvReader import CsvReader
from Two_Bar_Planar_Linear_Actuator_Arm import Arm
from Screen import Screen
from Button import Button
from Mouse import Mouse

'''
fileWriteName = '/home/pi/Documents/Motor Control/Normal Walking Gait/03032021.csv'
fileReadName = '/home/pi/Documents/Motor Control/Normal Walking Gait/03032021.csv'
'''

fileWriteName = 'C:/Users/drunk/PycharmProjects/pythonProject/Pygame Mechanism Module/Pygame Mechanisms Projects/Hip Curves/03132021.csv'
fileReadName = 'C:/Users/drunk/PycharmProjects/pythonProject/Pygame Mechanism Module/Pygame-Mechanism-Module/Hip Curves/03132021.csv'
fileWriteNameIterator = 'C:/Users/drunk/PycharmProjects/pythonProject/Pygame Mechanism Module/Pygame Mechanisms Projects/Senior Design/Achievable Mechanisms/03262021.csv'

screen_dim_pix = 800
screen_dim_inch = 150

v.time_delay = 0

screen = Screen(screen_dim_pix, screen_dim_inch)

arm1 = Arm(screen, sd.linkLength1, sd.linkLength2, sd.actuator1_ground,
           sd.actuator2_ground, sd.actuator1_connection, sd.linkage2_connection)

csvWriter = CsvWriter(screen, fileWriteName, arm1)
csvReader = CsvReader(screen, fileReadName)

mouse = Mouse(screen, 0, 0)

Point(screen, screen.inches_to_pixels(screen.origin_x + sd.linkLength1), screen.inches_to_pixels(screen.origin_y), 0, screen.points)

iterate = True
iterator = Iterator(screen, arm1)
csvWriterIterator = CsvWriter(screen, fileWriteNameIterator, iterator)

run = True
test = False
while run:
    screen.initialize()

    # Mouse Position
    keys = py.key.get_pressed()
    mouse_press = py.mouse.get_pressed()
    mouse_pos = py.mouse.get_pos()
    mouse.function(mouse_pos, mouse_press, 0)

    screen.check_key_commands(keys)

    if iterate:
        iterator.iterate_ground_positions()

        sd.work_space_origin = [12, -18]
        sd.ground_positions_origin = [-30, sd.work_space_origin[1] - sd.work_space[1]]
        iterator.iterate_ground_positions()

        sd.work_space_origin = [6, -18]
        sd.ground_positions_origin = [-36, sd.work_space_origin[1] - sd.work_space[1]]
        iterator.iterate_ground_positions()

        sd.work_space_origin = [0, -18]
        sd.ground_positions_origin = [-42, sd.work_space_origin[1] - sd.work_space[1]]
        iterator.iterate_ground_positions()
        break

    # Calculate all position and force variables based on current point
    arm1.create()
    arm1.kinetics(sd.patient_weight, sd.patient_angle)
    screen.draw([[arm1]])

py.quit()


