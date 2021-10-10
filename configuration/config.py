from tensorflow.keras.models import load_model

classes = {  # 11 classes/movements that the neural network will predict given an eyes pic
    0: 'blink_left',
    1: 'blink_right',
    2: 'eyes_centered',
    3: 'eyes_closed',
    4: 'eyes_left',
    5: 'eyes_right',
    6: 'eyes_up',
    7: 'head_down',
    8: 'head_left',
    9: 'head_right',
    10: 'head_up',
}
threshold = 0.80  # Under that threshold accuracy we will disregard the prediction and we won't be doing any movement.

x_ = 25  # Number of pixels we move the mouse on x axis
time_ = 0.1  # Time we expend in moving those pixels

n = [12, 10, 8]  # Array of sensibility (number of pixels we move). We are not using it at the moment


buffer_size = 2  # Buffer size
new_model = load_model('model/80epochs_11classes_10.h5')

path = "C:/Users/yabo9/AI/Computer Vision/CNN" # Global path for saving the pics we are taking of ourselves
