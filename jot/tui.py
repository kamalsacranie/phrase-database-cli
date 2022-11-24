import pytermgui as ptg
from sqlalchemy.sql.schema import Table
from controller import Controller
from config import CONFIG

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


def add_entry_view(
    manager: ptg.WindowManager,
    window: ptg.Window,
    table_name: Table | str,
    *args,
) -> None:
    manager.remove(window)
    window = ptg.Window(
        ptg.InputField("", prompt="Phrase: "),
        ptg.InputField("", prompt="Page number: "),
        ptg.Button(
            "Add entry",
            lambda *_: add_entry_view(manager, window, table_name=table),
        ),
        width=200,
        box="DOUBLE",
    )
    manager.add(window)


def column_list(
    column_index: int, column_name: str, elements: tuple[tuple[str]]
) -> list[ptg.Label]:
    column_name_label: ptg.Label = ptg.Label(column_name.title() or "No label")
    column_list = [ptg.Label(str(i[column_index])) for i in elements]
    column_list.insert(0, column_name_label)
    return column_list


def table_view(manager: ptg.WindowManager, window: ptg.Window, *args) -> None:
    manager.remove(window)
    # Accessing the label of our table which is also the name
    table = c.get_table(args[0][0].label)
    column_names = c.get_table_columns(table)
    elements = c.get_table_elements(table)
    populated_columns = [
        column_list(column_names.index(name), name, elements)
        for name in column_names
    ]
    window = ptg.Window(
        # Make config option to switch on and off pk
        ptg.Splitter(*[ptg.Container(*i) for i in populated_columns])
        if len(elements) > 0
        else ptg.Label("You have no entries in this table"),
        ptg.Button(
            "Add entry",
            lambda *_: add_entry_view(manager, window, table_name=table),
        ),
        width=200,
        box="DOUBLE",
    )
    manager.add(window)


def first_window(manager: ptg.WindowManager, window: ptg.Window):
    manager.remove(window)
    tables = [i.name for i in c.get_tables()]
    table_buttons = [
        ptg.Button(table, lambda *_: table_view(manager, window, _))
        for table in tables
    ]
    window = ptg.Window(
        *table_buttons
        if len(tables) > 0
        else ptg.Label("You have no tables yet."),
        # Must figure out a dynamic way to gen line
        "-" * (window.width - 10),
        ["Create table", lambda *_: create_new_jot(manager, window)],
        title="Your Jots",
        width=60,
        box="DOUBLE",
    )
    manager.add(window)
    return window


def start_tui():
    with ptg.WindowManager() as manager:
        window = ptg.Window(
            ptg.Button(
                "Start", onclick=lambda *_: first_window(manager, window)
            ),
            width=60,
            box="DOUBLE",
        )
        manager.add(window)


if __name__ == "__main__":
    start_tui()
