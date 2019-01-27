import cv2
from puzzle import puzzle

#block puzzle with video
previewScale = 1
imageScale = 1.5
starting_puzzle_size = 3
min_puzzle_size = 2
max_puzzle_size = 15

        
def toggle_trackbar(val):
    global p,img,imageScale,min_puzzle_size
    if val < min_puzzle_size:
        return
    else:
        begin_capture(val)
    


def begin_capture(size = starting_puzzle_size):
    p = None

    cap = cv2.VideoCapture(0)
    started = False
    while(True):
        _, frame = cap.read()
    
        preview = cv2.resize(frame,None,fx=previewScale, fy=previewScale, interpolation = cv2.INTER_CUBIC)
        cv2.imshow('preview',preview)
    
        if started == False:
            p = puzzle(frame, size, scale = imageScale)
            started = True
        else:
            p.update(frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return
 
cv2.namedWindow('preview')
cv2.createTrackbar('puzzle size','preview',starting_puzzle_size,max_puzzle_size,toggle_trackbar)       
begin_capture()
cv2.destroyAllWindows()



