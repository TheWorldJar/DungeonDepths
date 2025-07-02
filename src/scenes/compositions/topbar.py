from asciimatics.effects import Print


def print_top_bar(source: Print, content: str):
    bar_edge = "=" * (source.screen.width - 2)
    bar_side = "= + ="
    bar_content = content
    source.screen.print_at(bar_edge, 1, 1, 7, 1)
    source.screen.paint(
        text=bar_side,
        x=1,
        y=2,
        colour_map=[(7, 1, 0), (0, 1, 0), (3, 1, 0), (0, 1, 0), (7, 1, 0)],
    )
    source.screen.print_at(
        bar_content, (source.screen.width - len(bar_content)) // 2, 2, 1, 4
    )
    source.screen.paint(
        text=bar_side,
        x=source.screen.width - 1 - len(bar_side),
        y=2,
        colour_map=[(7, 1, 0), (0, 1, 0), (3, 1, 0), (0, 1, 0), (7, 1, 0)],
    )
    source.screen.print_at(bar_edge, 1, 3, 7, 1)
