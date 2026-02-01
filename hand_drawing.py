import cv2 as cv
import mediapipe as mp
import math
import numpy as np


def hand_drawing():
    cap = cv.VideoCapture(0)
    mp_hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mp_drawing = mp.solutions.drawing_utils

    ret, frame = cap.read()
    h, w = frame.shape[:2]

    canvas = np.zeros((h, w, 3), np.uint8)

    # state
    drawing = False
    prev_x, prev_y = None, None

    # palette
    colors = [
        ((0, 0, 255), "Red"),
        ((0, 255, 0), "Green"),
        ((255, 0, 0), "Blue"),
        ((0, 255, 255), "Yellow"),
        ((255, 0, 255), "Magenta"),
        ((255, 255, 255), "White"),
    ]
    current_color_idx = 0
    brush_size = 4
    eraser_active = False
    eraser_size = 30

    # UI layout
    PAL_Y = 35
    PAL_START_X = 35
    PAL_SPACING = 55
    PAL_RADIUS = 22

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        frame = cv.flip(frame, 1)
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = mp_hands.process(frame_rgb)

        finger_in_ui = False
        hand_detected = False

        if results.multi_hand_landmarks:
            hand_detected = True

            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

                # détection : index levé, les autres repliés
                index_up = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
                middle_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
                ring_up = hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y
                pinky_up = hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y
                thumb_up = hand_landmarks.landmark[4].x < hand_landmarks.landmark[2].x

                only_index_up = index_up and not middle_up and not ring_up and not pinky_up and not thumb_up

                # position de l'index
                index_finger = hand_landmarks.landmark[8]
                x = int(index_finger.x * w)
                y = int(index_finger.y * h)

                # --- sélection couleur / gomme ---
                if only_index_up:
                    for i in range(len(colors)):
                        cx = PAL_START_X + i * PAL_SPACING
                        if math.sqrt((x - cx) ** 2 + (y - PAL_Y) ** 2) < PAL_RADIUS + 8:
                            finger_in_ui = True
                            current_color_idx = i
                            eraser_active = False

                    # gomme
                    eraser_cx = PAL_START_X + len(colors) * PAL_SPACING
                    if math.sqrt((x - eraser_cx) ** 2 + (y - PAL_Y) ** 2) < PAL_RADIUS + 8:
                        finger_in_ui = True
                        eraser_active = True

                # --- dessin ---
                if not finger_in_ui:
                    if only_index_up:
                        if not drawing:
                            drawing = True
                            prev_x, prev_y = x, y

                        if prev_x is not None and prev_y is not None:
                            if eraser_active:
                                temp = np.zeros((h, w), np.uint8)
                                cv.line(temp, (prev_x, prev_y), (x, y), 255, eraser_size)
                                canvas[temp > 0] = [0, 0, 0]
                            else:
                                cv.line(canvas, (prev_x, prev_y), (x, y),
                                        colors[current_color_idx][0], brush_size)

                        prev_x, prev_y = x, y
                    else:
                        drawing = False
                        prev_x, prev_y = None, None
                else:
                    drawing = False
                    prev_x, prev_y = None, None

                # préview du doigt
                preview_size = eraser_size // 2 if eraser_active else max(brush_size // 2, 3)
                preview_color = (100, 100, 100) if eraser_active else colors[current_color_idx][0]
                cv.circle(frame, (x, y), preview_size, preview_color, 2)

                # indicateur visuel
                status_color = (0, 255, 0) if only_index_up else (0, 0, 180)
                cv.circle(frame, (x, y), preview_size + 5, status_color, 2)

        if not hand_detected:
            drawing = False
            prev_x, prev_y = None, None

        # overlay canvas
        mask = cv.cvtColor(canvas, cv.COLOR_BGR2GRAY)
        mask = cv.threshold(mask, 1, 255, cv.THRESH_BINARY)[1]
        frame[mask > 0] = canvas[mask > 0]

        # --- UI ---
        overlay = frame.copy()
        cv.rectangle(overlay, (0, 0),
                     (PAL_START_X + len(colors) * PAL_SPACING + 45, 75), (0, 0, 0), -1)
        frame = cv.addWeighted(overlay, 0.55, frame, 0.45, 0)

        # palette couleurs
        for i, (color, name) in enumerate(colors):
            cx = PAL_START_X + i * PAL_SPACING
            cv.circle(frame, (cx, PAL_Y), PAL_RADIUS, color, -1)
            cv.circle(frame, (cx, PAL_Y), PAL_RADIUS, (180, 180, 180), 2)
            if i == current_color_idx and not eraser_active:
                cv.circle(frame, (cx, PAL_Y), PAL_RADIUS + 4, (255, 255, 255), 3)

        # gomme
        eraser_cx = PAL_START_X + len(colors) * PAL_SPACING
        cv.circle(frame, (eraser_cx, PAL_Y), PAL_RADIUS, (60, 60, 60), -1)
        cv.circle(frame, (eraser_cx, PAL_Y), PAL_RADIUS, (180, 180, 180), 2)
        if eraser_active:
            cv.circle(frame, (eraser_cx, PAL_Y), PAL_RADIUS + 4, (255, 255, 255), 3)
        cv.putText(frame, "E", (eraser_cx - 6, PAL_Y + 7),
                   cv.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 2)

        cv.imshow("Hand Drawing", frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    hand_drawing()