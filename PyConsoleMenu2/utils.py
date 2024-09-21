from curses import KEY_CANCEL, KEY_DOWN, KEY_ENTER, KEY_EXIT, KEY_UP
from enum import Enum
from typing import Optional


class KeyboardAction(Enum):
    UP = (KEY_UP, ord("w"), ord("k"))
    DOWN = (KEY_DOWN, ord("s"), ord("j"))
    # KEY_ENTER could not be used in raw mode, so add 13
    APPROVE = (KEY_ENTER, ord("\n"), 13)
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
