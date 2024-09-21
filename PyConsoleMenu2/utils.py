from curses import KEY_CANCEL, KEY_DOWN, KEY_ENTER, KEY_EXIT, KEY_UP
from enum import Enum
from typing import Optional


class KeyboardAction(Enum):
    UP = (KEY_UP, ord("w"), ord("k"))
    DOWN = (KEY_DOWN, ord("s"), ord("j"))
    APPROVE = (KEY_ENTER, ord("\n"))
    SELECT = (ord(" "),)
    CANCEL = (KEY_CANCEL, KEY_EXIT, ord("q"), 3)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def from_key(key: int) -> Optional["KeyboardAction"]:
        for action in KeyboardAction:
            if key in action.value:
                return action
        return None
