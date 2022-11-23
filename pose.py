import cv2
import mediapipe as mp

print(cv2.__version__)

width=1280
height=720

points = (width,height)

cap = cv2.VideoCapture(0)

pose = mp.solutions.pose.Pose(static_image_mode=False, enable_segmentation=False, smooth_segmentation=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw=mp.solutions.drawing_utils

handRadius=20
handColor=(0,0,255)
handThickness=4

def lineLine(x1, y1, x2, y2, x3, y3, x4, y4):
    
    #calculate the direction of the lines
    uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
    uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))

    #if uA and uB are between 0-1, lines are colliding
    if (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1) :
        #optionally, draw a circle where the lines meet
        intersectionX = x1 + (uA * (x2-x1))
        intersectionY = y1 + (uA * (y2-y1))
        return True
    return False

#LINE/RECTANGLE
def lineRect(x1, y1, x2, y2, rx, ry, rw, rh):

    #check if the line has hit any of the rectangle's sides
    #uses the Line/Line function below
    left =   lineLine(x1,y1,x2,y2, rx,ry,rx, ry+rh)
    right =  lineLine(x1,y1,x2,y2, rx+rw,ry, rx+rw,ry+rh)
    top =    lineLine(x1,y1,x2,y2, rx,ry, rx+rw,ry)
    bottom = lineLine(x1,y1,x2,y2, rx,ry+rh, rx+rw,ry+rh)

    #if ANY of the above are true, the line has hit the rectangle
    if (left or right or top or bottom):
        return True

    return False
  
while True:
    ignore, frame = cap.read()
    frame = cv2.resize(frame, points,fx=0.5, fy=0.5,interpolation=cv2.INTER_AREA)
    #OpenCV reads images in BGR format. We need to convert it into RGB before passing it to mediapipe.
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    #Pass the RGB frame to process method of pose object. It will track the pose for you and give you the result.
    results = pose.process(frameRGB)
    #print(results)

    landMarks=[]
    if results.pose_landmarks != None:
        mpDraw.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
        #print(results.pose_landmarks)
        for lm in results.pose_landmarks.landmark:
            #print((lm.x, lm.y))
            landMarks.append((int(lm.x*width),int(lm.y*height)))
        
        cv2.circle(frame, landMarks[16], handRadius, handColor, handThickness)
        cv2.circle(frame, landMarks[20], handRadius, handColor, handThickness)
        cv2.circle(frame, landMarks[15], handRadius, handColor, handThickness)
        cv2.circle(frame, landMarks[19], handRadius, handColor, handThickness)

        #Line connecting left_elbow to left_wrist 
        cv2.line(frame,landMarks[13],landMarks[15],(255,0,0),handThickness)

        #Line connecting left_wrist to left_index
        cv2.line(frame,landMarks[15],landMarks[19],(255,0,0),handThickness)
        
        #Line connecting right_elbow to right_wrist 
        cv2.line(frame,landMarks[14],landMarks[16],(255,0,0),handThickness)

        #Line connecting right_elbow to right_wrist 
        cv2.line(frame,landMarks[16],landMarks[20],(255,0,0),handThickness)

        #Static bounding box
        cv2.rectangle(frame, (200,100),(280,150),(255,0,0),thickness = 3, lineType = cv2.LINE_AA)
        cv2.rectangle(frame, (500,500),(580,550),(255,0,0),thickness = 3, lineType = cv2.LINE_AA)

        x1,y1 = landMarks[19]
        x2=y2=0
        sx= 200
        sy= 100
        sw= 80
        sh= 50

        x1r,y1r = landMarks[20]

        hit = lineRect(x1,y1,x2,y2, sx,sy,sw,sh)
        if (hit):
            cv2.rectangle(frame, (200,100),(280,150),(250,150,0),3)
            print("ON")
        else:
            cv2.rectangle(frame, (200,100),(280,150),(0,150,255),3)
            print("OFF")

        hit = lineRect(x1,y1,x2,y2, 500,500,sw,sh)
        if (hit):
            cv2.rectangle(frame, (500,500),(580,550),(250,150,0),3)
            print("ON")
        else:
            cv2.rectangle(frame, (500,500),(580,550),(0,150,255),3)
            print("OFF")

        hit = lineRect(x1r,y1r,x2,y2, sx,sy,sw,sh)
        if (hit):
            cv2.rectangle(frame, (200,100),(280,150),(250,150,0),3)
            print("ON")
        else:
            cv2.rectangle(frame, (200,100),(280,150),(0,150,255),3)
            print("OFF")

        hit = lineRect(x1r,y1r,x2,y2, 500,500,sw,sh)
        if (hit):
            cv2.rectangle(frame, (500,500),(580,550),(250,150,0),3)
            print("ON")
        else:
            cv2.rectangle(frame, (500,500),(580,550),(0,150,255),3)
            print("OFF")

    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break
cap.release()