# TODO

- Implement the seven other classes to the save system.
- Change const PALETTE to improve display for popups and other layouts.
- Remove state tracking from the play scene and migrate over to the game state.
- Put scene names into const file for better tracking across modules.
- In the Play Scene, change the header text to the selected character's name.
- Make an Enum for the Actor Types.
- Refactor the Charcter & Actor classes to user getters and setters.
-Finish implementing ability functions for all classes.

## Priority Modifers

- If it targets low:
    - +1 per Bloodied target.
    - +0.1 per Hurt target.
- If it targets high:
    - +2 per Full target.
    - +1 per Healthy target.
    - +0.1 per Hurt target.
- If it targets all:
    - +1 per target.
- If it targets n:
    - x0 if less than n target.
    - +2 if n or more targets.
- If it targets first:
    - x0 if first is friendly.
    - +2 if first is enemy.
    - vice-versa on healing.
- If it targets last:
    - x0 if last is friendly.
    - +2 if last is enemy.
    - vice-versa on healing.
- If it heals self:
    - +1 if self i Hurt.
    - +2 if self is Bloodied.
- If it's a buff:
    - x0 if target already has the buff.
    - +1 per ally without the buff.
    - -1 per ally with the buff.