import time
import vgamepad as vg
while True:
    gamepad = vg.VX360Gamepad()

    print("Controller Connected!")

    gamepad.left_joystick(x_value=32767, y_value=0)
    gamepad.update()

    time.sleep(2)

    gamepad.left_joystick(x_value=0, y_value=0)
    gamepad.update()

    print("Done")
