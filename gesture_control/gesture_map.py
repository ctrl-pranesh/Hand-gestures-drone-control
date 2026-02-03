# gesture_control/gesture_map.py
"""
Single-hand only gesture rules for the hackathon prototype.
Provides detect_gesture_from_results(hands_landmarks) so mediapipe_gestures.py
does not need to be changed.

Recognized gestures:
 "FORWARD","BACK","LEFT","RIGHT","UP","DOWN","STOP","UNKNOWN"
(Only single-hand detection — ignores any second hand.)
"""

FINGER_TIPS = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky

def fingers_up(landmarks):
    """Return list of booleans for thumb,index,middle,ring,pinky being 'up'."""
    up = []
    for i, tip in enumerate(FINGER_TIPS):
        tip_x, tip_y, _ = landmarks[tip]
        if i == 0:
            # Thumb heuristic: compare tip x to IP joint x (works for right hand; ok for demo)
            ip_x = landmarks[3][0]
            up.append(tip_x > ip_x)
        else:
            pip_y = landmarks[tip - 2][1]
            up.append(tip_y < pip_y)
    return up

def palm_open(landmarks):
    """True if most fingers except thumb are open."""
    up = fingers_up(landmarks)
    return sum(up[1:]) >= 3  # index..pinky mostly up

def fist(landmarks):
    """True if almost all fingers are down."""
    up = fingers_up(landmarks)
    return sum(up) == 0

def left_right(landmarks, threshold=0.06):
    wrist_x = landmarks[0][0]
    index_mcp_x = landmarks[5][0]
    diff = index_mcp_x - wrist_x

    # SWAPPED:
    if diff < -threshold:
        return "RIGHT"   # previously LEFT
    if diff > threshold:
        return "LEFT"    # previously RIGHT

    return None


def up_down(landmarks, threshold=0.06):
    """Detect vertical offset: RETURN 'UP' or 'DOWN' or None."""
    wrist_y = landmarks[0][1]
    index_tip_y = landmarks[8][1]
    diff = wrist_y - index_tip_y
    if diff > threshold:
        return "UP"
    if diff < -threshold:
        return "DOWN"
    return None

def detect_single_hand(landmarks):
    """Core single-hand rules returning gesture string."""
    if landmarks is None:
        return "UNKNOWN"
    try:
        # STOP: closed fist
        if fist(landmarks):
            return "STOP"

        # If palm is open, prefer left/right/up/down or forward
        if palm_open(landmarks):
            lr = left_right(landmarks)
            if lr:
                return lr
            ud = up_down(landmarks)
            if ud:
                return ud
            return "FORWARD"

        # Finger-specific heuristics
        up = fingers_up(landmarks)
        # index up only => FORWARD
        if up[1] and not any([up[2], up[3], up[4]]):
            return "FORWARD"
        # thumb up only => UP
        if up[0] and not any(up[1:]):
            return "UP"

        # fallback lateral/vertical detection
        lr = left_right(landmarks)
        if lr:
            return lr
        ud = up_down(landmarks)
        if ud:
            return ud

        return "UNKNOWN"
    except Exception:
        return "UNKNOWN"

def detect_gesture_from_results(hands_landmarks):
    """
    Public API used by mediapipe_gestures.py.

    hands_landmarks: list where each element is a list of 21 (x,y,z) landmarks.
    This implementation uses ONLY the first detected hand (if any).
    """
    if not hands_landmarks:
        return "UNKNOWN"
    # Use the first detected hand only
    return detect_single_hand(hands_landmarks[0])
