import random


def roll(n: int) -> tuple[int, list[int]]:
    success = 0
    result = []
    for i in range(0, n):
        dice = random.randint(1, 6)
        result.append(dice)
        if dice == 5 or dice == 6:
            success += 1
    return (success, result)
