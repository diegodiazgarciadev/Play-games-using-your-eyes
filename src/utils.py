import time
import cv2

def window_display_info(frame, path, pTime, car_mode_on, detect_face):
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (180, 30, 30), 2)
    cv2.putText(frame, path, (15, 470), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
    if detect_face:
        cv2.putText(frame, "Car Mode: " + str(car_mode_on), (500, 40), cv2.FONT_HERSHEY_PLAIN, 1, (180, 30, 30), 1)

    #print(fps)
    return pTime

def draw_eyes(img, faces):
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

def eyes_detection(frame_copy, faces):
    try:
        # we get the min and max position of the eyes (left and right) on any frame so that we can have a
        # windows of the eyes, even if we move
        # 130 left eye landmark
        x_min, y_min = faces[0][130]
        # 359 right eye landmark
        x_max, y_max = faces[0][359]

        # We create a new image where we have just the eyes so that we can pass it to the CNN model
        image_eyes = frame_copy[y_min - 20:y_max + 20, x_min - 10:x_max + 10]
        return image_eyes
    except IndexError as err:
        print(err)

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img