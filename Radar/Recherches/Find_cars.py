import cv2

car_cascade = cv2.CascadeClassifier('C:/Users/broca/Programmation/Projets/En cours/Radar/Recherches/cars.xml')
cap = cv2.VideoCapture('C:/Users/broca/Programmation/Projets/En cours/Radar/Recherches/webcam-autoroutefr-a-11h09-ce-samedi.mp4')

if cap.isOpened() == False:
    print("ERROR : Can't open Video file")
else:
    print("Video file opened")



while cap.isOpened():
    ret, frame = cap.read()
    
    if ret == False:
        print("Video file closed")
        break

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray,1.8,2)

    
    for (x,y,w,h) in cars:
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h), (0,255,0),2)
    
    
    cv2.imshow('Cars', frame)

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
print("All tasks are done ")
