from asciimatics.screen import Screen

DEBUG = True

# Screen Size Constrainsts
MIN_SCREEN_WIDTH = 100
MIN_SCREEN_HEIGHT = 30

# Save File
SAVE_PATH = "./save"
SAVE_FILE = SAVE_PATH + "/save.json"

# Dice Rolls
DICE_MIN = 1
DICE_MAX = 6
DICE_SUCCESS = (5, 6)

# Health States
FULL_HEALTH = 0.99
HEALTHY = 0.7
HURT = 0.3
BLOODIED = 0.01
DEAD = 0


# Characters
CHARACTER_BASE_HEALTH = 5
CHARACTER_HEALTH_MULTIPLIER = 5
MAX_CHARACTER_SLOT = 8
START_CHARACTER_SLOT = 2
ABILITY_SLOT = 4

# Marauder
MARAUDER_HEALTH_MULTIPLIER = 3
MARAUDER_BASE_REGEN = 1

# Effect Durations
NO_DURATION = float("inf")
END_DURATION = 0

# Colour Palette
PALETTE = {
    "background": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "shadow": (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "disabled": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "invalid": (Screen.COLOUR_RED, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "label": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "borders": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "scroll": (Screen.COLOUR_YELLOW, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "title": (Screen.COLOUR_RED, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "edit_text": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "readonly": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "focus_readonly": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "button": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "control": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "field": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "focus_button": (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_WHITE),
    "focus_control": (
        Screen.COLOUR_BLACK,
        Screen.A_NORMAL,
        Screen.COLOUR_WHITE,
    ),
    "focus_field": (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_WHITE),
    "focus_edit_text": (
        Screen.COLOUR_BLACK,
        Screen.A_NORMAL,
        Screen.COLOUR_WHITE,
    ),
    "focus_label": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "selected_field": (
        Screen.COLOUR_WHITE,
        Screen.A_REVERSE,
        Screen.COLOUR_BLACK,
    ),
    "selected_control": (
        Screen.COLOUR_WHITE,
        Screen.A_REVERSE,
        Screen.COLOUR_BLACK,
    ),
    "selected_button": (
        Screen.COLOUR_BLACK,
        Screen.A_NORMAL,
        Screen.COLOUR_WHITE,
    ),
    "selected_focus_field": (
        Screen.COLOUR_BLACK,
        Screen.A_NORMAL,
        Screen.COLOUR_YELLOW,
    ),
    "selected_focus_control": (
        Screen.COLOUR_BLACK,
        Screen.A_NORMAL,
        Screen.COLOUR_YELLOW,
    ),
    "selected_focus_button": (
        Screen.COLOUR_BLACK,
        Screen.A_NORMAL,
        Screen.COLOUR_WHITE,
    ),
}
