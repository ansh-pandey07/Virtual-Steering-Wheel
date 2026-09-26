import cv2

from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QFont, QImage, QPixmap, QGuiApplication


class Overlay(QWidget):

    def __init__(self):

        super().__init__()

        # -------------------------
        # Window
        # -------------------------

        self.setWindowTitle("AI Steering")

        self.resize(340, 470)

        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint
        )

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setStyleSheet("""
        QWidget{
            background-color:rgba(25,25,25,230);
            border-radius:18px;
        }

        QLabel{
            color:white;
            font-size:16px;
            background:transparent;
        }
        """)

        # Drag variables
        self.dragging = False
        self.dragPos = QPoint()

        # -------------------------
        # Title
        # -------------------------

        self.title = QLabel("🎮 AI Steering", self)
        self.title.setFont(QFont("Arial", 18, QFont.Bold))
        self.title.move(85, 15)

        # -------------------------
        # Camera Preview
        # -------------------------

        self.camera = QLabel(self)
        self.camera.setGeometry(20, 55, 300, 180)

        self.camera.setStyleSheet("""
        border:2px solid #666;
        border-radius:10px;
        background:black;
        """)

        # -------------------------
        # HUD
        # -------------------------

        self.angle = QLabel("Angle : 0°", self)
        self.angle.move(20, 255)

        self.grip = QLabel("Grip : NO", self)
        self.grip.move(20, 290)

        self.fps = QLabel("FPS : 0", self)
        self.fps.move(20, 325)

        self.controller = QLabel("Controller : OFF", self)
        self.controller.move(20, 360)

        self.positionText = QLabel(
            "1-TL  2-TR  3-BL  4-BR",
            self
        )
        self.positionText.move(20, 405)

        # Default Position
        self.setPosition("top_right")

    # =====================================================

    def updateFrame(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        h, w, ch = rgb.shape

        image = QImage(
            rgb.data,
            w,
            h,
            ch * w,
            QImage.Format_RGB888
        )

        pixmap = QPixmap.fromImage(image)

        self.camera.setPixmap(
            pixmap.scaled(
                self.camera.width(),
                self.camera.height(),
                Qt.KeepAspectRatio
            )
        )

    # =====================================================

    def updateData(self, angle, grip, fps, controller):

        self.angle.setText(
            f"Angle : {int(angle)}°"
        )

        self.grip.setText(
            f"Grip : {grip}"
        )

        self.fps.setText(
            f"FPS : {fps}"
        )

        self.controller.setText(
            f"Controller : {controller}"
        )

    # =====================================================

    def setPosition(self, position):

        screen = QGuiApplication.primaryScreen().availableGeometry()

        margin = 20

        w = self.width()
        h = self.height()

        if position == "top_left":

            self.move(
                margin,
                margin
            )

        elif position == "top_right":

            self.move(
                screen.width() - w - margin,
                margin
            )

        elif position == "bottom_left":

            self.move(
                margin,
                screen.height() - h - margin
            )

        elif position == "bottom_right":

            self.move(
                screen.width() - w - margin,
                screen.height() - h - margin
            )

    # =====================================================
    # Drag Window
    # =====================================================

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.dragging = True

            self.dragPos = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

            event.accept()

    def mouseMoveEvent(self, event):

        if self.dragging:

            self.move(
                event.globalPosition().toPoint()
                - self.dragPos
            )

            event.accept()

    def mouseReleaseEvent(self, event):

        self.dragging = False