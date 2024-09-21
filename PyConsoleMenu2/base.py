import curses
import platform
from abc import ABC
from contextlib import suppress
from typing import Any, Callable, Dict, List

import _curses

from .utils import KeyboardAction


class BaseMenu(ABC):
    def __init__(
        self,
        title: str = "",
    ):
        self.stdscr: curses._CursesWindow
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
            KeyboardAction.CANCEL: self._cancel,
        }
        self._raise_when_too_small = False

    def add_option(self, option: str):
        """
        add an option
        """
        self._options.append(option)
        return self

    def add_options(self, options: List[str]):
        """
        add a list of options
        """
        self._options.extend(options)
        return self

    def default_index(self, index: int):
        """
        set default selected index
        """
        self._index = index
        return self

    def prefix(self, indicator: str):
        """
        set custom indicator at the beginning of selected item
        """
        self._prefix = indicator
        return self

    def suffix(self, indicator: str):
        """
        set custom indicator at the end of selected item
        """
        self._suffix = indicator
        return self

    def raise_when_too_small(self, value: bool = True):
        """
        whether raise exception if console is too small to render menu
        """
        self._raise_when_too_small = value
        return self

    def on_user_cancel(self, func: Callable):
        """
        Do something when user cancel the input. This will replace the default behavior,
        which raises a KeyboardInterrupt exception.
        """
        self._control_config[KeyboardAction.CANCEL] = func
        return self

    # region Private

    def _go_up(self):
        self._index = (self._index - 1) % len(self._options)

    def _go_down(self):
        self._index = (self._index + 1) % len(self._options)

    def _cancel(self):
        raise KeyboardInterrupt

    def _run_loop(self) -> Any:
        self.stdscr = curses.initscr()
        curses.raw()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        with suppress(_curses.error):
            curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0)
        while True:
            self._draw()
            key = self.stdscr.getch()
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

    def _draw(self):
        self.stdscr.clear()
        _, max_x = self.stdscr.getmaxyx()

        try:
            self._draw_title(max_x)
            self._draw_options(max_x)
        except _curses.error:
            if self._raise_when_too_small:
                raise Exception("This terminal is small to update information")

        self.stdscr.refresh()

    def _draw_title(self, max_x: int):
        if self._title:
            # hack: if titie contains CJK characters, the title will not show correctly
            self._y = (
                1 if platform.system() == "Windows" and not self._title.isascii() else 0
            )
            for line in self._title.split("\n"):
                self.stdscr.addnstr(self._y, 0, line, max_x)
                self._y += 1

    def _draw_options(self, max_x: int):
        for local_y, line in enumerate(self._options):
            if local_y == self._index:
                line = f"{self._prefix}{line}{self._suffix}"
            else:
                line = f'{" " * len(self._prefix)}{line}'
            self.stdscr.addnstr(self._y, 0, line, max_x)
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
        return self._run_loop()

    def run_get_item(self) -> str:
        """
        Return the name of selected option
        """
        return self._options[self.run()]
