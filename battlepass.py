from pynput import keyboard
from os import system, path, listdir, curdir
import threading
import pydirectinput as input
import pyautogui as auto
import win32con, win32api, win32gui
import random
import time

maxnum=0
mainExiting=False
started=False
skipPrep=False
input.FAILSAFE=False
auto.FAILSAFE=False

def printf(word):
    print("["+time.strftime("%Y-%m-%d %H:%M:%S")+"]",word)

def findGame():
    global started, skipPrep
    gameHWND=win32gui.FindWindow(0, "Call of Duty®: Modern Warfare®")
    platHWND=win32gui.FindWindow(0, "Battle.net")
    if not platHWND:
        stop("Battle.net not running, exiting...")
    if not gameHWND:
        printf("Game not running, booting...")
        gameSwitched=False
        while not win32gui.FindWindow(0, "Call of Duty®: Modern Warfare®"):
            try:
                if started:
                    notFound=True
                    position = auto.locateCenterOnScreen('-2.png', confidence=0.8)
                    if position is not None:
                        gameSwitched=True
                        notFound=False
                    else:
                        gameSwitched=False
                    position = auto.locateCenterOnScreen('-3.png', confidence=0.8)
                    if position is not None and not gameSwitched:
                        auto.moveTo(position[0],position[1],duration=random.uniform(1, 3),tween=auto.easeInOutQuad)
                        time.sleep(random.uniform(0, 1))
                        input.click(clicks=3, duration=1)
                        notFound=False
                    position = auto.locateCenterOnScreen('-4.png', confidence=0.8)
                    if position is not None and gameSwitched:
                        auto.moveTo(position[0],position[1],duration=random.uniform(1, 3),tween=auto.easeInOutQuad)
                        time.sleep(random.uniform(0, 1))
                        input.click(clicks=3, duration=1)
                        notFound=False
                    promptHWND=win32gui.FindWindow(0, "是否在安全模式下运行？")
                    if promptHWND:
                        win32gui.ShowWindow(promptHWND, win32con.SW_SHOWDEFAULT)
                        win32gui.SetForegroundWindow(promptHWND)
                        input.press('n')
                        notFound=False
                    if notFound:
                        win32gui.ShowWindow(platHWND, win32con.SW_SHOWDEFAULT)
                        win32gui.BringWindowToTop(platHWND)
                        win32gui.SetActiveWindow(platHWND)
                        win32gui.SetForegroundWindow(platHWND)
            except:
                stop("Game booting failed, exiting...")
            time.sleep(0.1)
        skipPrep=False
    win32gui.ShowWindow(platHWND, win32con.SW_SHOWMINIMIZED)
    win32gui.ShowWindow(gameHWND, win32con.SW_SHOWDEFAULT)

def resetControl():
    input.keyUp('w')
    input.keyUp('s')
    input.keyUp('a')
    input.keyUp('d')
    input.keyUp('shift')
    input.mouseUp()

def resetCursor():
    auto.moveTo(win32api.GetSystemMetrics(0)//2,win32api.GetSystemMetrics(1)//2, duration=random.uniform(1,3), tween=auto.easeOutQuad)

def stop(exitWord):
    global mainExiting
    resetControl()
    printf(exitWord)
    mainExiting=True
    time.sleep(1)

def on_press(key):
    global started, skipPrep
    if (key == keyboard.Key.f5):
        started=True
        printf("starting...")
    elif (key == keyboard.Key.f6):
        if started:
            started=False
            skipPrep=False
            resetControl()
            printf("stopping...")

def on_release(key):
    global started
    if key == keyboard.Key.f7:
        started=False
        stop("exiting...")
        return False

def keyBoardListener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def startListener():
    global started
    while True:
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
    while True:
        if not started:
            break
        findGame()
        if skipPrep:
            break
        position = auto.locateCenterOnScreen(str(i)+'.png', confidence=0.8)
        if position is not None:
            auto.moveTo(position[0],position[1],duration=random.uniform(1, 3),tween=auto.easeInOutQuad)
            time.sleep(random.uniform(0, 1))
            input.click(clicks=3, duration=1)
            if i == maxnum:
                skipPrep=True
                printf("game started")
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
                printf("game ended")
                continue
            if auto.locateCenterOnScreen('-1.png', confidence=0.5) is not None:
                skipPrep=False
                printf("game aborted")
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
            printf("Failsafe detected, resetting cursor...")
            resetCursor()
            continue
        except Exception as e:
            stop("Error: " +  ("Unknown" if not str(e) else str(e)) + " occured, exiting...")

if __name__ == '__main__':
    print("[BattlePasser Version 1.1]")
    noError=True
    try:
        filelist=listdir(curdir)
        for fichier in filelist[:]:
            if not(fichier.endswith(".png")):
                filelist.remove(fichier)
            else:
                try:
                    if int(fichier[:-4]) <= 0:
                        filelist.remove(fichier)
                except ValueError:
                    filelist.remove(fichier)
        maxnum = int(filelist[-1][:-4])
    except:
        stop("Reading filenames from folder failed, exiting...")
        noError=False
    if noError:
        for i in range(1, maxnum+1):
            if not path.exists(str(i)+".png"):
                stop("Picture identifier '"+str(i)+".png' missing, exiting...")
                noError=False
                break
    if not path.exists("0.png") and noError:
        stop("Game ending picture identifier '0.png' missing, exiting...")
        noError=False
    if not path.exists("-1.png") and noError:
        stop("Game aborting picture identifier '-1.png' missing, exiting...")
        noError=False
    if noError:
        if not path.exists("-2.png") or not path.exists("-3.png") or not path.exists("-4.png"):
            stop("Game rebooting picture identifier(s) '-2.png/-3.png/-4.png' missing, exiting...")
            noError=False
    if noError:
        print("Press F5/F6/F7 to start/stop/exit")
        input.FAILSAFE=False
        auto.FAILSAFE=False
        thread1=threading.Thread(target=keyBoardListener)
        thread1.daemon=True
        thread1.start()
        thread2=threading.Thread(target=startListener)
        thread2.daemon=True
        thread2.start()
    while True:
        if mainExiting:
            system("pause")
            break
        time.sleep(1)