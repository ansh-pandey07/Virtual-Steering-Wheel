import cv2

class HUD:

    def draw(self, frame, fps, angle, hands):

        cv2.putText(
            frame,
            f"FPS : {fps}",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"Steering : {int(angle)}",
            (20,80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,255),
            2
        )

        cv2.putText(
            frame,
            f"Hands : {hands}",
            (20,120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,0),
            2
        )

        return frame