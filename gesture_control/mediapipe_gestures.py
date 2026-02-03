"""
Main program: captures webcam frames, runs MediaPipe Hands,
detects gesture using gesture_map, and dispatches via UDP or keyboard.
Supports two-hand gestures: BOOST and BRAKE.
Run: python mediapipe_gestures.py --mode udp
or   python mediapipe_gestures.py --mode keys
"""

import cv2
import mediapipe as mp
import argparse
import time
from gesture_map import detect_gesture_from_results

# senders
from sender_keys import send_key
from sender_udp import send_udp

mp_h = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def lm_list(landmark_proto):
    return [(p.x, p.y, p.z) for p in landmark_proto.landmark]

def main(mode="keys", cam_index=0):
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        print("Cannot open webcam")
        return

    with mp_h.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.5
    ) as hands:
        prev_gesture = None
        last_send = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            gesture = "UNKNOWN"
            hands_list = []
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    hands_list.append(lm_list(hand_landmarks))
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_h.HAND_CONNECTIONS)

                # detect using possibly two hands
                gesture = detect_gesture_from_results(hands_list)

            # show text
            cv2.putText(frame, f"Gesture: {gesture}", (10,30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv2.imshow("Hand Tracking", frame)

            now = time.time() * 1000
            if gesture != prev_gesture or (now - last_send) > 200:
                prev_gesture = gesture
                last_send = now
                if mode == "keys":
                    send_key(gesture)
                else:
                    send_udp(gesture)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["keys", "udp"], default="keys")
    parser.add_argument("--cam", type=int, default=0)
    args = parser.parse_args()
    main(mode=args.mode, cam_index=args.cam)
