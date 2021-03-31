import math as m
import Senior_Design_Variables as sd

'''
*****************************************************************
Specify the path to the pygame mechanisms module.
The Iterator class needs to have a specific screen and the mechanism.

The create_points method creates an array of points, starting at the top left corner at position sd.work_space_origin
    which is an x,y position in inches relative to the mechanism origin. The dimensions of the array is specified by 
    sd.work_space, also in inches and is the (width, height) of the array. The create_points method is called in 
    iterate_points.
    
The iterate_points method looks at the sd.actuator_limits list and (essentially) determines the actuator stroke length. 
    Really, the list is comprised of 2 dimensional lists which denote the lower and upper bounds for the length of 
    each linear actuator. iterate_points defines these limits for actuator 1, then iterates through all the limits for 
    actuator 2, each iteration checking the array of points and determining if the actuators fall within that range and 
    don't surpass 800 lb. The last if statement checks to see if the bottom of the mechanism goes below 10 inches below 
    the array, since the array should be a foot above the ground (minimum sitting hip height for 6 yo kids). If any 
    condition is not met, the achievable parameter is set to false. IF the array is finished and achievable is true, add 
    this configuration to the list. The iterate_points method is called in iterate_ground_positions.
    
    
    
    
*****************************************************************
'''

import sys
sys.path.insert(0, 'C:/Users/drunk/PycharmProjects/pythonProject/Pygame Mechanism Module/Pygame-Mechanism-Module')

from Point import Point
import Variables as v

class Iterator:
    def __init__(self, screen, arm):
        self.screen = screen
        self.arm = arm
        self.achievable_mechanisms = []
        self.achievable = True

    def create_points(self):
        self.screen.points = []
        for x_pos in range(int(self.screen.inches_to_pixels(sd.work_space_origin[0] + self.screen.origin_x)),
                           int(self.screen.inches_to_pixels(sd.work_space_origin[0] + sd.work_space[0] + self.screen.origin_x)),
                           20):
            for y_pos in range(int(self.screen.inches_to_pixels(self.screen.origin_y - sd.work_space_origin[1])),
                               int(self.screen.inches_to_pixels(
                                   self.screen.origin_y - sd.work_space_origin[1] + sd.work_space[1])), 20):
                Point(self.screen, x_pos, y_pos, 0, self.screen.points)

    def iterate_points(self):
        for limits1 in sd.actuator_limits:
            actuator1_lims = limits1
            for limits2 in sd.actuator_limits:
                actuator2_lims = limits2
                self.achievable = True
                self.create_points()
                for index in range(len(self.screen.points)):
                    self.screen.point_index = index
                    self.screen.initialize()
                    self.arm.create()
                    self.arm.kinetics(sd.patient_weight, sd.patient_angle)
                    self.screen.draw([[self.arm]])
                    if actuator1_lims[0] <= self.arm.actuator1_length <= actuator1_lims[1] and abs(self.arm.actuator1_force) <= 800:
                        if actuator2_lims[0] <= self.arm.actuator2_length <= actuator2_lims[1] and abs(self.arm.actuator2_force) <= 800:
                            if self.screen.origin_y - self.arm.actuator2_joint[1] >= sd.work_space_origin[1] - sd.work_space[1] - 10:
                                self.screen.current_point.color = v.green
                            else:
                                self.achievable = False
                                break
                        else:
                            self.achievable = False
                            break
                    else:
                        self.achievable = False
                        break

                    if index == len(self.screen.points) - 1 and self.achievable:
                        self.achievable_mechanisms.append((self.arm.actuator1_ground, self.arm.actuator2_ground, actuator1_lims[2], actuator2_lims[2]))
                        print("Actuator 1 ground, Actuator 2 Ground, Act1 stroke, Act2 stroke: ")
                        print(self.arm.actuator1_ground, self.arm.actuator2_ground, actuator1_lims[2], actuator2_lims[2])

    def iterate_ground_positions(self):
        increment = 2
        for x_pos2 in range(sd.ground_positions_origin[0], sd.ground_positions_origin[0] + sd.ground_positions_range[0],increment):
            for y_pos2 in range(sd.ground_positions_origin[1], sd.ground_positions_origin[1] + sd.ground_positions_range[1],increment):
                self.arm.actuator2_ground = [self.screen.origin_x + x_pos2, self.screen.origin_y - y_pos2]
                for x_pos1 in range(sd.ground_positions_origin[0], sd.ground_positions_origin[0] + sd.ground_positions_range[0], increment):
                    for y_pos1 in range(sd.ground_positions_origin[1], sd.ground_positions_origin[1] + sd.ground_positions_range[1], increment):
                        self.arm.actuator1_ground = [self.screen.origin_x + x_pos1, self.screen.origin_y - y_pos1]
                        self.iterate_points()