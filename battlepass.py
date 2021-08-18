from pynput import keyboard
from os import system, path, listdir, curdir
import threading
import pydirectinput as input
import pyautogui as auto
import win32con, win32api, win32gui, win32process, win32ui
import random
import time
import ctypes

maxnum=0
mainExiting=False
started=False
skipPrep=False
unexpected=False
input.FAILSAFE=False
auto.FAILSAFE=False
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)

def printf(word):
    global mainExiting
    if not mainExiting:
        print("["+time.strftime("%Y-%m-%d %H:%M:%S")+"]",word)

def getGameHWND():
    pid = win32process.GetWindowThreadProcessId(win32gui.FindWindow(0, "Call of Duty®: Modern Warfare®"))[1]
    def callback (hwnd, hwnds):
        if win32gui.IsWindowVisible (hwnd) and win32gui.IsWindowEnabled (hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId (hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
        return True
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    if len(hwnds) > 0:
        return hwnds[0]
    else:
        return 0

def resizeGame():
    gameHWND=getGameHWND()
    nonGameHWND=win32gui.FindWindow(0, "Call of Duty®: Modern Warfare®")
    if gameHWND and gameHWND != nonGameHWND:
        if not win32gui.IsIconic(gameHWND):
            win32gui.ShowWindow(gameHWND, win32con.SW_MINIMIZE)
        win32gui.ShowWindow(gameHWND, win32con.SW_SHOWDEFAULT)
        win32gui.SetActiveWindow(gameHWND)
        if win32api.GetSystemMetrics(0) < 1920 or win32api.GetSystemMetrics(1) < 1080:
            return
        gameX, gameY, gameW, gameH = win32gui.GetWindowRect(gameHWND)
        if gameX==0 and gameY==0 and gameW == 1920 and gameH == 1080:
            return
        win32ui.CreateWindowFromHandle(gameHWND).ModifyStyle(win32con.WS_CAPTION, 0)
        win32gui.SetWindowPos(gameHWND, win32con.NULL, 0, 0, 1920,1080, win32con.SWP_FRAMECHANGED)
        x, y, _, h = win32gui.GetWindowRect(gameHWND)
        y=y+h//2
        currX, currY=auto.position()
        auto.click(x,y, duration=0.1)
        auto.moveTo(currX, currY)

def findUnexpected():
    global skipPrep, unexpected, started
    if skipPrep and started:
        if auto.locateCenterOnScreen('game_end.png', confidence=0.5) is not None or auto.locateCenterOnScreen('game_ended.png', confidence=0.5) is not None or auto.locateCenterOnScreen('game_ends.png', confidence=0.5) is not None:
            skipPrep=False
            printf("game ended")
            resetCursor()
            return
    if auto.locateCenterOnScreen('game_abort.png', confidence=0.7) is not None and started:
        if skipPrep:
            skipPrep=False
        printf("game aborted")
        resetCursor()
        input.press('esc')
        return
    if started:
        if auto.locateCenterOnScreen('game_update.png', confidence=0.8) is not None or auto.locateCenterOnScreen('game_updated.png', confidence=0.8) is not None:
            skipPrep=False
            position=None
            if not unexpected:
                unexpected=True
                printf("game updated")
            if started:
                position = auto.locateCenterOnScreen('game_leave.png', confidence=0.8)
            if position is None and started:
                position = auto.locateCenterOnScreen('game_quit.png', confidence=0.8)
            if position is not None and started:
                auto.moveTo(position[0],position[1],duration=random.uniform(1, 3),tween=auto.easeInOutQuad)
                time.sleep(random.uniform(0, 1))
                if auto.position()==(position[0],position[1]) and started:
                    input.click()
            return
    if auto.locateCenterOnScreen('game_disconnect.png', confidence=0.8) is not None and started:
        skipPrep=False
        position=None
        if not unexpected:
            unexpected=True
            printf("game disconnnected")
        if started:
            position = auto.locateCenterOnScreen('game_leave.png', confidence=0.8)
        if position is None and started:
            position = auto.locateCenterOnScreen('game_quit.png', confidence=0.8)
        if position is not None and started:
            auto.moveTo(position[0],position[1],duration=random.uniform(1, 3),tween=auto.easeInOutQuad)
            time.sleep(random.uniform(0, 1))
            if auto.position()==(position[0],position[1]) and started:
                input.click()
        return
    if auto.locateCenterOnScreen('game_fail.png', confidence=0.8) is not None and started:
        skipPrep=False
        position=None
        if not unexpected:
            unexpected=True
            printf("game failed")
        if started:
            position = auto.locateCenterOnScreen('game_leave.png', confidence=0.8)
        if position is None and started:
            position = auto.locateCenterOnScreen('game_quit.png', confidence=0.8)
        if position is not None and started:
            auto.moveTo(position[0],position[1],duration=random.uniform(1, 3),tween=auto.easeInOutQuad)
            time.sleep(random.uniform(0, 1))
            if auto.position()==(position[0],position[1]) and started:
                input.click()
        return
    if auto.locateCenterOnScreen('game_prompt.png', confidence=0.8) is not None and started:
        skipPrep=False
        position=None
        if not unexpected:
            unexpected=True
            printf("game prompted")
        if started:
            position = auto.locateCenterOnScreen('game_confirm.png', confidence=0.8)
        if position is not None and started:
            auto.moveTo(position[0],position[1],duration=random.uniform(1, 3),tween=auto.easeInOutQuad)
            time.sleep(random.uniform(0, 1))
            if auto.position()==(position[0],position[1]) and started:
                input.click()
        return
    if started:
        promptHWND=win32gui.FindWindow(0, "致命错误")
        if promptHWND:
            skipPrep=False
            printf("game errored")
            win32gui.ShowWindow(promptHWND, win32con.SW_SHOWDEFAULT)
            win32gui.SetForegroundWindow(promptHWND)
            input.press('enter')
            return

def findGame():
    global started, skipPrep, unexpected
    gameHWND=win32gui.FindWindow(0, "Call of Duty®: Modern Warfare®")
    platHWND=win32gui.FindWindow(0, "Battle.net")
    if not platHWND:
        platHWND=win32gui.FindWindow(0, "战网")
    if not gameHWND and started:
        printf("Game not running, booting...")
        if skipPrep and started:
            resetControl()
            skipPrep=False
        gameSwitched=False
        if not platHWND and started:
            stop("Battle.net not running, exiting...")
            return
        while not win32gui.FindWindow(0, "Call of Duty®: Modern Warfare®") and started:
            notFound=True
            position=None
            if started:
                win32gui.SetWindowPos(platHWND, win32con.NULL, 0, 0, 1600,900, win32con.SWP_FRAMECHANGED)
                time.sleep(0.1)
                position = auto.locateCenterOnScreen('plat_switch.png', confidence=0.8)
            if position is not None and not gameSwitched and started:
                currX, currY=auto.position()
                auto.moveTo(position[0],position[1])
                if auto.position()==(position[0],position[1]) and started:
                    auto.click()
                if started:
                    auto.moveTo(160,790)
                    if auto.position()==(160,790) and started:
                        auto.click()
                        auto.press('esc')
                    if started:
                        input.moveTo(currX, currY)
            promptHWND=win32gui.FindWindow(0, "是否在安全模式下运行？")
            if promptHWND and started:
                win32gui.ShowWindow(promptHWND, win32con.SW_SHOWDEFAULT)
                win32gui.SetForegroundWindow(promptHWND)
                input.press('n',interval=0.1)
                notFound=False
            promptHWND=win32gui.FindWindow(0, "设置为最佳设置？")
            if promptHWND and started:
                win32gui.ShowWindow(promptHWND, win32con.SW_SHOWDEFAULT)
                win32gui.SetForegroundWindow(promptHWND)
                input.press('n',interval=0.1)
                notFound=False
            promptHWND=win32gui.FindWindow(0, "致命错误")
            if promptHWND and started:
                win32gui.ShowWindow(promptHWND, win32con.SW_SHOWDEFAULT)
                win32gui.SetForegroundWindow(promptHWND)
                input.press('enter',interval=0.1)
                notFound=False
            if notFound and started:
                platHWND=win32gui.FindWindow(0, "Battle.net")
                if not platHWND:
                    platHWND=win32gui.FindWindow(0, "战网")
                if platHWND:
                    if win32gui.IsIconic(platHWND):
                        win32gui.ShowWindow(platHWND, win32con.SW_SHOWDEFAULT)
                    win32gui.BringWindowToTop(platHWND)
                    win32gui.SetActiveWindow(platHWND)
                    win32gui.SetForegroundWindow(platHWND)
                else:
                    stop("Battle.net not running, exiting...")
            time.sleep(0.1)
        if started and unexpected:
            resetCursor()
            unexpected=False
    else:
        if started:
            findUnexpected()
    if started and platHWND:
        if not win32gui.IsIconic(platHWND):
            win32gui.ShowWindow(platHWND, win32con.SW_SHOWMINIMIZED)

def resetControl():
    input.keyUp('w')
    input.keyUp('s')
    input.keyUp('a')
    input.keyUp('d')
    input.keyUp('shift')
    input.mouseUp()

def resetCursor(x=None, y=None, time=random.uniform(0.5,1)):
    if x is None and y is None:
        x,y=win32api.GetSystemMetrics(0)//2,win32api.GetSystemMetrics(1)//2
    if auto.position() != (x,y):
        auto.moveTo(x,y, duration=time, tween=auto.easeInOutQuad)

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
    if key == keyboard.Key.f5:
        if not started:
            started=True
            printf("starting...")
    elif key == keyboard.Key.f6:
        if started:
            started=False
            skipPrep=False
            resetControl()
            printf("stopping...")

def on_release(key):
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
    global started
    x,y=auto.position()
    xOffSet = random.randint(-2,2)
    yOffSet = random.randint(-1,1)
    for _ in range(int(duration*1000)):
        if not started:
            break
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, xOffSet, yOffSet, 0, 0)
    resetCursor(x=x, y=y)

def randKey():
    global started
    for _ in range (4):
        if not started:
            break
        seed = random.randint(0,3)
        if seed == 0:
            input.keyUp('s')
            input.keyDown('w')
            time.sleep(random.uniform(0.1,0.2))
            if started:
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
        if started:
            time.sleep(random.uniform(0.1,0.3))

def gamePrep():
    global skipPrep, maxnum, started
    i = 1
    while started:
        findGame()
        if skipPrep:
            break
        position = auto.locateCenterOnScreen(str(i)+'.png', confidence=0.8)
        if position is not None:
            if started:
                auto.moveTo(position[0],position[1])
                time.sleep(random.uniform(0, 1))
            if started:
                if auto.position()==(position[0],position[1]):
                    input.click(clicks=3, duration=1)
                if i == maxnum:
                    skipPrep=True
                    printf("game started")
                    break
        else:
            if i >= maxnum:
                i = 0
                if started:
                    resetCursor()
                    resizeGame()
        if started:
            i += 1
            time.sleep(0.1)

def mainLoop():
    global started, skipPrep
    while True:
        try:
            gamePrep()
            if not started:
                if skipPrep:
                    resetControl()
                break
            if started:
                randKey()
                time.sleep(random.uniform(0, 3))
            if started:
                input.press('space')
                time.sleep(random.uniform(0, 3))
            if started:
                input.press('c')
                time.sleep(random.uniform(1, 2))
            if started:
                input.press('space')
            if started:
                moveMouse(round(random.uniform(0, 4),3))
                input.rightClick()
                time.sleep(random.uniform(0, 1))
            if started:
                input.mouseDown()
                time.sleep(random.uniform(0, 4))
            if started:
                input.mouseUp()
                time.sleep(random.uniform(0, 1))
            if started:
                input.rightClick()
                time.sleep(random.uniform(0, 1))
            if started:
                input.press('1')
                time.sleep(random.uniform(0, 3))
        except (auto.FailSafeException, input.FailSafeException):
            if started:
                printf("Failsafe detected, resetting...")
                resetCursor()
            continue
        except Exception as e:
            stopError(e)

if __name__ == '__main__':
    print("[BattlePasser Version 1.35]")
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
    if not path.exists("game_ended.png") and noError:
        stop("Game ending picture identifier 'game_ended.png' missing, exiting...")
        noError=False
    if not path.exists("game_ends.png") and noError:
        stop("Game ending picture identifier 'game_ends.png' missing, exiting...")
        noError=False
    if not path.exists("game_abort.png") and noError:
        stop("Game aborting picture identifier 'game_abort.png' missing, exiting...")
        noError=False
    if not path.exists("game_update.png") and noError:
        stop("Game updating picture identifier 'game_update.png' missing, exiting...")
        noError=False
    if not path.exists("game_updated.png") and noError:
        stop("Game updating picture identifier 'game_updated.png' missing, exiting...")
        noError=False
    if not path.exists("game_disconnect.png") and noError:
        stop("Game disconnecting picture identifier 'game_disconnect.png' missing, exiting...")
        noError=False
    if not path.exists("game_fail.png") and noError:
        stop("Game failing picture identifier 'game_fail.png' missing, exiting...")
        noError=False
    if not path.exists("game_prompt.png") and noError:
        stop("Game prompting picture identifier 'game_prompt.png' missing, exiting...")
        noError=False
    if not path.exists("game_leave.png") and noError:
        stop("Game leaving picture identifier 'game_leave.png' missing, exiting...")
        noError=False
    if not path.exists("game_quit.png") and noError:
        stop("Game quitting picture identifier 'game_quit.png' missing, exiting...")
        noError=False
    if not path.exists("game_confirm.png") and noError:
        stop("Game confirming picture identifier 'game_confirm.png' missing, exiting...")
        noError=False
    if not path.exists("plat_switch.png") and noError:
        stop("Battle.net game switching picture identifier 'plat_switch.png' missing, exiting...")
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