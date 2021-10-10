import time
import resources.keys as k

keys = k.Keys()             # Instance of the Keys class


def direct_key(key):
    keys.directKey(key)

def direct_key_released(key):
    keys.directKey(key, keys.key_release)

def direct_key_sleep(key, sleep):
    keys.directKey(key)
    time.sleep(sleep)
    keys.directKey(key, keys.key_release)

def direct_key_move(key, sleep, moving):
    moving = not moving
    if moving == True:
        keys.directKey(key)
        time.sleep(sleep)
    else:
        keys.directKey(key, keys.key_release)
        time.sleep(sleep)
    return moving

def mouse(x,y):
    for i in range(20):
        keys.directMouse(x, y)
        time.sleep(0.004)
def left_mouse(n):
    print("left_mouse")
   # for i in range(n):
   #     keys.directMouse(-1*i, 0)
   #     time.sleep(0.001)
    keys.directMouse(-1 * n, 0)

def right_mouse(n):
   # for i in range(n):
   #     keys.directMouse(2*i, 0)
   #     time.sleep(0.004)
    keys.directMouse(1 * n, 0)


def up_mouse(n):
    for i in range(n):
        keys.directMouse(0, -1*i)
        time.sleep(0.001)

def down_mouse(n):
    for i in range(n):
        keys.directMouse(0, 1*i)
        time.sleep(0.001)

def click_left_mouse():
    keys.directMouse(buttons=keys.mouse_lb_press)
    time.sleep(0.01)
    keys.directMouse(buttons=keys.mouse_lb_release)
    time.sleep(0.1)
