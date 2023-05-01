from apscheduler.schedulers.blocking import BlockingScheduler
# 导入pynput库的keyboard模块
from pynput.keyboard import Key, Listener, Controller
from conf import keyMap

scheduler = BlockingScheduler()

keyboard = Controller()
g_flag = False


def press_key(key):
    global g_flag
    if g_flag:
        keyboard.type(key)


def on_press(key):
    print(key.__dict__)
    match (hasattr(key, "vk") and key.vk, hasattr(key, "char") and key.char):
        # Ctrl+1
        case (49, None):
            global g_flag
            g_flag = not g_flag
            print("flag{}", g_flag)
        case _:
            pass


if __name__ == "__main__":
    Listener(on_press=on_press).start()
    for key, value in keyMap.items():
        scheduler.add_job(press_key, 'interval', args=key, seconds=value)
    scheduler.start()
