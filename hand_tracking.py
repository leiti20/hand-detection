import cv2 as cv

import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def run_hand_tracking():
    # Start capturing video from the webcam.
    cap = cv.VideoCapture(index=0)
    
    # Initialize MediaPipe Hands.
    with mp_hands.Hands(
        model_complexity=0,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as hands:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
            
            frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)
       
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=hand_landmarks,
                        connections=mp_hands.HAND_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style(),
                        connection_drawing_spec=mp_drawing_styles.get_default_hand_connections_style()
                    )
                    
            cv.imshow('Hand Tracking', cv.flip(frame, 1))
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
if __name__ == "__main__":
    run_hand_tracking()