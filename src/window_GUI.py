import PySimpleGUI as sg
import cv2
import datetime

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


def check_events(event, window, recording, detect_face, game_frame, show_face_detection, record_button):
    # Exit event
    if event in ('Exit', None):
        #cv2.destroyWindow('just eyes')
        #cv2.destroyWindow('-image-')lk
        pass
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

    elif event == "l":
        detect_face = not detect_face
        if not detect_face:
            cv2.destroyWindow('just eyes')

    elif event == "v":
        print(game_frame)
        game_frame = not game_frame
        print(game_frame)
        if game_frame == False:
            cv2.destroyWindow('frame_game')

    elif event == "k":
        show_face_detection = not show_face_detection
        if show_face_detection == True:
            image_elem, record_button, window = create_GUI()
        else:
            window.close()


    return window, recording, detect_face, game_frame, show_face_detection


def record(image_eyes, path, number_file):
    gray = cv2.cvtColor(image_eyes, cv2.COLOR_BGR2GRAY)
    date = datetime.datetime.now().strftime("%Y_%m_%d_%I_%M_%S_%p")
    ruta_total = path + "/" + date + "_" + str(number_file) + ".png"
    cv2.imwrite(ruta_total, gray)
    number_file = number_file + 1
    return number_file