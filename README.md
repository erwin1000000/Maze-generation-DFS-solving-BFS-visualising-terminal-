*This project has been created as part of the 42 curriculum by Younes Abyaa and Mohammed Mokhliss.*

## Description
**A-Maze-ing** is a Python software suite designed for the generation, visualization, and automated solving of complex mazes. The project's primary objective is to develop a robust maze engine while strictly adhering to modern PEP 621 Python packaging standards. The application features an interactive terminal interface to generate mazes, visualize paths, customize themes, and export the output. It also functions as a standalone, reusable Python module (`mazegen`) that can be installed seamlessly via `pip`.

---

## Instructions

### Prerequisites
* **Operating System:** Linux Ubuntu
* **Python:** Version 3.10 or higher
* **Package Manager:** Poetry

### Installation
To set up the isolated virtual environment and install development dependencies (Mypy, Flake8):
```bash
make install
```

### Execution
To run the interactive maze generator using the provided configuration file:
```bash
make run
```
Note: This executes `poetry run python3 a_maze_ing.py config.txt` under the hood.

### Compilation & Packaging
To compile the standalone module into a distributable Wheel (.whl) format:
```bash
poetry build
```
This command generates the build artifacts inside the `dist/` directory.

---

## Resources

### External References & Documentation:
- **Maze Algorithms:** [Wikipedia - Randomized Depth-First Search](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- **Solving Algorithms:** [Wikipedia - Breadth-First Search (BFS)](https://en.wikipedia.org/wiki/Breadth-first_search)
- **Packaging:** [PEP 621 – Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- **Environment:** [Poetry Official Documentation](https://python-poetry.org/docs/)
- **Video Tutorials:** [YouTube](https://www.youtube.com)

### AI Usage Statement:
Artificial Intelligence was occasionally used during this project as a learning aid — specifically to quickly clarify concepts, ask targeted questions, or better understand documentation when written resources were unclear.

No AI was used for writing, generating, or debugging any part of the actual code, packaging configuration, or architectural decisions. All implementation was done manually by the team.

---

## Configuration File Description
The project is driven by a configuration file (e.g., `config.txt`) strictly formatted as `KEY=Value`. The parser validates the following parameters:

- **WIDTH:** (Integer) The total width of the maze grid.
- **HEIGHT:** (Integer) The total height of the maze grid.
- **ENTRY:** (Coordinates) The starting point of the maze, formatted exactly as `x,y`.
- **EXIT:** (Coordinates) The destination point of the maze, formatted exactly as `x,y`.
- **OUTPUT_FILE:** (String) The name/path of the file where the final maze data will be saved (e.g., `maze.txt`).
- **PERFECT:** (Boolean) Accepts `True` (creates a perfect maze with no loops) or `False` (creates an imperfect maze with multiple paths/loops).
- **SEED:** (Integer, Optional) A seed value for the random number generator to ensure reproducible mazes.

---

## The Chosen Maze Algorithm
- **Generation:** Randomized Depth-First Search (DFS)
- **Solver:** Breadth-First Search (BFS)

### The Reason for Choosing This Algorithm
**DFS for Generation:** We chose Randomized DFS because it is highly memory-efficient and naturally produces "perfect" mazes characterized by deep, winding corridors and long dead ends. This provides a high degree of visual complexity and difficulty, fulfilling the project's aesthetic goals.

**BFS for Solving:** We chose BFS for the solver because it structurally guarantees finding the shortest possible path. This is critically important when solving "imperfect" mazes (`PERFECT=False`), which contain loops and multiple valid routes to the exit.

---

## Reusable Module Documentation (`mazegen`)
The `mazegen` package is a standalone, reusable Python module designed to be imported into other applications without relying on the command-line interface.

### Core Components:
- **Grid Class:** Manages the internal 2D array representation of the maze. It handles coordinate mapping, embedding the mandatory 42 logo, and provides ANSI-colored terminal rendering via the `print_maze` method.
- **MazeGenerator Class:** Encapsulates the algorithmic engine. It takes a grid state and features methods for generation (`dfs`), loop introduction (`make_imperfect`), and shortest-path calculation (`bfs_solver`).

---

## Team and Project Management

### The roles of each team member
- **Younes Abyaa:** Lead algorithmic development (DFS/BFS logic), PEP 621 packaging implementation via Poetry, and Makefile automation.
- **Mohammed Mokhliss:** Configuration file parsing logic, interactive terminal UI rendering, ANSI color formatting, and extensive edge-case testing.

### Anticipated planning and how it evolved
Our initial plan was to strictly finish the maze generation and solving algorithms first, and only tackle the Python packaging requirements at the very end. However, this evolved quickly; we realized that waiting to set up Poetry and `pyproject.toml` could cause dependency and import issues late in development. We pivoted to setting up the package infrastructure on day one, allowing us to test the code natively inside its virtual environment throughout the entire build process.

### What worked well and what could be improved
**What worked well:** Dividing the logic strictly between the "Engine" (`mazegen.py`) and the "Interface" (`a_maze_ing.py`). This separation of concerns made debugging much easier and naturally fulfilled the standalone module requirement.

**What could be improved:** Time estimation for modern Python packaging. Transitioning from traditional `requirements.txt`/`setup.py` to Poetry and PEP 621 took more research time than anticipated. We could have allocated more time to studying the documentation before attempting to build the wheel.

### Specific tools used
- **Git:** For version control and collaborative branching.
- **Poetry:** For strict dependency locking (`poetry.lock`) and virtual environment management.
- **Mypy:** For rigorous static type checking to ensure code safety.
- **Flake8:** For PEP 8 linting and style enforcement.
- **Make:** To wrap complex Poetry and Python commands into standardized execution targets.
