import PySimpleGUI as sg
from datetime import date
import cv2
import time
from cvzone.FaceMeshModule import FaceMeshDetector




def check_eyes(img, faces, eyes_on):
    #left eye landmarks
    leye = [130,30,29,28,27,56,190,243,112,26,22,23,24,110,25,33,246,161,160,159,158,157,173,133,155,154,153,145,144,163, 7, 33]
    #right eye landmarks
    reye = [362, 398, 384,385,386,387,388,466,263,249,390,373,374,380,381,382,463,414,286,258,259,257,260,467,359,255,339,254,253,252,256,341]

    if eyes_on:
        # Drawing eyes on blue colour
        try:
            for landmark in leye:
                cv2.circle(img, ((faces[0][landmark])[0], (faces[0][landmark])[1]), 2, (255, 50, 0), cv2.FILLED)
            for landmark in reye:
                cv2.circle(img, ((faces[0][landmark])[0], (faces[0][landmark])[1]), 2, (255, 50, 0), cv2.FILLED)
        except Exception as err:
            print(err)

def main():
    #Connecting to the Webcam
    camara = cv2.VideoCapture(0)



    #PySimpleGUI theme
    sg.theme('lightBlue')
    #Defining elements of the Graphic interface
    button2 = sg.Button('Take Video pictures')
    read_button = sg.ReadFormButton('Click to record Video', bind_return_key=True)
    layout = [
              [sg.Image(filename='', key='-image-')],
              [sg.Button('Set Folder'),read_button, sg.Button('exit')],
              ]
    #Creating Graphic interface
    window = sg.Window('Camera',
                       layout,
                       return_keyboard_events=True,
                       no_titlebar=False,
                       location=(0, 900))


    image_elem = window['-image-']
    number = 0
    detector = FaceMeshDetector(maxFaces=1)
    detect_face = False
    pTime = 0
    eyes_on = False
    recording = False
    ruta = ""
    while camara.isOpened():
        #Obtenemos informacion de la interfaz grafica y video
        event, values = window.read(timeout=0)
        ret, frame = camara.read()
        frame = cv2.flip(frame, 1)
        image_new = frame.copy()

        if detect_face:
            frame, faces = detector.findFaceMesh(frame)
            check_eyes(frame, faces, eyes_on)

            # we get the min and max position of the eyes (left and right) on any frame so that we can have a
            # windows of the eyes, even if we move
            # 130 left eye landmark
            x_min, y_min = faces[0][130]
               #cv2.circle(frame, (x_min, y_min), 2, (255, 50, 0), cv2.FILLED)
            # 359 right eye landmark
            x_max, y_max = faces[0][359]
                #cv2.circle(frame, (x_max, y_max), 2, (255, 50, 0), cv2.FILLED)

            # We create a new image where we have just the eyes so that we can pass it to the CNN model
            image_new = image_new[y_min - 20:y_max + 20, x_min - 10:x_max + 10]
            #cv2.imshow('eyes', frame)
            output = cv2.resize(image_new, [120,40])
            cv2.imshow('just eyes', output)



        #Exit event
        if event in ('Exit', None):
            break

        #Taking pictures of video frames for saving them
        elif event == 'Set Folder':
            ruta = sg.popup_get_folder(title='Save pic', message="Destiny folder")
            print(ruta)
            #gray = cv2.cvtColor(image_new, cv2.COLOR_BGR2GRAY)
            #cv2.imwrite(ruta + "/" + str(date.today()) + str(number) + ".png", gray)
        elif event == "Click to record Video":
            if recording:
                recording = False
                read_button.Update("Click to record Video", button_color=('white', 'blue'))
            else:
                recording = True
                print("recording")
                read_button.Update("Recording Video", button_color=('white', 'red'))

        elif event == "f":
            detect_face = not detect_face
            if not detect_face:
                cv2.destroyWindow('just eyes')


        if not ret:
            break




        number = number + 1

        #  Frame Rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(frame, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (180, 30, 30), 2)
        cv2.putText(frame, ruta, (15, 470), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
        #print(fps)

        # Sending video to GUI
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
        image_elem.update(data=imgbytes)

        if recording:
            gray = cv2.cvtColor(image_new, cv2.COLOR_BGR2GRAY)
            ruta_total = ruta + "/" + str(date.today()) + str(number) + ".png"
            print(ruta_total)
            cv2.imwrite(ruta_total, gray)
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
