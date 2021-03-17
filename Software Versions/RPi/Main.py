#|*****************************************************************************|
#| Trencher BLDC Motor controls and sensor output
#| Author: Conor Porter
#| Last Modified: 02/23/2021
#|*****************************************************************************|

import os
os.system ("sudo pigpiod") #Launching GPIO library
from pynput import keyboard
from Peripherals import *
from Connections import *

# sv = 12 #PWM pin
# fr = 27 #non-PWM pin
# brk = 22 #non-PWM pin
# rpm = 17 #non-PWM pin
# pi = pigpio.pi()
# speed = 0
# m = Motor(pi, sv, fr, brk)
# c = CurrentSensor(0)
# h = HallEffectSensor(pi, rpm, 4)
port = 3000
noneCount = 0 #timeout counter
timeout = 6
c = None
cs = None
message = None
foundPort = False
while not foundPort:
    try:
        c = ClientConnection(port)
        c.listenAndAccept(10)
        cs = SocketReader(c.client())
        message = cs.receive()
        if (message.type() == 'init' and message.contents() == 'hello'):
            foundPort = True
        w = SocketWriter(c.client())
        w.send(message)
    except:
        port += 1


while True:
    # amps = c.measureCurrent(1000)
    # rpms = h.measureRPMs()

    message = cs.receive()
    if (message != None):
        noneCount = 0
        print(message.type())
        if (message.type() == "string" and message.content() == "Shutdown"):
            cs.getSocket().close()
            print("listening")
            c.listenAndAccept(5)
            cs = SocketReader(c.client())
        if (message.type() == "string"):
            print(message.content())
    else:
        noneCount += 1
        print("None!")
    if (noneCount >= timeout):
        c.close()
        exit(0)

def ControlMotor(command):# check if the switch is on and button is not pressed. If so, accelerate motor to max speed
    #start recording clock for tracking RPM data
    if command == 'up' and speed < 255:
        m.speedUp(5)
    elif command == 'down' and speed > 0:
        m.slowDown(5)
    elif command == 'w':
        m.forward()
    elif command == 's':
        m.reverse()
    elif command == 'space':
        m.setSpeed(0)
    elif command == 'esc':
        m.hardStop()
