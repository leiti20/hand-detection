import cv2 as cv 
import mediapipe as mp
import pyautogui
import math 


def hand_mouse_control():
    # start video capture
    cap = cv.VideoCapture(0)
    
    #initialize mediapipe hands
    mp_hands = mp.solutions.hands.Hands(max_num_hands=1)
    mp_drawing = mp.solutions.drawing_utils
    
    # get screen size
    screen_width , screen_height = pyautogui.size()

    # cliking state
    clicking = False
    pinch_threshold = 0.05  # distance in pixels to consider as pinch
    
    #process video frames
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue
        
        #convert frame to RGB
        frame = cv.flip(frame,1)
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = mp_hands.process(frame_rgb)
        
        #draw hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
                
                #get index finger tip position
                index_finger = hand_landmarks.landmark[8]
                x = int(index_finger.x * frame.shape[1])
                y = int(index_finger.y * frame.shape[0])
                
                #map to screen coordinates
                screen_x = int(index_finger.x * screen_width)
                screen_y = int(index_finger.y * screen_height)
                
                #move mouse
                pyautogui.moveTo(screen_x, screen_y)

                #check for pinch (click)
                thumb_finger = hand_landmarks.landmark[4]
                dx = thumb_finger.x - index_finger.x
                dy = thumb_finger.y - index_finger.y
                dist = math.sqrt(dx * dx + dy * dy)
                
                # Visual feedback: draw circle at pinch midpoint
                mid_x = int((index_finger.x + thumb_finger.x) / 2 * frame.shape[1])
                mid_y = int((index_finger.y + thumb_finger.y) / 2 * frame.shape[0])
                color = (0, 255, 0) if dist < pinch_threshold else (0, 0, 255)
                cv.circle(frame, (mid_x, mid_y), 15, color, -1)
                
                if dist < pinch_threshold and not clicking:
                    clicking = True
                    pyautogui.click()
                elif dist >= pinch_threshold and clicking:
                    clicking = False
        
        cv.imshow("Hand Mouse Control", frame)
        if cv.waitKey(1) & 0xFF == ord('q'): # quit with the 'q' key 
            break   
        
    cap.release()
    cv.destroyAllWindows()
    
if __name__ == "__main__":
    hand_mouse_control()
       
    
    
    
    
    
    
    

