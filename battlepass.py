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
unexpected=False
input.FAILSAFE=False
auto.FAILSAFE=False

def printf(word):
    global mainExiting
    if not mainExiting:
        print("["+time.strftime("%Y-%m-%d %H:%M:%S")+"]",word)

def findUnexpected():
    global skipPrep, unexpected
    if auto.locateCenterOnScreen('game_end.png', confidence=0.5) is not None and skipPrep:
        skipPrep=False
        printf("game ended")
        resetCursor()
        return True
    if auto.locateCenterOnScreen('game_abort.png', confidence=0.5) is not None and skipPrep:
        skipPrep=False
        printf("game aborted")
        resetCursor()
        input.press('esc')
        return True
    if auto.locateCenterOnScreen('game_update.png', confidence=0.8) is not None:
        skipPrep=False
        if not unexpected:
            unexpected=True
            printf("game updated")
        position = auto.locateCenterOnScreen('game_leave.png', confidence=0.8)
        if position is None:
            position = auto.locateCenterOnScreen('game_exit.png', confidence=0.8)
        if position is not None:
            auto.moveTo(position[0],position[1],duration=random.uniform(1, 3),tween=auto.easeInOutQuad)
            time.sleep(random.uniform(0, 1))
            input.click()
        return True
    if auto.locateCenterOnScreen('game_disconnect.png', confidence=0.8) is not None:
        skipPrep=False
        if not unexpected:
            unexpected=True
            printf("game disconnnected")
        position = auto.locateCenterOnScreen('game_exit.png', confidence=0.8)
        if position is not None:
            auto.moveTo(position[0],position[1],duration=random.uniform(1, 3),tween=auto.easeInOutQuad)
            time.sleep(random.uniform(0, 1))
            input.click()
        return True
    return False

def findGame():
    global started, skipPrep, unexpected
    gameHWND=win32gui.FindWindow(0, "Call of Duty®: Modern Warfare®")
    platHWND=win32gui.FindWindow(0, "Battle.net")
    if not platHWND:
        stop("Battle.net not running, exiting...")
    if not gameHWND:
        printf("Game not running, booting...")
        skipPrep=False
        gameSwitched=False
        while not win32gui.FindWindow(0, "Call of Duty®: Modern Warfare®"):
            if started:
                notFound=True
                position = auto.locateCenterOnScreen('plat_identify.png', confidence=0.8)
                if position is not None:
                    gameSwitched=True
                    notFound=False
                else:
                    gameSwitched=False
                position = auto.locateCenterOnScreen('plat_switch.png', confidence=0.8)
                if position is not None and not gameSwitched:
                    auto.moveTo(position[0],position[1],duration=random.uniform(1, 3),tween=auto.easeInOutQuad)
                    time.sleep(random.uniform(0, 1))
                    input.click(clicks=3, duration=1)
                    notFound=False
                position = auto.locateCenterOnScreen('plat_start.png', confidence=0.8)
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
                promptHWND=win32gui.FindWindow(0, "设置为最佳设置？")
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
            time.sleep(0.1)
        resetCursor()
        unexpected=False
    else:
        win32gui.ShowWindow(gameHWND, win32con.SW_SHOWDEFAULT)
        findUnexpected()
    win32gui.ShowWindow(platHWND, win32con.SW_SHOWMINIMIZED)

def resetControl():
    input.keyUp('w')
    input.keyUp('s')
    input.keyUp('a')
    input.keyUp('d')
    input.keyUp('shift')
    input.mouseUp()

def resetCursor():
    centerPos=win32api.GetSystemMetrics(0)//2,win32api.GetSystemMetrics(1)//2
    if auto.position() != centerPos:
        auto.moveTo(centerPos[0],centerPos[1], duration=random.uniform(0.5,1), tween=auto.easeInOutQuad)

def stop(exitWord):
    global started, mainExiting
    resetControl()
    printf(exitWord)
    mainExiting=True
    started=False
    time.sleep(1)

def stopError(e):
    stop("Error '" +  ("Unknown" if not str(type(e).__name__) else str(type(e).__name__)+": "+str(e)) + "' occured, exiting...")

def on_press(key):
    global started, skipPrep
    if (key == keyboard.Key.f5):
        if not started:
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
        stop("exiting...")
        return False

def keyBoardListener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def startListener():
    global started, mainExiting
    while not mainExiting:
        if started:
            mainLoop()
        time.sleep(0.1)

def moveMouse(duration):
    xOffSet = random.randint(-2,2)
    yOffSet = random.randint(-1,1)
    for _ in range(int(duration*1000)):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, xOffSet, yOffSet, 0, 0)

def randKey():
    for _ in range (4):
        seed = random.randint(0,3)
        if seed == 0:
            input.keyUp('s')
            input.keyDown('w')
            time.sleep(random.uniform(0.1,0.2))
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
    global skipPrep, maxnum, started, mainExiting
    i=1
    while True:
        if not started or mainExiting:
            break
        findGame()
        if skipPrep:
            break
        position = auto.locateCenterOnScreen(str(i)+'.png', confidence=0.8)
        if position is not None:
            auto.moveTo(position[0],position[1],duration=random.uniform(1, 3),tween=auto.easeOutQuad)
            time.sleep(random.uniform(0, 1))
            input.click(clicks=3, duration=1)
            if i == maxnum:
                skipPrep=True
                printf("game started")
                break
        else:
            if i >= maxnum:
                i = 0
                resetCursor()
        i += 1
        time.sleep(0.1)

def mainLoop():
    global started, skipPrep, mainExiting
    while True:
        try:
            gamePrep()
            if not started or mainExiting:
                break
            randKey()
            time.sleep(random.uniform(0, 3))
            input.press('space')
            time.sleep(random.uniform(0, 3))
            input.press('c')
            time.sleep(random.uniform(1, 2))
            input.press('space')
            moveMouse(round(random.uniform(0, 4),3))
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
            printf("Failsafe detected, resetting...")
            resetCursor()
            continue
        except Exception as e:
            stopError(e)

if __name__ == '__main__':
    print("[BattlePasser Version 1.21]")
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
                except Exception as e:
                    stopError(e)
                    noError=False
                    break
        maxnum = int(filelist[-1][:-4])
    except IndexError:
        stop("Picture identifier missing, exiting...")
        noError=False
    except Exception as e:
        stopError(e)
        noError=False
    if noError:
        for i in range(1, maxnum+1):
            if not path.exists(str(i)+".png"):
                stop("Picture identifier '"+str(i)+".png' missing, exiting...")
                noError=False
                break
    if not path.exists("game_end.png") and noError:
        stop("Game ending picture identifier 'game_end.png' missing, exiting...")
        noError=False
    if not path.exists("game_abort.png") and noError:
        stop("Game aborting picture identifier 'game_abort.png' missing, exiting...")
        noError=False
    if not path.exists("game_update.png") and noError:
        stop("Game updating picture identifier 'game_update.png' missing, exiting...")
        noError=False
    if not path.exists("game_disconnect.png") and noError:
        stop("Game disconnecting picture identifier 'game_disconnect.png' missing, exiting...")
        noError=False
    if not path.exists("game_leave.png") and noError:
        stop("Game leaving picture identifier 'game_leave.png' missing, exiting...")
        noError=False
    if not path.exists("game_exit.png") and noError:
        stop("Game exiting picture identifier 'game_exit.png' missing, exiting...")
        noError=False
    if not path.exists("plat_identify.png") and noError:
        stop("Battle.net game identifying picture identifier 'plat_identify.png' missing, exiting...")
        noError=False
    if not path.exists("plat_switch.png") and noError:
        stop("Battle.net game switching picture identifier 'plat_switch.png' missing, exiting...")
        noError=False
    if not path.exists("plat_start.png") and noError:
        stop("Battle.net game starting picture identifier 'plat_start.png' missing, exiting...")
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