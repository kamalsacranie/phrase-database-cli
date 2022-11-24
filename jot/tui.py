import pytermgui as ptg
from sqlalchemy.sql.schema import Table
from controller import Controller
from config import CONFIG

c = Controller(CONFIG.db_path)

# Pro tip, you can literally use + to add stuff to the current window window + widget.value


def submit_add_new_table(
    manager: ptg.WindowManager, window: ptg.Window
) -> None:
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


def submit_add_new_entry(
    manager: ptg.WindowManager, window: ptg.Window, table: Table
) -> None:
    form_data = {}
    for widget in window:
        if isinstance(widget, ptg.InputField):
            if widget.value == "":
                # Directing back if we do not have a value for widget
                pass
                # create_new_jot(
                #     manager,
                #     window,
                #     f"You did not fill in the '{widget.prompt}' field!",
                # )
            # perhaps look at the serialisation object
            key = (
                widget.prompt.strip()
                .lower()
                .replace(" ", "_")
                .replace(":", "")
            )
            form_data[key] = widget.value
    c.add_table_entry(table, form_data["phrase"], form_data["page_number"])
    window = table_view(manager, window, table=table)


def create_new_jot(
    manager: ptg.WindowManager, window: ptg.Window, *args
) -> None:
    manager.remove(window)
    window = ptg.Window(
        ptg.InputField("", prompt="Table name: "),
        ptg.Button(
            "Create table",
            onclick=lambda *_: submit_add_new_table(manager, window),
        ),
        *args,
        width=60,
        box="DOUBLE",
    )
    manager.add(window)


def add_entry_view(
    manager: ptg.WindowManager,
    window: ptg.Window,
    table: Table | str,
) -> None:
    manager.remove(window)
    window = ptg.Window(
        ptg.InputField("", prompt="Phrase: "),
        ptg.InputField("", prompt="Page number: "),
        ptg.Button(
            "Add entry",
            lambda *_: submit_add_new_entry(manager, window, table=table),
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


def table_view(
    manager: ptg.WindowManager, window: ptg.Window, *args, **kwargs
) -> None:
    manager.remove(window)
    # Accessing the label of our table which is also the name
    # Passing through our table if we have the Table object in kwargs else we
    # are passin through the table name string
    table = (
        # needs to be reworked as we should just create a table_name kwarg
        kwargs["table"]
        if "table" in kwargs.keys()
        else c.get_table(args[0][0].label)
    )
    column_names = c.get_table_columns(table)
    elements = c.get_table_elements(table)
    populated_columns = [
        column_list(column_names.index(name), name, elements)
        for name in column_names
    ]
    window = ptg.Window(
        # Make config option to switch on and off pk
        # We are goin g to need to set our column widths here. The only way I
        # can think to do this well is either hard code it or put it as an
        # option int eh config
        ptg.Splitter(
            *[
                ptg.Container(
                    *i,
                    width=len(
                        max(
                            [e.value for e in i],
                            key=len,
                        )
                    ),
                )
                for i in populated_columns[1:]
            ]
        )
        if len(elements) > 0
        else ptg.Label("You have no entries in this table"),
        ptg.Button(
            "Add entry",
            lambda *_: add_entry_view(manager, window, table=table),
        ),
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
