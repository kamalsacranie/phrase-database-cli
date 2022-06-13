import urwid

from controller import Controller

phrase_obj = Controller("../testing.db")


def menu(title, choices):
    # Setting up our title and divider. Think of these like both block HTML
    # elements which are read in from left to right
    body = [urwid.Text(title), urwid.Divider("━")]

    for choice in choices:
        button = urwid.Button(
            choice
        )  # Creating a button object so our connect signal can have something to "latch onto"
        urwid.connect_signal(
            button, "click", item_chosen, choice
        )  # Passing our button through and giving it the callback of item chosen
        body.append(
            urwid.AttrMap(button, None, focus_map="reversed"),
        )  # attrmap add our style when in and out of focus and then we add to body

    return urwid.ListBox(
        urwid.SimpleFocusListWalker(body)
    )  # List box is what we must use to display our body list


def item_chosen(button, choice):

    elements = phrase_obj.get_table_elements("the prince")
    sorted_elements_columns = tuple(zip(*elements))
    text_wrapped_columns = tuple(
        map(
            lambda column: urwid.SimpleFocusListWalker(
                tuple(map(lambda column: urwid.Button(str(column)), column))
            ),
            sorted_elements_columns,
        )
    )
    text_wrapped_columns = [
        (
            text_wrapped_columns.index(e) + 1,
            urwid.BoxAdapter(urwid.ListBox(e), 1),
        )
        for e in text_wrapped_columns
    ]  # We have to wrap our box ina  box adapter to make it flexible
    response = urwid.Columns(text_wrapped_columns, 1, None, 5, None)
    done = urwid.Button("Ok")  # creating another button
    urwid.connect_signal(done, "click", exit_program)
    # Resetting our main widget
    main.original_widget = urwid.Filler(
        urwid.Pile([response, urwid.AttrMap(done, None, focus_map="reversed")])
    )


def exit_program(button):
    raise urwid.ExitMainLoop()


table_names = phrase_obj.inspector.get_table_names()
# main = urwid.Padding(menu("Pythons", table_names), left=2, right=2)


def temp():
    return [
        urwid.Columns(
            [
                ("pack", urwid.Text("Testing")),
                ("pack", urwid.Text("Testing")),
                ("pack", urwid.Text("Testing")),
                ("pack", urwid.Text("Testing")),
            ]
        ),
        urwid.Columns(
            [
                (20, urwid.Text("Testing")),
                (20, urwid.Text("Testing")),
                (20, urwid.Text("dfklsajfdslajkfjlda dfasl ")),
                (20, urwid.Text("Testing")),
            ]
        ),
        urwid.Columns(
            [
                ("pack", urwid.Text("jfdklsj alfjd sal jl jldfsa")),
                ("pack", urwid.Text("Testing")),
                ("pack", urwid.Text("Testing")),
                ("pack", urwid.Text("Testing")),
            ]
        ),
    ]


main = urwid.Padding(urwid.ListBox(temp()), left=2, right=2)
top = urwid.Overlay(
    main,
    urwid.SolidFill("\N{MEDIUM SHADE}"),  # bottom widget
    align="center",
    width=("relative", 80),
    valign="middle",
    height=("relative", 80),
    min_width=20,
    min_height=9,
)
urwid.MainLoop(top, palette=[("reversed", "standout", "")]).run()
