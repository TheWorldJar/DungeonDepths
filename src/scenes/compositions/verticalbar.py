from asciimatics.effects import Print


def print_vertical_bar(source: Print, x: int, c="|"):
    y = 4
    while y < source.screen.height:
        source.screen.print_at(c, x, y, 7, 1)
        y += 1
