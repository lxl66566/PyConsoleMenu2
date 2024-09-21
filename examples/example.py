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
