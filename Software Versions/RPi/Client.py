#|*****************************************************************************|
#| Trencher BLDC Motor controls and sensor output
#| Author: Conor Porter
#| Last Modified: 02/23/2021
#|*****************************************************************************|

from pynput import keyboard
from Connections import *
import sys
#
host = sys.argv[1]
port = 3000

foundPort = False
while not foundPort:
    try:
        s = ServerConnection(host, port)
        w = SocketWriter(s)
        message = Message('init', 'hello')
        w.send(message)
        c = ClientConnection(port)
        c.listenAndAccept(10)
        cs = SocketReader(c.client())
        message = cs.receive()
        while (message == None):
            message = cs.receive()
        if (message.type() == 'init' and message.contents() == 'hello'):
            foundPort = True
    except:
        port += 1

#start keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread

while True:
    x = 0

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
