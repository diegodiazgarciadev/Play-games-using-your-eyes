import cv2
import time
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PoseModule import PoseDetector
from tensorflow.keras.models import load_model
import numpy as np
from PIL import ImageGrab
import src.utils as ut
import configuration.config as cnf
import src.window_GUI as win
import src.mouse as mouse
import src.haar_managment as haar
import resources.keys as k



n = [12, 10, 8]
i = 0
buffer_predictions = []
new_model = load_model('model/50epochs_7classes.h5')
moving = False
car_mode_on = True




keys = k.Keys()

def direct_key(key, sleep):
    # keyboard (direct keys)
    keys.directKey(key)
    #time.sleep(sleep)


def direct_key_released(key):
    keys.directKey(key, keys.key_release)

def direct_key_move(key, sleep):
    # keyboard (direct keys)
    global moving
    moving = not moving
    if moving == True:
        keys.directKey(key)
        time.sleep(0.4)
    else:
        keys.directKey(key, keys.key_release)
        time.sleep(0.4)

def virtual_key():
    # keyboard (virtual keys)
    keys.directKey("w", type=keys.virtual_keys)
    time.sleep(0.04)
    keys.directKey("w", keys.key_release, keys.virtual_keys)

def countdown(num_of_secs):
    for i in range.reverse(num_of_secs):
        print(i)
        time.sleep(i)



def do_action(movement, sensibility):
    global i
    global car_mode_on
    if movement != "eyes_centered":
        if movement == "eyes_left":
            if car_mode_on:
                direct_key("a", 1)
            else:
                mouse.left_mouse(15)


        elif movement == "eyes_right":
            if car_mode_on:
                direct_key("d", 1)
            else:
                 mouse.right_mouse(15)

        elif movement == "eyes_up":
             direct_key_move("w", 0.5)
        elif movement == "eyes_closed":
           # mouse.down_mousefff
            direct_key_move("s", 0.1)
        elif movement == "blink_left":
            # mouse.click_left_mouse()
            direct_key("x", 0.2)

        elif movement == "blink_right":
            #change sensibility
            car_mode_on =  not  car_mode_on
            time.sleep(0.3)
            print("Car mode: ", car_mode_on)
            """
            print ("len(n)-1 :", len(n)-1)
            if i == len(n)-1:
                i=0
            else:
                i = i + 1
            time.sleep(0.3)
            print("new Sensitivity to  :", n[i], i)
            """
        print("movement", movement)
    else:
        direct_key_released("a")
        direct_key_released("d")
        direct_key_released("s")


def predict_(frame):
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

        movement = cnf.classes[mode]
        #print("movement", movement)
        global i
        do_action(movement, n[i])


        return movement

def detect_pose(frame, detector_pose):
    frame = detector_pose.findPose(frame)
    lmList, bboxInfo = detector_pose.findPosition(frame, bboxWithHands=False)
    if bboxInfo:
        center = bboxInfo["center"]
        cv2.circle(frame, center, 5, (255, 0, 255), cv2.FILLED)
        # mouse(center[0], center[1])
    return frame



def main():
    # Connecting to the Webcam
    #url = 'http://192.168.31.168:8080/shot.jpg'
    #camara = cv2.VideoCapture(url)
    camera = cv2.VideoCapture(0)
    image_elem, record_button, window = win.create_GUI()

    # inicializating of flags
    number_file = 0
    frame_it = 0
    detector_face = FaceMeshDetector(maxFaces=1)
    detector_pose = PoseDetector()
    detect_face = False
    pTime = 0
    draw_eyes = False
    recording = False
    path = "C:/Users/yabo9/AI/Computer Vision/CNN"
    game_frame = False
    show_face_detection = True

    while camera.isOpened():
        # Getting info from GUI and video
        event, values = window.read(timeout=0)
        #camera = cv2.VideoCapture(url)
        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)
        try:
            if detect_face:
                frame_copy = frame.copy()
                frame, faces = detector_face.findFaceMesh(frame)
                image_eyes = ut.eyes_detection(frame_copy, faces)
                ut.check_eyes(frame, faces, draw_eyes)
                output = cv2.resize(image_eyes, [120, 40])
                gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
                predict_(gray)
                #cv2.putText(frame, "Sensibitily: " + str(int(sensibility)), (220, 50), cv2.FONT_HERSHEY_PLAIN, 2, (180, 30, 30), 2)
                frame_it = frame_it + 1
                # cv2.imshow('just eyes light', image_eyes_light)
                cv2.imshow('just eyes', gray)
                # cv2.imshow('just eyes', output)


            if game_frame:
                # Grabbing screehot
                img_game = ImageGrab.grab(bbox=(0, 300, 800, 800))  # x, y, w, h
                # img_game = img_game.resize(300, 400)
                img_game_np = np.array(img_game)
                frame_game = cv2.cvtColor(img_game_np, cv2.COLOR_BGR2GRAY)
                # haar.pipeline_model(img_game_np)

                # frame = img_game_np
                frame_game = detect_pose(img_game_np, detector_pose)
                cv2.imshow("frame_game", frame_game)

        except Exception as err:
            print(err)


        #   Checking events on the window
        window, recording, detect_face, game_frame, show_face_detection = win.check_events(event, window, recording, detect_face, game_frame, show_face_detection, record_button)
        #   Frame Rate
        pTime = ut.frame_rate(frame, path, pTime)


        # Sending video to GUI
        if show_face_detection:
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
            image_elem.update(data=imgbytes)

        if recording:
            number_file = win.record(image_eyes, path, number_file)


        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

        if k == ord("k"):
            show_face_detection = not show_face_detection
            if show_face_detection == True:
                image_elem, record_button, window = win.create_GUI()
            else:
                window.close()


        if k == ord("v"):
            game_frame = not game_frame
            if not detect_face:
                cv2.destroyWindow('frame_game')

        if k == ord("l"):
            detect_face = not detect_face
            if not detect_face:
                cv2.destroyWindow('just eyes')
            print("detect_face ", detect_face)
        if k == ord("e"):
            draw_eyes = not draw_eyes


main()
