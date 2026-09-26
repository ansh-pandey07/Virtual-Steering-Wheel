import time


class FPSCounter:
    def __init__(self):

        self.prev_time = time.perf_counter()
        self.current_fps = 0
        self.avg_fps = 0

        self.frame_count = 0
        self.start_time = time.perf_counter()

    def update(self):

        current_time = time.perf_counter()

        delta = current_time - self.prev_time

        if delta > 0:
            self.current_fps = 1 / delta

        self.prev_time = current_time

        self.frame_count += 1

        elapsed = current_time - self.start_time

        if elapsed > 0:
            self.avg_fps = self.frame_count / elapsed

        return int(self.current_fps)

    def get_average_fps(self):

        return int(self.avg_fps)

    def reset(self):

        self.prev_time = time.perf_counter()
        self.start_time = time.perf_counter()

        self.frame_count = 0
        self.current_fps = 0
        self.avg_fps = 0