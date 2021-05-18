import cv2
from parameters import *
from functions import *

car_cascade = cv2.CascadeClassifier(classifier_name) #Initialisation of the cascade classifier
cap = cv2.VideoCapture(video_src) #Start capture of the video source
print(type(car_cascade))
#Check if video source capture started
if cap.isOpened() == False:
    print("ERROR : Can't open Video file")
else:
    print("Video file opened")

index = 0
while cap.isOpened(): #While video capture is available
    ret, frame = cap.read() #Read the video source
    
    #Break the infinit loop if no more pictures in the video source
    if ret == False:
        print("Video file closed")
        break
    
    frame, cars = find_cars(frame, car_cascade)
    index = save_cars(frame, path, index, cars)
    #Show the actual frame with rectangles in a cv2 window
    cv2.imshow('Cars', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'): #Time between 2 frames : 10ms / If 'q' is pressed, break the loop
        break

#Release the capture and destroy all created windows at the end of the program
cap.release()
cv2.destroyAllWindows()
print("All tasks are done ") #Confirm the end of the program