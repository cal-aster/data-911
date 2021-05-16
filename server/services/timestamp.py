from datetime import datetime


class Timestamps:
    def __init__(self) -> None:
        pass

    def now(self) -> int:
        return int(datetime.now().timestamp())
