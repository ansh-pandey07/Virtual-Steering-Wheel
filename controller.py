import vgamepad as vg


class VirtualController:

    def __init__(self):

        self.gamepad = vg.VX360Gamepad()

    def steer(self, value):

        value = max(-32768, min(32767, int(value)))

        self.gamepad.left_joystick(
            x_value=value,
            y_value=0
        )

        self.gamepad.update()

    def throttle(self, value):

        value = max(0, min(255, int(value)))

        self.gamepad.right_trigger(value)

        self.gamepad.update()

    def brake(self, value):

        value = max(0, min(255, int(value)))

        self.gamepad.left_trigger(value)

        self.gamepad.update()

    def reset(self):

        self.gamepad.reset()

        self.gamepad.update()