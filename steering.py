import math


class Steering:
    def __init__(self):
        # Calibration
        self.center_angle = 0

        # Maximum steering angle
        self.max_angle = 90

        # Deadzone (ignore tiny movements)
        self.deadzone = 5

        # Sensitivity
        self.sensitivity = 1.0

    # -----------------------------
    # Raw angle between both hands
    # -----------------------------
    def calculate(self, left, right):

        x1, y1 = left
        x2, y2 = right

        angle = math.degrees(
            math.atan2(
                y2 - y1,
                x2 - x1
            )
        )

        angle -= self.center_angle

        angle *= self.sensitivity

        angle = max(-self.max_angle,
                    min(self.max_angle, angle))

        if abs(angle) < self.deadzone:
            angle = 0

        return angle

    # -----------------------------
    # Calibrate steering center
    # -----------------------------
    def calibrate(self, left, right):

        x1, y1 = left
        x2, y2 = right

        self.center_angle = math.degrees(
            math.atan2(
                y2 - y1,
                x2 - x1
            )
        )

    # -----------------------------
    # Angle -> Percentage
    # -----------------------------
    def get_percentage(self, angle):

        return int((angle / self.max_angle) * 100)

    # -----------------------------
    # Angle -> Joystick Value
    # (-32768 to 32767)
    # -----------------------------
    def joystick_value(self, angle):

        return int(
            (angle / self.max_angle) * 32767
        )

    # -----------------------------
    # Angle -> 0 to 1
    # -----------------------------
    def normalized(self, angle):

        return (angle + self.max_angle) / (2 * self.max_angle)