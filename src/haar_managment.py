import cv2

###########################################################
# We used this haar cascade object detection method for the
# first versions  but we are not using it anymore
############################################################
haar = cv2.CascadeClassifier('./model/haarcascade_frontalface_default.xml')
haar2 = cv2.CascadeClassifier('./model/haarcascade_fullbody.xml')

def pipeline_model(img , color='bgr'):

    if color == 'bgr':
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    else:
        gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

    faces = haar.detectMultiScale(gray,1.5,3)
    for x,y,w,h in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2) # drawing rectangle
        roi = gray[y:y+h,x:x+w] # crop image
        roi = roi / 255.0

        if roi.shape[1] > 100:
            roi_resize = cv2.resize(roi,(100,100),cv2.INTER_AREA)
        else:
            roi_resize = cv2.resize(roi,(100,100),cv2.INTER_CUBIC)
        roi_reshape = roi_resize.reshape(1,10000) # 1,-1


