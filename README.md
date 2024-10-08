# PyConsoleMenu2

An extreamly easy to use Python console menu. (fork ver.)

Features:

- Cross platform, interactive selection
- Flexible Builder pattern
- Multi selection and Callback selection support

## Preview

![Selector](https://github.com/BaggerFast/PyConsoleMenu/blob/main/assets/selector.gif?raw=true)

[See other](https://github.com/BaggerFast/PyConsoleMenu/tree/main/assets)

## Installation 💾

```sh
pip install PyConsoleMenu2
```

## Usage example 👨‍💻

```py
from PyConsoleMenu2 import BaseMenu, ItemMenu, MultiMenu

# basic usage, get the index
ret = BaseMenu("title: BaseMenu").add_options(["a", "b", "c"]).run()
print(ret)  # 0 / 1 / 2

# get the name, and more options
ret = (
    BaseMenu("title: BaseMenu")
    .add_options(["a", "b", "c"])
    .add_option("d")
    .default_index(1)
    .prefix("[")
    .suffix("]")
    .raise_when_too_small()
    .on_user_cancel(lambda: print("cancel"))
    .run_get_item()
)
print(ret)  # a / b / c / d

# multi selection (use space to select)
ret = MultiMenu("title: MultiMenu").max_count(2).add_options(["a", "b", "c"]).run()
print(ret)

# each option related to an item. could be used as callback function.
func = (
    ItemMenu("title: ItemMenu")
    .add_option("a", lambda: print("a"))
    .add_options([("b", lambda: print("b")), ("c", lambda: print("c"))])
    .run_get_item()
)
func()
```

~~_[See more examples](https://github.com/lxl66566/PyConsoleMenu/tree/main/examples)_~~

## Document

- Three types of menus: _BaseMenu_ (only strings), _MultiMenu_ (multi selections), _ItemMenu_ (binds items to each option)
- Keybindings: [See code](./PyConsoleMenu2/utils.py)
- methods:
  - `run`: get index of selected option.
  - `run_get_item`: get the related item of selected option. Option string for _BaseMenu_, a set of string for _MultiMenu_, and user given item for _ItemMenu_.
  - `raise_when_too_small`: when set to True, raise a `error.RenderException`, otherwise ignore drawing.
  - `on_user_cancel`: exec a function when user cancel the input. If not set, raise `KeyboardInterrupt` by default.
  - ...

## Additional

There's problem when displaying CJK string on windows terminal, caused by upstream dependency [windows-curses](https://github.com/zephyrproject-rtos/windows-curses). But still usable.
