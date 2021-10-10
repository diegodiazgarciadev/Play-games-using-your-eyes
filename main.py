import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PoseModule import PoseDetector
import numpy as np
from PIL import ImageGrab
import src.utils as ut
import configuration.config as cfg
import src.window_GUI as win


def main():
    # If we want to  Connect to an  IP Webcam the next to lines need to be uncommented
    # url = 'http://192.168.31.168:8080/shot.jpg'
    # camara = cv2.VideoCapture(url)

    ########################
    # Connecting the Webcam
    ########################
    camera = cv2.VideoCapture(0)
    image_elem, record_button, window = win.create_GUI()

    ########################
    # initializing flags
    ########################

    number_file = 0                              # Counter that we will be using when we are taking pictures to add to the file name
    pTime = 0                                    # Used to get frames per second
    detector_face = FaceMeshDetector(maxFaces=1) # Calling to cvzone library for face detection
    detector_pose = PoseDetector()               # Calling to cvzone library for pose detection
    face_detection = False                       # If we are using Face detection
    eyes_detection = True                        # Flag that will start the predictions and actions from the eyes movements
    draw_eyes = False                            # Flag to draw the eyes in blue on face detection
    recording = False                            # Flag to let us know if we are recording pics
    game_frame = False                           # Flag to start object detectionIN the game (not totally implemented yet)
    show_face_detection = True                   # Flag to close the face detection window in order to get more frames per second
    moving = False                               # Flag to check if the player is walking
    car_mode_on = False                          # Flag to check if the car mode is ON

    while camera.isOpened():
        
        # Getting info from GUI and video
        event, values = window.read(timeout=0)
        
        # If we need to use an IP cam, the next line has to be uncommented
        # camera = cv2.VideoCapture(url)
        
        # Reading the camera getting the frame and flipping it
        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)
        
        # We need the program to keep going even if there is no face, eyes or what ever the program expect.
        # Without the try - except we would have index out bounds exception for those cases
        try:
            if face_detection:
                # Copy the original frame for doing modifications over it and cropping the eyes
                frame_copy = frame.copy()
                # calling method findFaceMesh for the face detection of the frame
                frame, faces = detector_face.findFaceMesh(frame)

                # If draw_eyes is True the eyes from the mesh will be coloured in blue (just for fun)
                if draw_eyes:
                    ut.draw_eyes(frame, faces)

                # The moment we activate eyes detecion (if face detection is active), the program
                # will get the eyes (ROI) from the frame (using info from the face detection) and will
                # give that eyes to the Convolutional Neural Network model asking for a prediction
                # and finally do an action about the prediction
                if eyes_detection:

                    # Getting eyes from frame
                    image_eyes = ut.eyes_detection(frame_copy, faces)

                    output = cv2.resize(image_eyes, [120, 40])
                    output = ut.increase_brightness(output, 10)
                    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

                    # Showing the eyes ROI in a new window
                    cv2.imshow('just eyes', gray)
                    cv2.moveWindow('just eyes', 540, 10)

                    # Calling the NN model for getting the movement prediction
                    movement = ut.predict(gray)

                    # Doing the action that correspond that movement
                    car_mode_on, moving = ut.do_action(movement, car_mode_on, moving)



            # Not fully implemented yet
            # Getting a game frame (piece of the screen where we are displaying the game) and doing
            # some object detection over it. In this case a pose detection so that we will
            # be able to do actions in the game depending on what we are detecting.
            if game_frame:
                # Grabbing screehot
                img_game = ImageGrab.grab(bbox=(0, 300, 800, 800))  # x, y, w, h
                img_game_np = np.array(img_game)
                frame_game = ut.detect_pose(img_game_np, detector_pose)
                cv2.imshow("frame_game", frame_game)

        except Exception as err:
            print(err)

        #   We are using PySimpleGUI and cv2 windows, so we need to check event independently.
        #   Checking events on PySimpleGUI window
        window, cfg.path, recording, face_detection, game_frame, show_face_detection = win.check_events(event, window, cfg.path,
                                                                                                 recording, face_detection,
                                                                                                 game_frame,
                                                                                                 show_face_detection,
                                                                                                 record_button)

        # Displaying some useful info on the PySimpleGUI window
        pTime = ut.window_display_info(frame, cfg.path, pTime, car_mode_on, face_detection)

        # Sending video to GUI
        if show_face_detection:
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
            image_elem.update(data=imgbytes)

        # if recording = True the program will start taken pictures.
        if recording:
            number_file = win.record(image_eyes, cfg.path, number_file)

        ################################################
        ################################################
        # Managing cv2 windows keyboard Events
        ################################################
        ################################################

        # Reading the key
        k = cv2.waitKey(1) & 0xFF

        # If we click "esc" we leave the program
        if k == 27:
            break

        # If we click k we close the PySimpleGUI window for better performance
        if k == ord("k"):
            show_face_detection = not show_face_detection
            if show_face_detection == True:
                image_elem, record_button, window = win.create_GUI()
            else:
                window.close()

        # If we click v we start the game frame object detection (Not implemented yet)
        if k == ord("v"):
            game_frame = not game_frame
            if not face_detection:
                cv2.destroyWindow('frame_game')


        # If we click l we start face detection
        if k == ord("l"):
            face_detection = not face_detection
            if not face_detection:
                cv2.destroyWindow('just eyes')
            print("face_detection ", face_detection)

        # If we click e we draw eyes in blue if face detection is activated
        if k == ord("e"):
            draw_eyes = not draw_eyes

        # If we click b we change sensibility of the mouse (just for testing purposes)
        if k == ord("b"):
            if cfg.x == -150:
                cfg.x = -25
                cfg.time_ = 0.2
            else:
                cfg.x = -150
                cfg.time_ = 0.1


main()
