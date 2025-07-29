## Build/Lint/Test

*   **Run:** `source venv/bin/activate && export PYTHONPATH=$(pwd) && python3 src/main.py`
*   **Test:** `pytest` (No tests found, but this is the standard)
*   **Lint:** `pylint src` or `flake8 src`

## Code Style

*   **Imports:** Grouped as standard library, third-party, and then source imports.
*   **Formatting:** Follows PEP 8. Use `black` or `autopep8` for auto-formatting.
*   **Types:** Use type hints for function signatures.
*   **Naming:**
    *   Classes: `PascalCase` (e.g., `GameState`)
    *   Functions/Methods/Variables: `snake_case` (e.g., `save_to_json`)
    *   Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_CHARACTER_SLOT`)
    *   Private members are prefixed with an underscore (e.g., `_current_scene`).
*   **Error Handling:** Use `try...except` blocks for operations that can fail, like screen resizing.
*   **Docstrings:** Use docstrings to explain the purpose of modules, classes, and functions.
