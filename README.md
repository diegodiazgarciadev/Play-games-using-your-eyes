# EYE Gaming

# Introduction

Creation of a python program using CNN (convolutional Neural Network) and a simple WebCam, that translate eyes gestures to a code that the computer can
understand, allowing people to play video games using just your eyes.

AMAZING, don't you think?

### Hackshow
This proyect has been selected as a finalist to be showed on the HackShow event of Ironhack

# Video examples

I'm leaving some short videos playing GTA V using my eyes.


https://user-images.githubusercontent.com/82879300/136693265-19cc433c-f412-4134-aaa8-e6965cd7a9cb.mp4

Using eyes up, to start and stop moving. Eyes left and right to move left and right, and eyes closed to get into the car.

https://user-images.githubusercontent.com/82879300/136693329-c7fd19a0-9cfb-42ad-adfb-7c6e77f240f0.mp4

Using wink left to hit and then eyes close to get into the car

https://user-images.githubusercontent.com/82879300/136693661-2440c955-4e21-4f65-93a8-3fb97456d6fb.mp4

Winking right to start CAR_MODE, then turning a bit the head or movien eyes (left,right) to control the car


# Why I did this?

### Academic motivation 
I wanted to use my AI knowlege and use everything I learned in the last few months.

### Challenge
Start with an idea in your head , having 10 days to complete it, and do all the process until you achieve kind of a product anybody could use, has been a very good challenge for me, but I have to say I had fun on the way :)

### Help
I didn't create this program for lazy people who could play games while they are eating or laying down, I created this program for disabled people who are not able to use their hands to play games. I wanted to give them the feeling of freedom of driving a fast car or to go for a walk in a new city.

# How does it work?

Basically what I build, is a translator that has an eye image as an input and a action on the output. We could say it is something like that:  


![image](https://user-images.githubusercontent.com/82879300/136744872-3f10c188-0586-46af-a25a-d154f288d252.png)


### There are two different parts to the project:
  * The creation of a Neuronal Network , in this case a CNN.
  * Using the prediction of the CNN to manage the game.

Our CNN is something like this:  
Where we have an image (120,40) as an input and 11 posibles output, 1 for every eye gesture I have created.  

![image](https://user-images.githubusercontent.com/82879300/136745190-3f59c5d7-e132-440c-944b-185b9080cf09.png)


#### We need to feed (train) this CNN, but how?. With thousands of eyes pictures.

For that I have created a program that take pictures just of the eyes, even if you are moving.   

If you are on the screen (webcam) and you start recording, the program will find your eyes, will take pics of them and
save them until you stop it. Obviously there is a button to set in what folder you want to save them.

![image](https://user-images.githubusercontent.com/82879300/136746149-2a769973-60ff-4a83-907d-4feb3d6a2b32.png)


After the first training I didn't have very good results (fitting with around 1000 pics):  
![image](https://user-images.githubusercontent.com/82879300/136747010-7cde8a70-deda-4d2f-9f13-6bcb809032d4.png)

But when I started adding more and more pics, everything started to work really well:

![image](https://user-images.githubusercontent.com/82879300/136747077-3288b318-bc87-4084-a790-00efac84c527.png)


### Now is the moment of doing a Real Time Prediction: 

* Our program will open the webcam
* For every single frame will do :
    + Face detection
    + Find the eyes (ROI)
    + Give the eye ROI to the CNN
    + Get the prediction
    + Order an action depending on the prediction (only if we are over a accuracy threshold)

We can see what actions we are able to do on the next section,



# Controlls for GTA V

![image](https://user-images.githubusercontent.com/82879300/136694237-b9be4f52-b9d3-4690-a717-a89b6e6330ef.png)

![image](https://user-images.githubusercontent.com/82879300/136694262-1f1cf82c-a879-46db-85e2-036764afbb64.png)



# Problems on the way

* Creation of a Eye language 

* Tuning the key/mouse parameters (sleep, number of pixels, released …) to make the game smooth

* Speed of winks/blinks (Creation of a predictions buffer)

* Light (thousands of pics)

* Computer performance

# Next Steps

* More research on image normalization for NN (for lighting issues)

* Create a better  eye language.

* Detect object in the game, and do actions . Like, if I find enemy, shoot him/her automatically. 

* Interface to customize the links eye movements → Keys 

* Customize sensibilities of eyes movement.

