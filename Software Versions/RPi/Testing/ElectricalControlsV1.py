#|*****************************************************************************|
#| Trencher BLDC Motor controls and sensor output
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
import spidev # To communicate with SPI devices

#Motor outputs
pwm = 3 #PWM pin
dir = 4 #non-PWM pin
rpm = 17

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

# Start SPI connection
spi = spidev.SpiDev() # Created an object
spi.open(0,0)

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

def ControlMotor(direction):# check if the switch is on and button is not pressed. If so, accelerate motor to max speed
    #start recording clock for tracking RPM data
    if direction == 'up' and pwm_value < 255:
        pwm_value += 5
    elif direction == 'down' and pwm_value > 0:
        pwm_value -= 5
    elif direction == 'space':
        print(f"Motor stopped")
        pwm_value = 0
    if pwm_value == 5:
         rpmStartTime = time.time()

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

def measureBucketRPMs():
    # Called if sensor output changes
    if (pi.read(rpm) == 0):
        sprocketCount += 1
    # if not GPIO.input(channel):
    #     # Magnet (LOW output)
    #     bucketCount += 1

    if (sprocketCount == sprocketRevs + 1): #plus 1 means it went full circle
        rpmEndTime = time.time()
        rpmDelta = (rpmEndTime - rpmStartTime)
        sprocketCount = 0
        bucketRPMs = 1.0 / ((rpmDelta) / 60.0)
        print(f"RPM: {bucketRPMs} {rpmEndTime}")
        rpmStartTime = time.time()

# Read MCP3008 data
def analogRead(channel):
  spi.max_speed_hz = 1350000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def measureMotorCurrent():
    maxVal = 0
    # delay(500)
    # digitalWrite(13, !digitalRead(13))
    for counter in range(1, samples):
        reading = analogRead(ampVin) # read the input pin
        if (reading > maxVal):
            maxVal = reading
    amps = ( (maxVal - zeroAmp) / halfAmp ) / 2.0
    print(f"Current: {amps} {time.time()}")

main()
