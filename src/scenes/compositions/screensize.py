from asciimatics.effects import Print

MIN_WIDTH = 100
MIN_HEIGHT = 30


def print_screen_size(source: Print):
    t1 = "Terminal too small!"
    t2 = f"Minimum: {MIN_WIDTH}x{MIN_HEIGHT}"
    t3 = f"Current: {source.screen.width}x{source.screen.height}"
    source.screen.print_at(t1, (source.screen.width - len(t1)) // 2, 1, 1, 4)
    source.screen.print_at(t2, (source.screen.width - len(t2)) // 2, 2, 1, 4)
    source.screen.print_at(t3, (source.screen.width - len(t3)) // 2, 3, 1, 4)
