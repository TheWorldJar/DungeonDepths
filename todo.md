# TODO

- Implement dungeon sub screen.
  - Implement time tracking.
  - Implement turn handling.
  - Implement turn progression.
- Implement basic enemy.
- Implement combat class.
- Run a combat.
- Finish implementing ability functions for all classes.
- Implement the rat amulet effect

## Priority Modifiers

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
  - vice versa on healing.
- If it targets last:
  - x0 if last is friendly.
  - +2 if last is enemy.
  - vice versa on healing.
- If it heals self:
  - +1 if self is Hurt.
  - +2 if self is Bloodied.
- If it's a buff:
  - x0 if target already has the buff.
  - +1 per ally without the buff.
  - -1 per ally with the buff.
