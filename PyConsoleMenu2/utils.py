from curses import KEY_DOWN, KEY_ENTER, KEY_UP
from enum import Enum
from typing import Optional


class KeyboardAction(Enum):
    UP = 1
    DOWN = 2
    APPROVE = 3
    SELECT = 4

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def from_key(key: int) -> Optional["KeyboardAction"]:
        if key in (KEY_UP, ord("w")):
            return KeyboardAction.UP
        if key in (KEY_DOWN, ord("s")):
            return KeyboardAction.DOWN
        if key in (KEY_ENTER, ord("\n")):
            return KeyboardAction.APPROVE
        if key == ord(" "):
            return KeyboardAction.SELECT

        return None
