import sys

from PySide6.QtWidgets import QApplication

from overlay import Overlay

app = QApplication(sys.argv)

window = Overlay()

window.show()

window.updateData(32,"YES",60,"Connected")

sys.exit(app.exec())