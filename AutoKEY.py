from apscheduler.schedulers.blocking import BlockingScheduler
# 导入pynput库的keyboard模块
from pynput.keyboard import Key, Listener, Controller

scheduler = BlockingScheduler()

keyboard = Controller()
g_flag = False


def press_key(key):
    global g_flag
    if g_flag:
        keyboard.type(key)


def on_press(key):
    if key.char == 'f':
        global g_flag
        g_flag = not g_flag


if __name__ == "__main__":
    keyMap = {
        "q": 1,
        "w": 1.2,
        "e": 1.3,
        "r": 1.4,
    }
    Listener(on_press=on_press).start()
    for key, value in keyMap.items():
        scheduler.add_job(press_key, 'interval', args=key, seconds=value)
    scheduler.start()
