import keyboard
from time import sleep
import sys

running = True

while running:
    if keyboard.is_pressed("k"):
        sleep(1)
    elif keyboard.is_pressed('Esc'):
        sys.exit()
    else:
        print("hello")