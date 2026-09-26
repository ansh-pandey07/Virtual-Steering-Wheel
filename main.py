import sys
import math
import cv2

from PySide6.QtWidgets import QApplication

from hand_tracker import HandTracker
from steering import Steering
from controller import VirtualController
from overlay import Overlay

from utils.smoothing import SmoothAngle
from utils.fps import FPSCounter
from calibration import Calibration

# =====================================
# QApplication
# =====================================

app = QApplication(sys.argv)

# =====================================
# Overlay
# =====================================

overlay = Overlay()
overlay.show()

# =====================================
# Camera
# =====================================

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# =====================================
# Classes
# =====================================

tracker = HandTracker()

steering = Steering()

controller = VirtualController()

smooth = SmoothAngle(alpha=0.15)

fps_counter = FPSCounter()

calibration = Calibration()

# =====================================
# Variables
# =====================================

left = None
right = None

angle = 0

grip = "NO"

controller_status = "Connected"

# =====================================
# Main Loop
# =====================================
left_index = False
right_index = False
while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    frame, hands = tracker.find_hands(frame)

    left = None
    right = None

    for hand in hands:

        if hand["label"] == "Left":

            left = hand["palm"]

            left_index = tracker.is_index_up(hand)

        elif hand["label"] == "Right":

            right = hand["palm"]

            right_index = tracker.is_index_up(hand)
    if right_index:

        cv2.putText(
            frame,
            "ACCELERATOR",
            (20,150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

    if left_index:

        cv2.putText(
            frame,
            "BRAKE",
            (20,190),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,0,255),
            2
        )
    if right_index:
        controller.throttle(255)
    else:
        controller.throttle(0)

    if left_index:
        controller.brake(255)
    else:
        controller.brake(0)
    # =====================================

    # Steering
    # =====================================

    if left and right:

        distance = math.dist(left, right)

        # Draw Hands
        cv2.circle(frame, left, 8, (0, 255, 0), -1)
        cv2.circle(frame, right, 8, (0, 0, 255), -1)

        cv2.line(frame, left, right, (255, 255, 255), 3)

        # Grip Detection
        if 180 < distance < 500:

            grip = "YES"

            raw_angle = steering.calculate(left, right)

            angle = smooth.update(raw_angle)

            joy = steering.joystick_value(angle)

            controller.steer(joy)

            percentage = steering.get_percentage(angle)

            center = (
                (left[0] + right[0]) // 2,
                (left[1] + right[1]) // 2
            )

            radius = int(distance / 2)

            cv2.circle(
                frame,
                center,
                radius,
                (255, 255, 255),
                3
            )

            cv2.circle(
                frame,
                center,
                5,
                (0, 255, 255),
                -1
            )

            # HUD
            cv2.putText(
                frame,
                f"Angle : {int(angle)}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Steering : {percentage}%",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

            cv2.putText(
                frame,
                "Grip : YES",
                (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        else:

            grip = "NO"

            angle = 0

            controller.steer(0)

    else:

        grip = "NO"

        angle = 0

        controller.steer(0)

    # =====================================
    # FPS
    # =====================================

    fps = fps_counter.update()

    # =====================================
    # Overlay Update
    # =====================================

    overlay.updateFrame(frame)

    overlay.updateData(
        angle,
        grip,
        fps,
        controller_status
    )

    app.processEvents()
        # =====================================
    # Keyboard Controls
    # =====================================

    key = cv2.waitKey(1) & 0xFF

    # Calibration
    if key == ord("c"):

        if left and right:

            calibration.calibrate(left, right)

            steering.calibrate(left, right)

            print("✅ Calibration Complete!")

    # Overlay Positions
    elif key == ord("1"):

        overlay.setPosition("top_left")

    elif key == ord("2"):

        overlay.setPosition("top_right")

    elif key == ord("3"):

        overlay.setPosition("bottom_left")

    elif key == ord("4"):

        overlay.setPosition("bottom_right")

    # Exit
    elif key == 27:

        break


# =====================================
# Cleanup
# =====================================

controller.reset()

cap.release()

cv2.destroyAllWindows()

sys.exit(app.exec())