from pynput import keyboard
from sys import exit
from os import system, path
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
auto.FAILSAFE=False
maxnum=0

def resetControl():
    input.keyUp('w')
    input.keyUp('s')
    input.keyUp('a')
    input.keyUp('d')
    input.keyUp('shift')
    input.mouseUp()

def resetCursor():
    auto.moveTo(win32api.GetSystemMetrics(0)//2,win32api.GetSystemMetrics(1)//2, duration=random.uniform(1,3), tween=auto.easeOutQuad)

def stop(word):
    resetControl()
    print("["+time.strftime("%Y-%m-%d %H:%M:%S")+"]",word)
    system("pause")
    exit()

def on_press(key):
    global started, exiting, skipPrep
    if (key == keyboard.Key.f5):
        started=True
        print("["+time.strftime("%Y-%m-%d %H:%M:%S")+"]","starting...")
    elif (key == keyboard.Key.f6):
        started=False
        skipPrep=False
        resetControl()
        print("["+time.strftime("%Y-%m-%d %H:%M:%S")+"]","stopping...")
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
    i=1
    while not skipPrep:
        if not started:
            break
        position = auto.locateCenterOnScreen(str(i)+'.png', confidence=0.8)
        if position is not None:
            auto.moveTo(position[0],position[1],duration=random.uniform(1, 3),tween=auto.easeInOutQuad)
            time.sleep(random.uniform(0, 1))
            input.click(clicks=3, duration=1)
            if i == maxnum:
                skipPrep=True
                print("["+time.strftime("%Y-%m-%d %H:%M:%S")+"]","game started")
                break
        else:
            if i >= maxnum:
                i = 0
        i += 1
        time.sleep(0.1)

def mainLoop():
    global started, skipPrep
    while True:
        try:
            gamePrep()
            if not started:
                break
            if auto.locateCenterOnScreen('0.png', confidence=0.5) is not None:
                skipPrep=False
                print("["+time.strftime("%Y-%m-%d %H:%M:%S")+"]","game ended")
                continue
            if auto.locateCenterOnScreen('-1.png', confidence=0.5) is not None:
                skipPrep=False
                print("["+time.strftime("%Y-%m-%d %H:%M:%S")+"]","game aborted")
                input.press('esc')
                continue
            randKey()
            time.sleep(random.uniform(0, 3))
            input.press('space')
            time.sleep(random.uniform(0, 3))
            input.press('c')
            time.sleep(random.uniform(1, 2))
            input.press('space')
            moveMouse(random.randint(0, 4))
            input.rightClick()
            time.sleep(random.uniform(0, 1))
            input.mouseDown()
            time.sleep(random.uniform(0, 4))
            input.mouseUp()
            time.sleep(random.uniform(0, 1))
            input.rightClick()
            time.sleep(random.uniform(0, 1))
            input.press('1')
            time.sleep(random.uniform(0, 3))
        except (auto.FailSafeException, input.FailSafeException):
            print("["+time.strftime("%Y-%m-%d %H:%M:%S")+"]","Failsafe detected, resetting cursor...")
            resetCursor()
            continue
        except Exception as e:
            stop("Error: " +  ("Unknown" if not str(e) else str(e)) + " occured, exiting...")

if __name__ == '__main__':
    print("[BattlePasser Version 1.0]")
    try:
        maxnum = int(builtins.input("Enter the max number of picture identifiers (start from 1):"))
    except:
        stop("Please enter integer only, exiting...")
    if maxnum < 1:
        stop("Please enter at least 1 identifier, exiting...")
    for i in range(1, maxnum+1):
        if not path.exists(str(i)+".png"):
            stop("Picture identifiers filename mismatch, exiting...")
    if not path.exists("0.png"):
        stop("Game ending picture identifier missing, exiting...")
    if not path.exists("-1.png"):
        stop("Game aborting picture identifier missing, exiting...")
    print("Press F5/F6/F7 to start/stop/exit")
    input.FAILSAFE=False
    auto.FAILSAFE=False
    thread1=threading.Thread(target=keyBoardListener)
    thread1.start()
    thread2=threading.Thread(target=startListener)
    thread2.start()