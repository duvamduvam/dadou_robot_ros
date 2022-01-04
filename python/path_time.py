class PathTime:

    def __init__(self, path, time):
        self.path = path
        self.time = time

    def get_path(self, params) -> str:
        return self.path

    def get_time(self, params) -> int:
        return self.time
