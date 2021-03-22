# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

from datetime import datetime


class Timestamps:
    def __init__(self) -> None:
        pass

    def now(self) -> int:
        return int(datetime.now().timestamp())
