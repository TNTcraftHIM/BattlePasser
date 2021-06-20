from pynput import keyboard
from sys import exit
from os import system
import builtins
import threading
import pydirectinput as input
import pyautogui as auto
import win32con, win32api
import random
import time

exiting=False
started=False
skipPrep=False
input.FAILSAFE=False
maxnum=0

def stop(word):
    print(word)
    system("pause")
    exit()

def on_press(key):
    global started, exiting
    if (key == keyboard.Key.f5):
        started=True
        print("starting...")
    elif (key == keyboard.Key.f6):
        started=False
        print("stopping...")
    elif (key == keyboard.Key.f7):
        started=False
        exiting=True
        exit()

def keyBoardListener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def startListener():
    global started, exiting
    while True:
        if exiting:
            stop("exiting...")
        if started:
            mainLoop()
        time.sleep(0.1)

def moveMouse(duration):
    xOffSet = random.randint(-2,2)
    yOffSet = random.randint(-1,1)
    for _ in range(duration*1000):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, xOffSet, yOffSet, 0, 0)

def randKey():
    input.keyUp('w')
    input.keyUp('a')
    input.keyUp('s')
    input.keyUp('d')
    for _ in range (4):
        seed = random.randint(0,3)
        if seed == 0:
            input.keyUp('s')
            input.keyDown('w')
            input.press('shift')
        if seed == 1:
            input.keyUp('d')
            input.keyDown('a')
        if seed == 2:
            input.keyUp('w')
            input.keyDown('s')
        if seed == 3:
            input.keyUp('a')
            input.keyDown('d')
        time.sleep(random.uniform(0.1,0.3))

def gamePrep():
    global skipPrep, maxnum, started
    i=0
    while not skipPrep:
        if not started:
            break
        position = auto.locateCenterOnScreen(str(i)+'.png', confidence=0.8)
        if position is not None:
            auto.moveTo(position[0],position[1],duration=random.randint(1, 3))
            time.sleep(random.randrange(0, 1))
            input.click(clicks=3, duration=1)
            if i == maxnum:
                skipPrep=True
                print("game started")
                break
        else:
            #print("not found")
            if i >= maxnum:
                i = -1
        i += 1

def mainLoop():
    global started, skipPrep
    while True:
        gamePrep()
        if not started:
            break
        position = auto.locateCenterOnScreen('-1.png', confidence=0.5)
        if position is not None:
            skipPrep=False
            continue
        randKey()
        time.sleep(random.randrange(0, 3))
        input.press('space')
        time.sleep(random.randrange(0, 3))
        input.press('c')
        time.sleep(random.randrange(1, 2))
        input.press('space')
        moveMouse(random.randint(0, 4))
        input.rightClick()
        time.sleep(random.randrange(0, 1))
        input.mouseDown()
        time.sleep(random.randrange(0, 4))
        input.mouseUp()
        time.sleep(random.randrange(0, 1))
        input.rightClick()
        time.sleep(random.randrange(0, 1))
        input.press('1')
        time.sleep(random.randrange(0, 3))

if __name__ == '__main__':
    try:
        maxnum = int(builtins.input("Enter the max number of picture identifiers (start from 0):"))
    except:
        stop("Please enter integer only, exiting...")
    if maxnum < 0:
        stop("You would need at least one identifier, exiting...")
    print("Press F5/F6/F7 to start/stop/exit")
    thread1=threading.Thread(target=keyBoardListener)
    thread1.start()
    thread2=threading.Thread(target=startListener)
    thread2.start()