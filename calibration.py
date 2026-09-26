import math


class Calibration:

    def __init__(self):

        self.center_angle = 0
        self.center_distance = 0

        self.calibrated = False

    def calibrate(self, left, right):

        x1, y1 = left
        x2, y2 = right

        self.center_angle = math.degrees(
            math.atan2(
                y2-y1,
                x2-x1
            )
        )

        self.center_distance = math.dist(left,right)

        self.calibrated = True

    def get_angle(self):

        return self.center_angle

    def get_distance(self):

        return self.center_distance