import pytermgui as ptg


def create_new_jot(manager: ptg.WindowManager, window: ptg.Window) -> None:
    manager.remove(window)
    window = ptg.Window(
        ["THIS WORKS", lambda *_: first_window(manager, window)],
        width=60,
        box="DOUBLE",
    )
    manager.add(window)


def first_window(manager: ptg.WindowManager, window: ptg.Window):
    manager.remove(window)
    window = ptg.Window(
        ["NO WAYS", lambda *_: create_new_jot(manager, window)],
        width=60,
        box="DOUBLE",
    )
    manager.add(window)


with ptg.WindowManager() as manager:
    window = ptg.Window(
        ["INTRO", lambda *_: create_new_jot(manager, window)],
        width=60,
        box="DOUBLE",
    )
    manager.add(window)
