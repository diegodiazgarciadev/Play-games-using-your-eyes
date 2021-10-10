import time
import resources.keys as k

keys = k.Keys()             # Instance of the Keys class


def direct_key(key):
    """
    Pressing a key on the keyboard
    :param key: key that will be pressed
    """
    keys.directKey(key)

def direct_key_released(key):
    """
    Releasing a key on the keyboard
    :param key: key that will be realeased
    """
    keys.directKey(key, keys.key_release)

def direct_key_sleep(key, sleep):
    """
    clicking a key, wait a sleep time and then realease that key
    :param key: key
    :param sleep: time the key will be pressed
    """
    keys.directKey(key)
    time.sleep(sleep)
    keys.directKey(key, keys.key_release)

def direct_key_move(key, sleep, moving):
    """
    if the player is stopped it will start moving and just will stop if
    this function is called again. The same on the other way round.
    :param key: key
    :param sleep: time the key will be pressed
    :param moving: flag to let know if it is moving or not
    :return:
    """
    moving = not moving
    if moving == True:
        keys.directKey(key)
        time.sleep(sleep)
    else:
        keys.directKey(key, keys.key_release)
        time.sleep(sleep)
    return moving


###########################################################
# Mouse movements from the Keys.py class
# We are not using at the moment but we leave it
# in case the movement is smoother for another video game.
##########################################################

def mouse(x,y):
    for i in range(20):
        keys.directMouse(x, y)
        time.sleep(0.004)
def left_mouse(n):
    for i in range(n):
       keys.directMouse(-1*i, 0)
       time.sleep(0.001)

def right_mouse(n):
    for i in range(n):
       keys.directMouse(1*i, 0)
       time.sleep(0.004)

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
