# TODO

- Implement ability sets for the seven other classes.
- Finish a full character creation.
    1. Implement the Ability and Status classes.
        1. Each ability needs to be able to change its own priority based on specific conditions from the other actors in the combat. (e.g.: Low enemies increase the priority of skills that target low).
            - The combat calls all of the active character's abilies' modify_priority function.
            - The combat calls that character's choose ability function.
            - The character calls the chose ability's execute function.
            - The ability resolves.
            - The combat resets that character's priorities to 1.
        2. Each ability needs to receive a priority malus if it was used on the last turn. (e.g.: 0.5x)
            - The character object can track that.
        3. Then, an ability is chosen with priority as a weight.
            - Rules defined below.
        4. Then, the ability targets it's prefered target, or finds one from the other actors in the combat.
- Implement the seven other classes to the save system.
- Change const PALETTE to improve display for popups and other layouts.
- Remove state tracking from the play scene and migrate over to the game state.
- Put scene names into const file for better tracking across modules.
- In the Play Scene, change the header text to the selected character's name.
- Make an Enum for the Actor Types.

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