from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)

pin = 0

kit.frequency = 50
kit.servo[pin].set_pulse_width_range(400,2400)

delay = 1

run = True
while run:
    startTime = time.time()
    
    kit.servo[pin].angle = 90
    time.sleep(delay)

    currentTime = time.time()
    # print(currentTime - startTime)

print("Done")
