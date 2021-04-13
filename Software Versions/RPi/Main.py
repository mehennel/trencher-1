#|*****************************************************************************|
#| Trencher BLDC Motor controls and sensor output
#| Author: Conor Porter
#| Last Modified: 03/31/2021
#|*****************************************************************************|

import os
os.system ("sudo pigpiod") #Launching GPIO library
from Peripherals import *
from Connections import *

def ControlMotor(command):# check if the switch is on and button is not pressed. If so, accelerate motor to max speed
    #start recording clock for tracking RPM data
    if command.contents() == 'up':
        m.speedUp(5)
    elif command.contents() == 'down':
        m.slowDown(5)
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
# rpm = 17 #non-PWM pin
pi = pigpio.pi()
# speed = 0
m = Motor(pi, sv, fr, brk)
# c = CurrentSensor(0)
# h = HallEffectSensor(pi, rpm, 4)
port = 3000
c = None
r = None
message = None
foundPort = False
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

while True:
    # amps = c.measureCurrent(1000)
    # rpms = h.measureRPMs()

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
            exit(0)
