from pynput import keyboard

def on_press(key):
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['space', 'down', 'up']:  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        print('Key pressed: ' + k)
        # return False  # stop listener; remove this if want more keys
# while True:
listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread
    # listener.join()  # remove if main thread is polling self.keys

while True:
    x = 1
