import pytermgui as ptg

from controller import Controller
from main import CONFIG

c = Controller(CONFIG.db_path)

# Pro tip, you can literally use + to add stuff to the current window window + widget.value


def submit(manager: ptg.WindowManager, window: ptg.Window) -> None:
    form_data = {}
    for widget in window:
        if isinstance(widget, ptg.InputField):
            if widget.value == "":
                # Directing back if we do not have a value for widget
                create_new_jot(
                    manager,
                    window,
                    f"You did not fill in the '{widget.prompt}' field!",
                )
            # perhaps look at the serialisation object
            key = (
                widget.prompt.strip()
                .lower()
                .replace(" ", "_")
                .replace(":", "")
            )
            form_data[key] = widget.value
    c.add_new_table(form_data["table_name"])
    window = first_window(manager, window)
    manager.add(window)


def create_new_jot(
    manager: ptg.WindowManager, window: ptg.Window, *args
) -> None:
    manager.remove(window)
    window = ptg.Window(
        ptg.InputField("", prompt="Table name: "),
        ptg.Button("Create table", onclick=lambda *_: submit(manager, window)),
        *args,
        width=60,
        box="DOUBLE",
    )
    manager.add(window)


def table_view(manager: ptg.WindowManager, window: ptg.Window, *args) -> None:
    manager.remove(window)
    window = ptg.Window(
        ptg.InputField("", prompt="Table name: "),
        ptg.Button("Create table", onclick=lambda *_: submit(manager, window)),
        *args,
        width=60,
        box="DOUBLE",
    )
    manager.add(window)


def first_window(manager: ptg.WindowManager, window: ptg.Window):
    manager.remove(window)
    tables = [i.name for i in c.get_tables()]
    table_buttons = [
        [table, lambda *_: table_view(manager, window)] for table in tables
    ]
    window = ptg.Window(
        *table_buttons,
        ["Create table", lambda *_: create_new_jot(manager, window)],
        title="Your Jots",
        width=60,
        box="DOUBLE",
    )
    manager.add(window)
    return window


with ptg.WindowManager() as manager:
    # ["", lambda *_: create_new_jot(manager, window)],
    window = ptg.Window(
        ptg.Button("Start", onclick=lambda *_: first_window(manager, window)),
        width=60,
        box="DOUBLE",
    )
    manager.add(window)
