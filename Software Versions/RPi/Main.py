#|*****************************************************************************|
#| Trencher BLDC Motor controls and sensor output
#| Author: Conor Porter
#| Last Modified: 04/12/2021
#|*****************************************************************************|

import os
os.system ("sudo pigpiod") #Launching GPIO library
from Peripherals import *
from Connections import *
import time
import threading

def ControlMotor(command):# check if the switch is on and button is not pressed. If so, accelerate motor to max speed
    #start recording clock for tracking RPM data
    if command.contents() == 'up':
        m.speedUp(2.55)
    elif command.contents() == 'down':
        m.slowDown(2.55)
    elif command.contents() == 'w':
        m.forward()
    elif command.contents() == 's':
        m.reverse()
    elif command.contents() == 'space':
        m.setSpeed(0)
    elif command.contents() == 'esc':
        m.hardStop()

sv = 12 #PWM pin
fr = 27 #non-PWM pin
brk = 22 #non-PWM pin
rpm = 17 #non-PWM pin
pi = pigpio.pi()
speed = 0
m = Motor(pi, sv, fr, brk)
curr = CurrentSensor(0)
h = HallEffectSensor(pi, rpm, 4)
port = 3000
c = None
r = None
message = None
foundPort = False
closing = False
while not foundPort:
    try:
        c = ClientConnection(port)
        print(f"listening on port {port}")
        c.listenAndAccept(10)
        r = SocketReader(c.client())
        message = r.receive()
        if (message.type() == 'init' and message.contents() == 'hello'):
            foundPort = True
    except:
        port += 1


print(f"message received: {message.contents()}")
w = SocketWriter(c.client())
w.send(message)

rpmFile = open("rpm_output.txt", "a")
ampFile = open("current_output.txt", "a")
startTime = time.time()

def collectData():
    while not closing:
        rpms = h.measureRPMs()
        amps = curr.measureCurrent(100);
        t = time.time() - startTime
        if (rpms == 0):
            rpmFile.write(f"{t} {rpms}\n")
        ampFile.write(f"{t} {amps}\n")
    rpmFile.close()
    ampFile.close()


thread = threading.Thread(target = collectData)
thread.start()

while True:
    #amps = curr.read()
    #rpms = h.measureRPMs()
    #print(f"Amps: {amps}")

    message = r.receive()
    # print(message)
    if (message != None):
        # print(message.contents())
        if (message.type() == "m"):
            ControlMotor(message)
        # if (message.type() == "r"):
        #     rpms = h.measureRPMs()
        #     w.send(Message('r', rpms))
        if (message.type() == 's' and message.contents() == "Shutdown"):
            c.close()
            closing = True
            exit(0)

