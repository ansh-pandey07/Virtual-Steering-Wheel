import cv2
import mediapipe as mp


class HandTracker:

    def __init__(
        self,
        max_hands=2,
        detection_confidence=0.7,
        tracking_confidence=0.7
    ):

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )

        self.drawer = mp.solutions.drawing_utils

    def find_hands(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        detected = []

        if results.multi_hand_landmarks and results.multi_handedness:

            h, w, _ = frame.shape

            for landmarks, handedness in zip(
                results.multi_hand_landmarks,
                results.multi_handedness
            ):

                # Draw Hand Skeleton
                self.drawer.draw_landmarks(
                    frame,
                    landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.drawer.DrawingSpec(
                        color=(0, 255, 0),
                        thickness=2,
                        circle_radius=2
                    ),
                    self.drawer.DrawingSpec(
                        color=(255, 255, 255),
                        thickness=2
                    )
                )

                # Store all 21 landmarks
                points = []

                for lm in landmarks.landmark:

                    x = int(lm.x * w)
                    y = int(lm.y * h)

                    points.append((x, y))

                # Wrist
                wrist = points[0]

                # Palm Center (average of key landmarks)
                palm_x = (
                    points[0][0]
                    + points[5][0]
                    + points[9][0]
                    + points[13][0]
                    + points[17][0]
                ) // 5

                palm_y = (
                    points[0][1]
                    + points[5][1]
                    + points[9][1]
                    + points[13][1]
                    + points[17][1]
                ) // 5

                detected.append({

                    "label": handedness.classification[0].label,

                    "score": handedness.classification[0].score,

                    "wrist": wrist,

                    "palm": (palm_x, palm_y),

                    "landmarks": points

                })

        return frame, detected
    
    def is_index_up(self, hand):

        lm = hand["landmarks"]

        # Index finger
        index_up = (
            lm[8][1] < lm[6][1]
        )

        # Middle
        middle_down = (
            lm[12][1] > lm[10][1]
        )

        # Ring
        ring_down = (
            lm[16][1] > lm[14][1]
        )

        # Pinky
        pinky_down = (
            lm[20][1] > lm[18][1]
        )

        return (
            index_up
            and middle_down
            and ring_down
            and pinky_down
        )