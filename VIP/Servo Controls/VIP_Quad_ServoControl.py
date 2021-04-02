from adafruit_servokit import ServoKit
import time
import math as m
import pygame
import csv

kit = ServoKit(channels = 16)
kit.frequency = 50

# CSV File name to pull angle values from
fileName = '/home/pi/Documents/Pygame-Mechanisms-Projects-master/VIP/Normal Walking Gaits/03312021_v2.csv'

# Standing Positions
fileName = '/home/pi/Documents/Pygame-Mechanisms-Projects-master/VIP/Standing Positions/03312021.csv'

# Front left 3 servos, front right 3 servos, etc
FL = []
FR = []
RL = []
RR = []
# All 12 servos
servos = []

# Angle offsets based on installment configurations
thighOffset = 180
calfOffset = 180
hipOffset = -90

# Empty lists to be filled with angle values from csv file
hipThetas = []
thighThetas = []
calfThetas = []

# Open csv fil and take all angle values from three rows and append them to appropriate theta lists
with open(fileName, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    for line in csv_reader:
        thighThetas.append((int(float(line[3]))))
        calfThetas.append(int(float(line[4])))
        hipThetas.append(int(float(line[5])))

print("Thigh: " + str(thighThetas))
print("Calf " + str(calfThetas))
print("Hip: " + str(hipThetas))


# Creating Servo Class
class Servo:
    def __init__(self, pin, thetas, offset, leg, inverted_angle = False):
        # Set Servo Pin to OUTPUT, Freq to 50HZ
        self.pin = pin
        self.thetas = thetas
        self.offset = offset
        self.leg = leg
        self.inverted_angle = inverted_angle
        self.angle = 0
        self.index = 0
        kit.servo[self.pin].set_pulse_width_range(400, 2400)

        # Append Servo to Servo Lists
        self.leg.append(self)
        servos.append(self)
        
    # Convert Angle value to Duty and sets the servo angle
    def setAngle(self, angle):
        if self.inverted_angle:
            kit.servo[self.pin].angle = 180 - (angle - self.offset)
        else:
            kit.servo[self.pin].angle = angle - self.offset

    # Calculates the angle the servo should be set to using linear interpolation between two adjacent angle values in theta list
    # self.index is the index the servo should be referencing from theta list
    # when self.index is not a whole number, it linear interpolates between list element before and after current index value
    # Ex: index = 2.5 -> indexLow = 2, indexHigh = 3, if thetas[2] = 10 and thetas[3] = 20, self.theta = 15
    def calculateAngle(self, speed):
        self.index += speed
        if self.index > len(self.thetas) - 1:
            self.index -= len(self.thetas)

        indexLow = m.floor(self.index)
        indexHigh = m.ceil(self.index + 0.0001)

        # If index is a whole number, indexHigh still has to be nex number, hence the +0.0001 so it rounds up
        if indexHigh > len(self.thetas) - 1:
            indexHigh -= len(self.thetas)

        thetaLow = self.thetas[indexLow]
        thetaHigh = self.thetas[indexHigh]

        # Linear interpolation
        self.angle = thetaLow + (((self.index - indexLow) * (thetaHigh - thetaLow)) / (indexHigh - indexLow))


# Take away jitter
def deJitter(delay):
    time.sleep(delay)

    for servo in servos:
        pass
        
    time.sleep(delay * 2)


# Calculates anlgle values for each servo and adjusts them using setAngle method
def iterateServos(speed):
    for servo in servos:
        servo.calculateAngle(speed)
        servo.setAngle(servo.angle)

    deJitter(0.01)


# Should be used after a walking method is used (trot, saunter) in order to set the legs to a proper initial configuration
def initiateServos():
    for servo in servos:
        servo.calculateAngle(0)
        servo.setAngle(servo.angle)
    deJitter(0.2)


# Front two legs in sync, offset from rear two legs by half a cycle
def trot():
    findex = 0
    rindex = findex + m.floor(len(hipThetas) / 2)
    for servo in FL:
        servo.index = findex
    for servo in FR:
        servo.index = findex
    for servo in RL:
        servo.index = rindex
    for servo in RR:
        servo.index = rindex
    initiateServos()


# All four legs offset by a quarter of a cycle
def saunter():
    frindex = 0
    flindex = m.floor(len(hipThetas) / 4)
    rrindex = m.floor(len(hipThetas) / 2)
    rlindex = m.floor((3 / 4) * len(hipThetas))
    for servo in FL:
        servo.index = flindex
    for servo in FR:
        servo.index = frindex
    for servo in RL:
        servo.index = rlindex
    for servo in RR:
        servo.index = rrindex
    initiateServos()


def gallop():
    index1 = 0
    index2 = m.floor(len(hipThetas) / 2)
    for servo in FL:
        servo.index = index1
    for servo in FR:
        servo.index = index2
    for servo in RL:
        servo.index = index2
    for servo in RR:
        servo.index = index1
    initiateServos()


def uniform():
    index = 0
    for servo in servos:
        servo.index = 0
    initiateServos()


# Set Up Servo
servoFLH = Servo(0, hipThetas, hipOffset, FL)
servoFLT = Servo(1, thighThetas, thighOffset + 10, FL, True)
servoFLC = Servo(2, calfThetas, calfOffset - 10, FL)

servoRLH = Servo(4, hipThetas, hipOffset - 15, RL)
servoRLT = Servo(5, thighThetas, thighOffset + 7, RL, True)
servoRLC = Servo(6, calfThetas, calfOffset - 10, RL)

servoFRH = Servo(8, hipThetas, hipOffset + 10, FR, True)
servoFRT = Servo(9, thighThetas, thighOffset - 7, FR)
servoFRC = Servo(10, calfThetas, calfOffset, FR, True)

servoRRH = Servo(12, hipThetas, hipOffset + 10, RR, True)
servoRRT = Servo(13, thighThetas, thighOffset - 5, RR)
servoRRC = Servo(14, calfThetas, calfOffset, RR, True)

trot()
speed = 1
while True:
    startTime = time.time()

    iterateServos(speed)

    currentTime = time.time()
    # print(currentTime - startTime)
servoFLH.pwmPin.stop()
servoFLT.pwmPin.stop()
servoFLC.pwmPin.stop()
GPIO.cleanup()






 
 