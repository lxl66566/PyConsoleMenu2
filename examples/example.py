from PyConsoleMenu2 import BaseMenu, FunctionalMenu, MultiMenu

# basic usage, get the index
ret = BaseMenu("title: BaseMenu").add_options(["a", "b", "c"]).run()
print(ret)

# get the name, and more options
ret = (
    BaseMenu("title: BaseMenu")
    .add_options(["a", "b", "c"])
    .add_option("d")
    .default_index(1)
    .prefix("[")
    .suffix("]")
    .raise_when_too_small()
    .run_get_item()
)
print(ret)

# multi selection
ret = MultiMenu("title: MultiMenu").max_count(2).add_options(["a", "b", "c"]).run()
print(ret)

# callback selection
func = (
    FunctionalMenu("title: FunctionalMenu")
    .add_option("a", lambda: print("a"))
    .add_options([("b", lambda: print("b")), ("c", lambda: print("c"))])
    .run_get_item()
)
func()
