import PySimpleGUI as sg
from datetime import date
import cv2
import time
import datetime
from cvzone.FaceMeshModule import FaceMeshDetector
import numpy as np
from tensorflow.keras.models import load_model
import utils.keys as k
import ctypes
user32 = ctypes.windll.user32
X, Y = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


new_model = load_model('100epochs_7classes2.h5')
classes = {
    0: 'blink_left',
    1: 'blink_right',
    2: 'eyes_centered',
    3: 'eyes_closed',
    4: 'eyes_left',
    5: 'eyes_right',
    6: 'eyes_up',
}
buffer_predictions = []
keys = k.Keys()

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

def predict_(frame, frame_it):
    global buffer_predictions
    frame = cv2.resize(frame, (120, 40))
    frame = frame / 255
    frame = np.expand_dims(frame, axis=0)
    frame = np.expand_dims(frame, axis=-1)
    frame.shape
    prediction = new_model.predict(frame)
    if prediction.max() > 0.90:
        # time.sleep(0.01)
        key = np.argmax(prediction)
        if (len(buffer_predictions)) < 5:
            buffer_predictions.append(key)
        else:
           # print(buffer_predictions, frame_it)
            buffer_predictions.append(key)
            buffer_predictions.pop(0)
           # print(buffer_predictions, frame_it)
        from statistics import mode
        mode = mode(buffer_predictions)

        movement = classes[mode]
        print("movement", movement)
        if movement != "eyes_centered":
            if movement == "eyes_left":
                left_mouse(10)
            elif movement == "eyes_right":
                right_mouse(10)
            elif movement == "eyes_up":
                up_mouse(10)
            elif movement == "eyes_closed":
                down_mouse(10)
            elif movement == "blink_left":
                print("blink_left")

            return movement


def check_eyes(img, faces, eyes_on):
    # left eye landmarks
    leye = [130, 30, 29, 28, 27, 56, 190, 243, 112, 26, 22, 23, 24, 110, 25, 33, 246, 161, 160, 159, 158, 157, 173, 133,
            155, 154, 153, 145, 144, 163, 7, 33]
    # right eye landmarks
    reye = [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382, 463, 414, 286, 258, 259,
            257, 260, 467, 359, 255, 339, 254, 253, 252, 256, 341]

    if eyes_on:
        # Drawing eyes on blue colour
        try:
            for landmark in leye:
                cv2.circle(img, ((faces[0][landmark])[0], (faces[0][landmark])[1]), 2, (255, 50, 0), cv2.FILLED)
            for landmark in reye:
                cv2.circle(img, ((faces[0][landmark])[0], (faces[0][landmark])[1]), 2, (255, 50, 0), cv2.FILLED)
        except Exception as err:
            print(err)


def create_GUI():
    # PySimpleGUI theme
    sg.theme('lightBlue')
    # Defining elements of the Graphic interface
    button2 = sg.Button('Take Video pictures')
    record_button = sg.ReadFormButton('Click to record Video', bind_return_key=True)
    layout = [
        [sg.Image(filename='', key='-image-')],
        [sg.Button('Set Folder'), record_button, sg.Button('exit')],
    ]
    # Creating Graphic interface
    window = sg.Window('Camera',
                       layout,
                       return_keyboard_events=True,
                       no_titlebar=False,
                       location=(0, 0))

    image_elem = window['-image-']

    return image_elem, record_button, window


def check_events(event, recording, detect_face, record_button):
    # Exit event
    if event in ('Exit', None):
        cv2.destroyWindow('just eyes')
        cv2.destroyWindow('-image-')
    # Taking pictures of video frames for saving them
    elif event == 'Set Folder':
        path = sg.popup_get_folder(title='Save pic', message="Destiny folder")
        print(path)
        # gray = cv2.cvtColor(image_new, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite(path + "/" + str(date.today()) + str(number) + ".png", gray)
    elif event == "Click to record Video":
        if recording:
            recording = False
            record_button.Update("Click to record Video", button_color=('white', 'blue'))
        else:
            recording = True
            print("recording")
            record_button.Update("Recording Video", button_color=('white', 'red'))

    elif event == "f":
        detect_face = not detect_face
        if not detect_face:
            cv2.destroyWindow('just eyes')

    return recording, detect_face


def frame_rate(frame, path, pTime):
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (180, 30, 30), 2)
    cv2.putText(frame, path, (15, 470), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
    return pTime


def eyes_detection(frame_copy, faces):
    try:
        # we get the min and max position of the eyes (left and right) on any frame so that we can have a
        # windows of the eyes, even if we move
        # 130 left eye landmark
        x_min, y_min = faces[0][130]
        # 359 right eye landmark
        x_max, y_max = faces[0][359]
    except IndexError as err:
        print(err)

    # We create a new image where we have just the eyes so that we can pass it to the CNN model
    image_eyes = frame_copy[y_min - 20:y_max + 20, x_min - 10:x_max + 10]
    return image_eyes


def main():
    # Connecting to the Webcam
    camara = cv2.VideoCapture(0)
    image_elem, record_button, window = create_GUI()

    # inicializating of flags
    number = 0
    frame_it = 0
    detector = FaceMeshDetector(maxFaces=1)
    detect_face = False
    pTime = 0
    eyes_on = False
    recording = False
    path = "C:/Users/yabo9/AI/Computer Vision/CNN"

    while camara.isOpened():
        # Getting info from GUI and video
        event, values = window.read(timeout=0)
        ret, frame = camara.read()
        frame = cv2.flip(frame, 1)

        if detect_face:
            frame_copy = frame.copy()
            frame, faces = detector.findFaceMesh(frame)
            image_eyes = eyes_detection(frame_copy, faces)
            check_eyes(frame, faces, eyes_on)

            try:
                output = cv2.resize(image_eyes, [120, 40])
                gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
                predict_(gray, frame_it)
                frame_it = frame_it + 1
            except Exception as err:
                print(err)

            cv2.imshow('just eyes', gray)
            # cv2.imshow('just eyes', output)

        #   Checking events on the window
        recording, detect_face = check_events(event, recording, detect_face, record_button)
        #   Frame Rate
        pTime = frame_rate(frame, path, pTime)

        # Sending video to GUI
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
        image_elem.update(data=imgbytes)

        if recording:
            gray = cv2.cvtColor(image_eyes, cv2.COLOR_BGR2GRAY)
            date = datetime.datetime.now().strftime("%Y_%m_%d_%I_%M_%S_%p")
            ruta_total = path + "/" + date + "_" + str(number) + ".png"
            cv2.imwrite(ruta_total, gray)
            number = number + 1

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

        if k == ord("f"):
            detect_face = not detect_face
            if not detect_face:
                cv2.destroyWindow('just eyes')
            print("detect_face ", detect_face)
        if k == ord("e"):
            eyes_on = not eyes_on


main()
