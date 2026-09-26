class SmoothAngle:
    def __init__(self, alpha=0.15):
        """
        alpha:
        0.05 = Very Smooth (Slow Response)
        0.15 = Recommended
        0.30 = Fast Response
        """

        self.alpha = alpha
        self.value = 0
        self.initialized = False

    def update(self, new_value):

        # First value
        if not self.initialized:
            self.value = new_value
            self.initialized = True
            return self.value

        # Exponential Moving Average
        self.value = (
            self.alpha * new_value
            + (1 - self.alpha) * self.value
        )

        return self.value

    def reset(self):
        self.value = 0
        self.initialized = False

    def set_alpha(self, alpha):
        self.alpha = alpha