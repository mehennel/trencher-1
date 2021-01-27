import os         #importing os library so as to communicate with the system
import time     #importing time library to make Rpi wait because its too impatient
os.system ("sudo pigpiod") #Launching GPIO library
import pigpio #importing GPIO library

#Motor outputs
pwm = 3 #PWM pin
dir = 4 #non-PWM pin

#Button/switch inputs
stp = 2 #non-PWM pin
start = 7 #non-PWM pin

#Sonic sensor IO
trig = 9 #non-PWM pin
echo = 10 #non-PWM pin

#Current Sensor input
ampVin = 3 #analog pin: potentiometer wiper (middle terminal) connected to analog pin 3
potPin = 2 #analo pin: potentiometer for controlling speed
reading = 0 # variable to store the value read
potRead = 0
maxVal = 0
samples = 1000 # how many samples per reading

#constants for converting amp sensor reading
zeroAmp = 513
halfAmp = 7
amps = 0.0

#Motor control variables
potToPWM = 4.011764706 #conversion for controlling speed of motor (1k Ohm ~ 255)
pwm_value = 0 #relates to speed of motor
incomingByte = 0 # for incoming serial data
userInput = 0 #a number from the serial monitor
startState = 0 #for checking if motor must hard stop
toggleStop = 0 #for using button as a toggle switch
stopState = 0 #for checking if motor must start

#RPM data variables
rpmStartTime = NULL #keeps track of clock
rpmSamples = 8 #how many times to read ultrasonic sensor to get accurate value
prevDistance = 11 #for handling noise from ultrasonic sensor
bucketDistance = 10 #distance from sensor to buckets
bucketRPMs = 0 #placeholder for final converted value
bucketCount = 0 #keep track of how many go by

#value for buckets and chain for tracking RPMs
distBucketToBucket = 1 #1.5ft min
#495.3mm is center of sprocket to center of sprocket sprocket distance (7-8inch diameter sprocket)
# \/ roughly 5.8 ft of chain for the min \/ (93.5 links)
distTrackLength = 1
numberOfBuckets = 4

#Pi specific variables
pi = pigpio.pi()
#initialize outputs
pi.set_mode(pwm, pigpio.OUTPUT)
pi.set_mode(dir, pigpio.OUTPUT)
pi.set_mode(trig, pigpio.OUTPUT)
#initialize inputs
pi.set_mode(stp, pigpio.INPUT)
pi.set_mode(start, pigpio.INPUT)
pi.set_mode(echo, pigpio.INPUT)

def checkToStopMotor():
    # NOTE: will require modifcation when transistors are set up with EN and BRK to make hard stopping possible
    # read the state of the pushbutton value:
    stopState = pi.read(stp)
    # check if the pushbutton is pressed. If it is, stop the motor:
    if (stopState == 1):
        toggleStop = toggleStop ^ 1
        print("Motor stopped:", end = " ")
        print(toggleStop)
        pwm_value = 0
        while (pi.read(stp) == 1) #polling loop to wait for you to let off on the button

def checkToStartMotor():

    # read the state of the pushbutton value:
    startState = digitalRead(start)

    # check if the switch is on and button is not pressed. If so, accelerate motor to max speed
    if (toggleStop == 0):

        controlSpeed()
        #start recording clock for tracking RPM data
        if (rpmStartTime == NULL) rpmStartTime = millis()

def measureBucketRPMs():

    #trigger sonic sensor and record output
    float duration
    float distance = bucketDistance + 1
    for counter in range(0, rpmSamples - 1):

        digitalWrite(trig, LOW)
        delayMicroseconds(500)
        digitalWrite(trig, HIGH)
        delayMicroseconds(500)
        digitalWrite(trig, LOW)
        duration = pulseIn (echo, HIGH)
        if (distance > ( (duration/2)/29 )):
            distance = (duration/2)/29


    unsigned long rpmEndTime = millis()
    #if less than 10cm from dist sensor
    if (distance < bucketDistance && prevDistance > bucketDistance):

        Serial.print(distance)
        Serial.println(" cm")
        Serial.print(prevDistance)
        Serial.println(" prev")
        bucketCount += 1
        if (bucketCount == numberOfBuckets + 1): #plus 1 means it went full circle

            double rpmDelta = ( (float) (rpmEndTime - rpmStartTime) ) / 1000 #time in seconds
            bucketCount = 0
            bucketRPMs = 1.0 / ((rpmDelta) / 60.0)
            Serial.print("RPM: ")
            Serial.print(bucketRPMs)
            Serial.print(" ")
            Serial.println(millis())
            rpmStartTime = millis()


    prevDistance = distance

def measureMotorCurrent():

    maxVal = 0
    # delay(500)
    # digitalWrite(13, !digitalRead(13))
    for counter in range(1, samples):
        reading = analogRead(ampVin) # read the input pin
        if (reading > maxVal)

            maxVal = reading


    amps = ( ( ((double) maxVal) - ((double) zeroAmp) ) / ((double) halfAmp) ) / 2.0
    Serial.print("Current: ")
    Serial.print(amps)
    Serial.print(" ")
    Serial.println(millis())


def controlSpeed():

    potRead = analogRead(potPin)
    pwm_value = potRead / potToPWM



while True:
    pi.write(dir, 0)
    pi.set_servo_pulsewidth(pwm, pwm_value)

    #if button pressed, stop
    checkToStopMotor()
    #if button is not pressed, accelerate motor
    checkToStartMotor()
    #measure rotations per minute of the bucket track
    measureBucketRPMs()
    #measure current flowing through motor
    measureMotorCurrent()
