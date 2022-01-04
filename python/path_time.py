class PathTime:

    def __init__(self, path, time):
        self.path = path
        self.time = time

    def get_path(self) -> str:
        return self.path

    def get_time(self) -> int:
        return self.time
