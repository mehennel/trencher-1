#|*****************************************************************************|
#| Trencher BLDC Motor controls and sensor output
#| Author: Conor Porter
#| Last Modified: 02/23/2021
#|*****************************************************************************|

import os
os.system ("sudo pigpiod") #Launching GPIO library
from pynput import keyboard
from CurrentSensor import CurrentSensor
from HallEffectSensor import HallEffectSensor
from Motor import Motor

sv = 12 #PWM pin
fr = 27 #non-PWM pin
brk = 22 #non-PWM pin
rpm = 17 #non-PWM pin
pi = pigpio.pi()
speed = 0
m = Motor(pi, sv, fr, brk)

def main():
    c = CurrentSensor(0)
    h = HallEffectSensor(pi, rpm, 4)

    #start keyboard listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread

    while True:
        amps = c.measureCurrent(1000)
        rpms = h.measureRPMs()

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

def on_press(key):
    # if key == keyboard.Key.esc:
    #     return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['up', 'down', 'w', 's', 'space', 'esc']:  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        print('Key pressed: ' + k)

main()
