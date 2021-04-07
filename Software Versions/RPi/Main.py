#|*****************************************************************************|
#| Trencher BLDC Motor controls and sensor output
#| Author: Conor Porter
#| Last Modified: 03/31/2021
#|*****************************************************************************|

# import os
# os.system ("sudo pigpiod") #Launching GPIO library
from pynput import keyboard
from Peripherals import *
from Connections import *


sv = 12 #PWM pin
fr = 27 #non-PWM pin
brk = 22 #non-PWM pin
rpm = 17 #non-PWM pin
pi = pigpio.pi()
# speed = 0
# m = Motor(pi, sv, fr, brk)
# c = CurrentSensor(0)
h = HallEffectSensor(pi, rpm, 4)
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
        foundPort = True
    except:
        port += 1

print(f"listening on port {port}")
c.listenAndAccept(10)
cs = SocketReader(c.client())
message = cs.receive()
print(f"message received: {message.contents()}")
# if (message.type() == 'init' and message.contents() == 'hello'):
w = SocketWriter(c.client())
w.send(message)

print(f"port found: {port}")

while True:
    # amps = c.measureCurrent(1000)
    # rpms = h.measureRPMs()

    message = cs.receive()
    print(message)
    if (message != None):
        print(message.contents())
        if (message.type() == "m"):
            ControlMotor(message)
        if (message.tyoe() == "r"):
            rpms = h.measureRPMs()
            w.send(Message('r', rpms))
        if (message.type() == "string" and message.contents() == "Shutdown"):
            exit(0)

def ControlMotor(command):# check if the switch is on and button is not pressed. If so, accelerate motor to max speed
    #start recording clock for tracking RPM data
    if command.contents() == 'up' and speed < 255:
        m.speedUp(5)
    elif command.contents() == 'down' and speed > 0:
        m.slowDown(5)
    elif command == 'w':
        m.forward()
    elif command.contents() == 's':
        m.reverse()
    elif command.contents() == 'space':
        m.setSpeed(0)
    elif command.contents() == 'esc':
        m.hardStop()
