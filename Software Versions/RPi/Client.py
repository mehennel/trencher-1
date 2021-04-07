#|*****************************************************************************|
#| Trencher BLDC Motor controls and sensor output
#| Author: Conor Porter
#| Last Modified: 03/31/2021
#|*****************************************************************************|

from pynput import keyboard
from Connections import *
import sys
from KeyboardInput import KeyboardInput


def ControlMotor(command):# check if the switch is on and button is not pressed. If so, accelerate motor to max speed
    #start recording clock for tracking RPM data
    message = Message('string', command)
    w.send(message)


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
        ControlMotor(k)

host = sys.argv[1]
port = 3000

foundPort = False
while not foundPort:
    try:
        s = ServerConnection(host, port)
        w = SocketWriter(s)
        message = Message('init', 'hello')
        w.send(message)
        cs = SocketReader(s)
        message = cs.receive()
        if (message.type() == 'init' and message.contents() == 'hello'):
            foundPort = True
    except:
        port += 1

kb = KeyboardInput(mc)

while (kb.acceptingInput()):
    message = cs.receive()
    if (message.type() == 'r'):
        print(message.contents())
