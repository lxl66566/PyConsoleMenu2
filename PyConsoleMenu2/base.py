from abc import ABC
from curses import curs_set, use_default_colors, wrapper
from typing import Any, Callable, Dict, List

import _curses

from .utils import KeyboardAction


class BaseMenu(ABC):
    def __init__(
        self,
        title: str = "",
    ):
        self._y = 0
        self._title = title
        self._options: list[str] = []
        self._prefix = "->"
        self._suffix = ""
        self._index = 0
        self._control_config: Dict[KeyboardAction, Callable] = {
            KeyboardAction.UP: self._go_up,
            KeyboardAction.DOWN: self._go_down,
            KeyboardAction.APPROVE: self._get_selected_index,
        }
        self._raise_when_too_small = False

    def add_option(self, option: str) -> "BaseMenu":
        """
        add an option
        """
        self._options.append(option)
        return self

    def add_options(self, options: List[str]) -> "BaseMenu":
        """
        add a list of options
        """
        self._options.extend(options)
        return self

    def default_index(self, index: int) -> "BaseMenu":
        """
        set default selected index
        """
        self._index = index
        return self

    def prefix(self, indicator: str) -> "BaseMenu":
        """
        set custom indicator at the beginning of selected item
        """
        self._prefix = indicator
        return self

    def suffix(self, indicator: str) -> "BaseMenu":
        """
        set custom indicator at the end of selected item
        """
        self._suffix = indicator
        return self

    def raise_when_too_small(self, value: bool = True) -> "BaseMenu":
        """
        whether raise exception if console is too small to render menu
        """
        self._raise_when_too_small = value
        return self

    # region Private

    def _go_up(self):
        self._index = (self._index - 1) % len(self._options)

    def _go_down(self):
        self._index = (self._index + 1) % len(self._options)

    def _run_loop(self, screen) -> Any:
        use_default_colors()
        curs_set(0)
        while True:
            self._draw(screen)
            key = screen.getch()
            action = KeyboardAction.from_key(key)
            if action is None:
                continue
            func = self._control_config.get(action)
            if func is not None:
                ret = func()
                if action == KeyboardAction.APPROVE:
                    return ret

    def _get_selected_index(self) -> int:
        return self._index

    # region Drawers

    def _draw(self, screen):
        screen.clear()
        _, max_x = screen.getmaxyx()

        self._y = 0
        try:
            self._draw_title(screen, max_x)
            self._draw_options(screen, max_x)
        except _curses.error:
            if self._raise_when_too_small:
                raise Exception("This terminal is small to update information")

        screen.refresh()

    def _draw_title(self, screen, max_x: int):
        if self._title:
            for line in self._title.split("\n"):
                screen.addnstr(self._y, 0, line, max_x)
                self._y += 1

    def _draw_options(self, screen, max_x: int):
        for local_y, line in enumerate(self._options):
            if local_y == self._index:
                line = f"{self._prefix}{line}{self._suffix}"
            else:
                line = f'{" " * len(self._prefix)}{line}'
            screen.addnstr(self._y, 0, line, max_x)
            self._y += 1

    # region Public

    def run(self) -> int:
        """
        Return the index of selected option
        """

        if not self._options:
            raise ValueError("Options must be not empty")
        if 0 <= self._index >= len(self._options):
            raise ValueError("Default_index must be in [0, len(options) - 1]")
        return wrapper(self._run_loop)

    def run_get_item(self) -> str:
        """
        Return the name of selected option
        """
        return self._options[self.run()]
