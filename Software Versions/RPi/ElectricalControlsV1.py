#|*****************************************************************************|
#| Trencher BLDC Motor controls and sensor output
#|   Currently, motor is controlled via 3 external periherals:
#|     Push button: Toggles motor stopping and starting
#|     Switch: Changes rotation of motor
#|     Potentiometer: Changes speed of motor
#| Author: Conor Porter
#| Last Modified: 02/23/2021
#|*****************************************************************************|

import os         #importing os library so as to communicate with the system
import time     #importing time library to make Rpi wait because its too impatient
os.system ("sudo pigpiod") #Launching GPIO library
import pigpio #importing GPIO library
import time
import datetime
# import RPi.GPIO as GPIO
from pynput import keyboard

#Motor outputs
pwm = 12 #PWM pin
dir = 27 #non-PWM pin
rpm = 17 #non-PWM pin

#Current Sensor input
ampVin = 3 #analog pin: potentiometer wiper (middle terminal) connected to analog pin 3
potPin = 2 #analog pin: potentiometer for controlling speed
reading = 0 # variable to store the value read
maxVal = 0
samples = 1000 # how many samples per reading

#constants for converting amp sensor reading
zeroAmp = 513
halfAmp = 7

#Motor control variables
pwm_value = 0 #relates to speed of motor

#RPM data variables
rpmStartTime = 0 #keeps track of clock
bucketRPMs = 0 #placeholder for final converted value
sprocketCount = 0 #keep track of how many go by
sprocketRevs = 4 #number of revolutions needed for full chain revolution

#Pi specific variables
pi = pigpio.pi()
#initialize outputs
pi.set_mode(pwm, pigpio.OUTPUT)
pi.set_mode(dir, pigpio.OUTPUT)
pi.set_mode(rpm, pigpio.INPUT)



# GPIO.setmode(GPIO.BCM)
# GPIO.setup(17 , GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.add_event_detect(17, GPIO.BOTH, callback=measureBucketRPMs, bouncetime=200)

def main():

    # Get initial reading
    # measureBucketRPMs(17)

    #start keyboard listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread

    while True:
        pi.write(dir, 0)
        pi.set_servo_pulsewidth(pwm, pwm_value)
        measureBucketRPMs()
        measureMotorCurrent()

def on_press(key):
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['up', 'down', 'space']:  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        print('Key pressed: ' + k)
        controlMotor(k)

main()
