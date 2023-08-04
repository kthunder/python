import pyautogui
import time

if __name__ == "__main__":
    while 1:
        # while 1:
        #     print(pyautogui.position())
        time.sleep(1.5)
        pyautogui.scroll(-500)
        time.sleep(0.5)
        x = pyautogui.locateOnScreen('a8.png', region=(800, 300, 200, 1700))
        if (x):
            pyautogui.click(x.left, x.top, duration=0.3)
            time.sleep(0.2)
            pyautogui.click(1120, 262, duration=0.3)
            time.sleep(0.2)
            pyautogui.click(1120, 400, duration=0.3)
            print(x)
