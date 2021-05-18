import cv2
import PySimpleGUI as sg
import os

# ---------------------------------------------------------------------------- #
#                      Set the parameters of the window :                      #
# ---------------------------------------------------------------------------- #

# ---------------------------------- Layout ---------------------------------- #

#Set the elements of the left column, where we will set the parameters of the radar :
param_col = [
        [
            sg.Text("Select the control area : ")
        ],
        [
            sg.Text("X1", size=(5,1), pad=(15,0)),
            sg.Text("Y1", size=(5,1)),
            sg.Text("X2", size=(5,1)),
            sg.Text("Y2", size=(5,1)),
            sg.Text("X3", size=(5,1)),
            sg.Text("Y3", size=(5,1)),
            sg.Text("X4", size=(5,1)),
            sg.Text("Y4", size=(5,1)),
        ],
        [
            sg.Slider((0,1), 0.5, 0.001, orientation="v", size=(5,8), key="-X1 SLIDER-"),
            sg.Slider((0,1), 0.5, 0.001, orientation="v", size=(5,8), key="-Y1 SLIDER-"),
            sg.Slider((0,1), 0.5, 0.001, orientation="v", size=(5,8), key="-X2 SLIDER-"),
            sg.Slider((0,1), 0.5, 0.001, orientation="v", size=(5,8), key="-Y2 SLIDER-"),
            sg.Slider((0,1), 0.5, 0.001, orientation="v", size=(5,8), key="-X3 SLIDER-"),
            sg.Slider((0,1), 0.5, 0.001, orientation="v", size=(5,8), key="-Y3 SLIDER-"),
            sg.Slider((0,1), 0.5, 0.001, orientation="v", size=(5,8), key="-X4 SLIDER-"),
            sg.Slider((0,1), 0.5, 0.001, orientation="v", size=(5,8), key="-Y4 SLIDER-"),
            sg.Spin([i for i in range(256)],0, key="-SPIN-")
        ],
        [
            sg.Text("Distance between detection lines : "),
            sg.InputText( "dist", key="DIST", size=(15,5))
        ],
        [
            sg.Text("Image folder"),
            sg.In( size = (25,1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Checkbox("Start detection : ", default=False, key="-START DETECTION-")
        ]
]

#Set the elements of the display column on th right, where the video flow will take place :
display_col = [
    [
        sg.Text("Video stream :")
    ],
    [
        sg.Image(key="-IMAGE-")
    ]
]

#Assemble the final layout in 2 columns :
layout = [
    [
        sg.Column(param_col),
        sg.VerticalSeparator(),
        sg.Column(display_col)
    ]
]

# -------------------------------- The window -------------------------------- #

#Create the window and set it's parameters :
window = sg.Window("Radar", layout = layout)


# ---------------------------------------------------------------------------- #
#                                     Radar                                    #
# ---------------------------------------------------------------------------- #

# --------------------------------- Variables -------------------------------- #


path = os.getcwd() #Path to the current working directory
classifier_name = path + '/' + 'cars.xml' #Path to the classifier
video_src = path + '/' + 'highway_webcam.mp4' #Path to the video source

cap = cv2.VideoCapture(video_src) #Start to capture the video source
car_cascade = cv2.CascadeClassifier(classifier_name) #Initialize the cascade classifier
index = 0 #Init of index
frame_size = [0,0] #Init frame size to 0's

coords = [[0,0,0,0],[0,0,0,0]] #Create an array to store the coords of the detection area

#Coords of the detection area : The area where the program will look for cars
control_area = [int(min(min(coords[0]) * 1.1,frame_size[0])), 
                int(min(min(coords[1]) * 1.1,frame_size[1])),
                int(max(max(coords[0]) * 1.1, 0)),
                int(max(max(coords[1]) * 1.1, 0))
               ] 
dist = None #Distance between the 2 lines of detections (Unit : meters)

# --------------------------------- Functions -------------------------------- #

def crop_frame(frame, rect):
    '''
    crop_frame() is a function that crop the given image around the rectangle (x,y,width,height) passed as a parameter.Returns the cropped picture.
    Inputs : Array (frame), list or tuple (rect)
    Outputs : Array (output_img)
    '''
    x, y, w, h = rect #Get the x, y position and the width and height of the rectangle

    output_img = frame[y:y+h,x:x+w] #Crop the frame [y0 to y1, x0 to x1]
    return output_img #Return the cropped image

def find_cars(frame,classifier):
    '''
    find_cars() is take an image and a 'car' haar cascade classifier as parameters and will look for cars on the given picture. 
    For each car it finds, the function raws on the frame a rectangle around the car. Returns the frame with rectangles and the list of coords of these rectangles.
    Inputs : Array (frame), cv2.CascadeClassifier(classifier)
    Outputs : Array(frame), list(cars)
    '''
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #Convert to grayscale image
    
    #Crop the frame to keep only the contro area
    detect_frame = crop_frame(gray, control_area) #Select a restrected area to control

    #Origin (x,y) of the control area in the global frame
    origin_x = control_area[0] 
    origin_y = control_area[1]

    cars = classifier.detectMultiScale(detect_frame,1.8,2) #Find cars in the control area

    for (x,y,w,h) in cars:
        frame = cv2.rectangle(frame,(origin_x+x,origin_y+y),(origin_x+x+w,origin_y+y+h), (0,255,0),2) #Draw rectangles around each detected car

    return frame, cars #Return the frame with drawn rectangles and there coords

def save_cars(frame= [] ,cwd = path, index = 0, car_list= []):
    '''
    save_cars() saves the picture of all cars stored in car_list in the 'Infringement' directory. If it doesn't exist, the functions create the dir.
    Parameters :
        frame : The input image that will be crop to save only the detected car.
        cwd : current working directory. The function need to know the path to its location to be able to create the 'Infringement' directory if it doesn't exist or if the cwd is already 'Infringement'
        index : An integer that increments for each new saved picture to give a different name to all saved picts
        car_list : A list that store al the coords of the detected cars that must be saved. Coords format : (x,y,width,height)
    Inputs : Array(frame), str(cwd), int(index), list(car_list)
    Outputs : int(index)
    '''
    try :
        assert os.getcwd() != 'Infringement' #If cwd is 'Infringement', raise an AssertException
        os.mkdir('Infringement') #Try to create a new directory : 'Infringement'
        #print("##### Infringement directory doesn't exist ##### \n >>'Infringement' directory created !") #Confirm the directory creation
        os.chdir(cwd + '/Infringement')
    except FileExistsError :
        #print("##### 'Infringement' directory already exists #####") #If 'Infringement' already exists, do nothing and print it in the console
        os.chdir(cwd + '/Infringement') #Enter in the 'Infringement' directory
    except AssertionError: #If the cwd is already 'Infringement', continue
        pass

    cwd = os.getcwd() #Store the cwd
    #print("cwd : {}".format(cwd))

    for elements in car_list:
        filename = 'Car' + str(index) + '.jpg' #Format the filename
        cv2.imwrite(filename, crop_frame(frame, elements)) #Save the picture in 'Infringement'
        print(">> {} was saved in '/Infringement'".format(filename)) #Confirm saving
        index += 1

    new_cwd = cwd[:-13]
    #print("new_cwd : {}".format(new_cwd))

    os.chdir(new_cwd)
    return index

# ---------------------------------------------------------------------------- #
#                                     Loop                                     #
# ---------------------------------------------------------------------------- #

while cap:
    event, values = window.read(timeout=20) #Read the events and their values in the window
    ret, frame = cap.read() #Read the video source
    frame_size = frame.shape[:2] #Get the frame size

    try :
        #Try to store Sliders values in coords
        coords = [
            int(values["-X1 SLIDER-"] * frame_size[0]), int(values["-X2 SLIDER-"] * frame_size[0]), #X1 and X2 values
            int(values["-X3 SLIDER-"] * frame_size[0]), int(values["-X4 SLIDER-"] * frame_size[0]), #X3 and X4 values
            int(values["-Y1 SLIDER-"] * frame_size[1]), int(values["-Y2 SLIDER-"] * frame_size[1]), #Y1 and Y2 values
            int(values["-Y3 SLIDER-"] * frame_size[1]), int(values["-Y4 SLIDER-"] * frame_size[1]) #Y3 and Y4 values
        ]
    except: #When we close the window, Sliders values become 'None' and that lead to an error because None isn't an iterable value, so we except errors and warn the user of the error

        print("Error in coords !")

    frame = cv2.rectangle(frame, (control_area[0],control_area[1]),(control_area[2],control_area[3]), (255,0,0),2) #Show the control area

    #Show the detection lines
    pt1 = (coords[0],coords[4])
    pt2 = (coords[1],coords[5])
    pt3 = (coords[2],coords[6])
    pt4 = (coords[3],coords[7])
    frame = cv2.line(frame, pt1, pt2, (0,255,0), 2) #top line
    frame = cv2.line(frame, pt3, pt4, (0,255,0), 2) #Bottom line
    frame = cv2.line(frame, pt1, pt3, (0,255,0), 2) #Left line
    frame = cv2.line(frame, pt2, pt4, (0,255,0), 2) #Right line

    print(coords)
    print(values["-SPIN-"])
    if event == sg.WINDOW_CLOSED or cap.isOpened == False or (cv2.waitKey(10) & 0xFF == ord('q')): #Conditions to stop the program
        break

    #Break the infinit loop if no more pictures in the video source
    if ret == False:
        print("Video file closed")
        break

    #Start the detection only if the box is checked
    if values["-START DETECTION-"]:
        frame, cars = find_cars(frame, car_cascade) #Locate the cars in the detection zone
        index = save_cars(frame, path, index, cars) #Save the picture of the selected cars

    imgbytes = cv2.imencode(".png",frame)[1].tobytes() #Convert current frame to a '.png' in a variable
    window["-IMAGE-"].update(data = imgbytes) #Update the Image() in the window with the current frame

    #Show the actual frame with rectangles in a cv2 window
    #cv2.imshow('Cars', frame)

#Release the capture and destroy all created windows at the end of the program
cap.release()
cv2.destroyAllWindows()
print("All tasks are done ") #Confirm the end of the program

print(frame_size)
