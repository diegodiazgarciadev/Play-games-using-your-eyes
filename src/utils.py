import time
import cv2
import src.keyboard as keyboard
import mouse as ms
import configuration.config as cfg
import statistics
import numpy as np


buffer_predictions = []  # Buffer where we store the last n (buffer_size)  predictions
def predict(frame):
    """
    Giving an eyes frame, this function will send it to the CNN and will get the prediction
    :param frame: A frame with the eyes geture
    :return: The class prediction if it is over the threshold
    """
    global buffer_predictions
    frame = cv2.resize(frame, (120, 40))
    frame = frame / 255
    frame = np.expand_dims(frame, axis=0)
    frame = np.expand_dims(frame, axis=-1)
    frame.shape
    prediction = cfg.new_model.predict(frame)

    if prediction.max() > cfg.threshold:
        key = np.argmax(prediction)
        if (len(buffer_predictions)) < cfg.buffer_size:
            buffer_predictions.append(key)
        else:
            buffer_predictions.append(key)
            buffer_predictions.pop(0)
            print(buffer_predictions)

        if key == 0 or key == 3:
            mode = statistics.mode(buffer_predictions)
            movement = cfg.classes[mode]
        else:
            movement = cfg.classes[key]

        return movement
    else:
        return f"Predcition under the permited {cfg.threshold} threshold accuracy"

def do_action(movement,car_mode_on, moving ):
    """
    Transalting the predicted class to the action of clicking on keyboard or moving the mouse
    :param movement: predicted class
    :param car_mode_on: car_mode_on flag
    :param moving: moving flag
    :return: car_mode_on, moving flags
    """
    if movement != "eyes_centered":
        ########################
        # Eyes movements
        ########################
        if movement == "eyes_left":
            keyboard.direct_key("a")
        elif movement == "eyes_right":
            keyboard.direct_key("d")
        elif movement == "eyes_up":
            moving = keyboard.direct_key_move("w", 0.4, moving)
        elif movement == "eyes_closed":
            keyboard.direct_key_sleep("f", 0.2)
        elif movement == "blink_left":
            keyboard.click_left_mouse()
        elif movement == "blink_right":
            keyboard.direct_key_sleep("NUMPADENTER", 0.08)
            car_mode_on = not car_mode_on
            keyboard.direct_key_sleep("h", 0.08)
            print("car_mode : ", car_mode_on)
            time.sleep(0.2)
        ########################
        # Head movements
        ########################
        elif movement == "head_left":
            if car_mode_on:
                keyboard.direct_key_sleep("a", 0.2)
            else:
                ms.move(-cfg.x_, 0, absolute=False, duration=cfg.time_)
        elif movement == "head_right":
            if car_mode_on:
                keyboard.direct_key_sleep("d", 0.2)
            else:
                ms.move(cfg.x_, 0, absolute=False, duration=cfg.time_)
        elif movement == "head_up":
            if car_mode_on:
                keyboard.direct_key_sleep("x", 0.2)
            else:
                ms.move(0, -cfg.x_, absolute=False, duration=cfg.time_)
        elif movement == "head_down":
            if car_mode_on:
                keyboard.direct_key_released("w")
                keyboard.direct_key("s")
            else:
                ms.move(0, cfg.x_, absolute=False, duration=cfg.time_)
        print("movement", movement)
    else:
        keyboard.direct_key_released("a")
        keyboard.direct_key_released("d")
        keyboard.direct_key_released("s")
        keyboard.direct_key_released("f")
        ms.unhook_all()

    return car_mode_on, moving

def detect_pose(frame, detector_pose):
    """

    :param frame: frame where the detector pose will be executed
    :param detector_pose: intance of the detector_pose object
    :return: frame with the pose detected
    """
    frame = detector_pose.findPose(frame)
    lmList, bboxInfo = detector_pose.findPosition(frame, bboxWithHands=False)
    if bboxInfo:
        center = bboxInfo["center"]
        cv2.circle(frame, center, 5, (255, 0, 255), cv2.FILLED)
    return frame

def window_display_info(frame, path, pTime, car_mode_on, detect_face):
    """
    Usefull info to be displayed on the window
    :param frame: frame where the info will be displayed
    :param path: path base where the pics will be saved
    :param pTime: time parameter to calculate the frame rate
    :param car_mode_on: car_mode_on flag
    :param detect_face: detect_face flag
    :return: pTime parameter that will be updated on every frame on  main.py
    """
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (180, 30, 30), 2)
    cv2.putText(frame, path, (15, 470), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
    if detect_face:
        cv2.putText(frame, "Car Mode: " + str(car_mode_on), (500, 40), cv2.FONT_HERSHEY_PLAIN, 1, (180, 30, 30), 1)

    return pTime

def draw_eyes(img, faces):
    """
    set colour on the eyes from a frame where the face mesh detection is done
    :param img: frame where the eyes will be coloured
    :param faces: array of faces with the points of the mesh
    """
    # left eye landmarks
    leye = [130, 30, 29, 28, 27, 56, 190, 243, 112, 26, 22, 23, 24, 110, 25, 33, 246, 161, 160, 159, 158, 157, 173, 133,
            155, 154, 153, 145, 144, 163, 7, 33]
    # right eye landmarks
    reye = [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382, 463, 414, 286, 258, 259,
            257, 260, 467, 359, 255, 339, 254, 253, 252, 256, 341]

    try:
        for landmark in leye:
            cv2.circle(img, ((faces[0][landmark])[0], (faces[0][landmark])[1]), 2, (255, 50, 0), cv2.FILLED)
        for landmark in reye:
            cv2.circle(img, ((faces[0][landmark])[0], (faces[0][landmark])[1]), 2, (255, 50, 0), cv2.FILLED)
    except Exception as err:
        print(err)

def eyes_detection(frame, faces):
    """
    Getting a ROI of the frame where there is a face mesh detection getting just the eyes
    :param img: frame from where the eyes will be taken
    :param faces: array of faces with the points of the mesh
    :return: ROI from the frame with just the yes
    """
    try:
        # we get the min and max position of the eyes (left and right) on any frame so that we can have a
        # windows of the eyes, even if we move
        # 130 left eye landmark
        x_min, y_min = faces[0][130]
        # 359 right eye landmark
        x_max, y_max = faces[0][359]

        # We create a new image where we have just the eyes so that we can pass it to the CNN model
        image_eyes = frame[y_min - 20:y_max + 20, x_min - 10:x_max + 10]
        return image_eyes
    except IndexError as err:
        print(err)

def increase_brightness(img, value=30):
    """
    increase the brightness of a frame
    :param img: frame where the brightness increasing will be done
    :param value: How much the increase will be done
    :return: The image update with the new increase
    """
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img