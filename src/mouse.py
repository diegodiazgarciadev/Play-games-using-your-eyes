import time
import resources.keys as k

keys = k.Keys()

def mouse(x,y):
    for i in range(20):
        keys.directMouse(x, y)
        time.sleep(0.004)
def left_mouse(n):
    print("left_mouse")
    for i in range(n):
        keys.directMouse(-1*i, 0)
        time.sleep(0.004)

def right_mouse(n):
    for i in range(n):
        keys.directMouse(1*i, 0)
        time.sleep(0.004)

def up_mouse(n):
    for i in range(n):
        keys.directMouse(0, -1*i)
        time.sleep(0.004)

def down_mouse(n):
    for i in range(n):
        keys.directMouse(0, 1*i)
        time.sleep(0.004)

def click_left_mouse():
    keys.directMouse(buttons=keys.mouse_lb_press)
    time.sleep(0.01)
    keys.directMouse(buttons=keys.mouse_lb_release)
    time.sleep(0.01)
