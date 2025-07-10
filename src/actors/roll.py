import random

from src.const import DICE_MIN, DICE_MAX, DICE_SUCCESS


def roll(n: int) -> tuple[int, list[int]]:
    """Rolls n d6 and records a success on each 5 and each 6."""
    success = 0
    result = []
    for _ in range(0, n):
        dice = random.randint(DICE_MIN, DICE_MAX)
        result.append(dice)
        if dice in DICE_SUCCESS:
            success += 1
    return (success, result)
