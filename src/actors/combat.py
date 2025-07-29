from src.actors.actor import Actor
from src.actors.characters.character import Character
from src.actors.monsters.monster import Monster
from src.actors.puzzles.puzzle import Puzzle
from src.actors.roll import roll_sum
from src.game import GameState
from src.game_types import ActorType


class Combat:
    def __init__(
        self,
        characters: list[Character],
        enemies: list[Monster | Puzzle],
        game_state: GameState,
    ):
        self._characters = characters
        self._enemies = enemies
        self._game = game_state
        self._round_numer = 0
        self._timeline: list[tuple[Actor, int]] = []

        # Roll Initiative
        # Build List Ordered on Initiative

    def _prepare_timeline(self):
        self._game.debug_log("Preparing timeline")
        for c in self.get_all_characters():
            roll = roll_sum(c.get_initiative_roll())
            c.set_initiative(roll[0] + c.get_initiative_mod())
            for i in c.get_initiative():
                self._timeline.append((c, i))

        for e in self.get_all_enemies():
            roll = roll_sum(e.get_initiative_roll())
            e.set_initiative(roll[0] + e.get_initiative_mod())
            for i in e.get_initiative():
                self._timeline.append((e, i))

        self._timeline.sort(key=lambda t: (-t[1], t[0].get_name()))
        self._game.debug_log(f"Prepared timeline: {self._timeline}")

    def _new_round(self):
        self._game.debug_log(f"New round: {self._round_numer + 1}")
        self._round_numer += 1
        self._prepare_timeline()

    def _on_actor_defeat(self, actor: Actor):
        for i, a in enumerate(self._timeline):
            if a[0] == actor.get_name():
                self._timeline.pop(i)
                i -= 1

        if actor.get_actor_type() == ActorType.CHARACTER:
            for i, c in enumerate(self._characters):
                if c.get_name() == actor.get_name():
                    self._characters.pop(i)
                    break
        else:
            for i, e in enumerate(self._enemies):
                if e.get_name() == actor.get_name():
                    self._enemies.pop(i)
                    break

    def _check_victory(self) -> int:
        """Check for Victory at the end of a Turn"""
        victory = 0
        if len(self.get_all_characters()) == 0:
            victory = -1
        elif len(self.get_all_enemies()) == 0 and len(self.get_all_characters()) > 0:
            victory = 1
        return victory

    # Nothing but Getters and Setters below.
    def get_characters(self, slot) -> Character:
        return self._characters[slot]

    def get_all_characters(self) -> list[Character]:
        return self._characters

    def set_character(self, character: Character, slot=-1):
        if slot < 0 or slot > len(self._characters):
            self._characters.append(character)
        else:
            self._characters[slot] = character

    def set_all_characters(self, characters: list[Character]):
        self._characters = characters

    def get_enemy(self, slot) -> Monster | Puzzle:
        return self._enemies[slot]

    def get_all_enemies(self) -> list[Monster | Puzzle]:
        return self._enemies

    def set_enemy(self, enemy: Monster | Puzzle, slot=-1):
        if slot < 0 or slot > len(self._enemies):
            self._enemies.append(enemy)
        else:
            self._enemies[slot] = enemy

    def set_all_enemies(self, enemies: list[Monster | Puzzle]):
        self._enemies = enemies
