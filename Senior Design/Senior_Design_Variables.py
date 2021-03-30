import math as m

linkLength1 = 3 * 12
linkLength2 = 3 * 12
actuator1_connection = linkLength1 / 2
linkage2_connection = linkLength2 / 4
actuator1_ground = [-16, -12]
actuator2_ground = [-1 * 12, 0]

# Min distance, max distance for the 1 inch, 2 inch, etc
actuator_limits = [[8.87, 9.87], [9.87, 11.87], [10.87, 13.87], [11.87, 15.87], [13.87, 19.87], [15.87, 23.87],
                       [16.87, 25.87], [17.87, 27.87], [19.87, 31.87], [21.87, 25.87], [23.87, 39.87], [25.87, 43.87],
                       [27.87, 47.87], [31.87, 55.87], [37.87, 67.87], [47.87, 87.87]]

# I just took out the stroke lengths that we definitely would never use (1-4, 23-40)
actuator_limits = [[13.87, 19.87], [15.87, 23.87],
                       [16.87, 25.87], [17.87, 27.87], [19.87, 31.87], [21.87, 25.87], [23.87, 39.87], [25.87, 43.87],
                       [27.87, 47.87]]

# I just took out the stroke lengths that we definitely would never use (1-4, 23-40)
actuator_limits = [[17.87, 27.87], [27.87, 47.87]]

patient_weight = 200
patient_angle = -m.pi / 2

work_space = [18, 18]
work_space_origin = [18, -18]

ground_positions_range = [18, 48]
ground_positions_origin = [-24, work_space_origin[1] - work_space[1]]

