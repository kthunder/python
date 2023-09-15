# -*- coding:utf-8 -*-
import pyautogui
import time
from pynput.keyboard import Key, Listener, Controller
import keyboard

def on_press(key):
    match (hasattr(key, "vk") and key.vk, hasattr(key, "char") and key.char):
        # p
        case (80, 'p'):
            global g_flag
            g_flag = not g_flag
            print("state : ", g_flag)
        case _:
            print(key.__dict__)
            pass

def fill_cell(x, y, info):
    time.sleep(0.2)
    pyautogui.click(3260,200)
    time.sleep(0.2)
    pyautogui.click(3260,200)
    time.sleep(0.2)
    pyautogui.click(x, y)
    time.sleep(0.2)
    if(len(info) > 4):
        keyboard.press_and_release("ctrl+v");
    else:
        keyboard.write(info)
    time.sleep(0.4)


def change_item():
    time.sleep(1.5)
    pyautogui.scroll(-500)
    time.sleep(0.5)
    x = pyautogui.locateOnScreen('a8.png', region=(800, 300, 200, 1700))
    if (x):
        pyautogui.click(x.left, x.top, duration=0.3)
        time.sleep(0.2)
        pyautogui.click(1120, 262, duration=0.3)
        time.sleep(0.2)
        pyautogui.click(1625, 1242, duration=0.3)
        print(x)


if __name__ == "__main__":

    g_flag = True

    # 监听按键，用来暂停 操作
    Listener(on_press=on_press).start()

    for _ in range(0,75):
        if _ < 5:
            time.sleep(1)
            print(pyautogui.position())
        if g_flag:
            fill_cell(1596, 1247, "参见实测日志Smu_test/Smu_Normal_Test.txt")
            pass

