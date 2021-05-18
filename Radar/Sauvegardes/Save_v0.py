import cv2
import os

path = os.getcwd() #Path to the current working directory
classifier_name = path + '/' + 'cars.xml' #Path to the classifier
video_src = path + '/' + 'highway_webcam.mp4' #Path to the video source


car_cascade = cv2.CascadeClassifier(classifier_name) #Initialisation of the cascade classifier
cap = cv2.VideoCapture(video_src) #Start capture of the video source

#Check if video source capture started
if cap.isOpened() == False:
    print("ERROR : Can't open Video file")
else:
    print("Video file opened")

def crop_frame(frame, rect):
    x, y, w, h = rect #Get the x, y position and the width and height of the rectangle

    output_img = frame[y:y+h,x:x+w] #Crop the frame [y0 to y1, x0 to x1]
    return output_img

index = 0

while cap.isOpened(): #While video capture is available
    ret, frame = cap.read() #Read the video source
    
    #Break the infinit loop if no more pictures in the video source
    if ret == False:
        print("Video file closed")
        break

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #Convert to grayscale image
    cars = car_cascade.detectMultiScale(gray,1.8,2) #Find cars in the current frame


    for (x,y,w,h) in cars:
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h), (0,255,0),2) #Draw rectangles around each detected car
        save_car = 'Car' + str(index) + '.jpg'
        print('crop')
        print(crop_frame(frame, (x,y,w,h)))
        #cv2.imwrite( save_car, crop_frame(frame, (x,y,w,h)))
        index += 1
    #Show the actual frame with rectangles in a cv2 window
    cv2.imshow('Cars', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'): #Time between 2 frames : 10ms / If 'q' is pressed, break the loop
        break

#Release the capture and destroy all created windows at the end of the program
cap.release()
cv2.destroyAllWindows()
print("All tasks are done ") #Confirm the end of the program