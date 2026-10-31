*This project has been created as part of the 42 curriculum by sbenkass, mosalhi.*

# A-Maze-ing 🌀

## Description

**A-Maze-ing** is a Python maze generator that creates random mazes from a user-defined configuration file. The program generates a maze of configurable dimensions, with custom entry and exit points, and optionally enforces a single unique solution path (perfect maze). The generated maze is saved to a file using a hexadecimal wall encoding and rendered visually in the terminal.

A key highlight of this project is the embedded **"42" pattern** — a shape drawn by fully-closed cells visible in the maze rendering — as a nod to the 42 school curriculum.

The maze generation logic is packaged as a reusable Python module (`mazegen`) that can be installed via `pip` and imported into any other project.

---

## Instructions

### Prerequisites

- Python 3.10 or later
- `pip` (or `uv`, `pipx`)

### Installation

Install all project dependencies:

```bash
make install
```

### Running the program

```bash
make run
```

Or directly:

```bash
python3 a_maze_ing.py config.txt
```

### Debug mode

Run the main script through Python's built-in debugger (`pdb`):

```bash
make debug
```

### Linting

```bash
make lint
```

This runs `flake8` and `mypy` with the following flags:
```
mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
```

### Cleaning

Remove temporary files and caches (`__pycache__`, `.mypy_cache`, etc.):

```bash
make clean
```

---

## Configuration File

The configuration file uses `KEY=VALUE` pairs, one per line. Lines starting with `#` are treated as comments and ignored.

A default `config.txt` is provided at the root of the repository.

### Mandatory keys

| Key           | Description                          | Example                  |
|---------------|--------------------------------------|--------------------------|
| `WIDTH`       | Maze width (number of cells)         | `WIDTH=20`               |
| `HEIGHT`      | Maze height (number of cells)        | `HEIGHT=15`              |
| `ENTRY`       | Entry coordinates (x,y)             | `ENTRY=0,0`              |
| `EXIT`        | Exit coordinates (x,y)              | `EXIT=19,14`             |
| `OUTPUT_FILE` | Output filename                      | `OUTPUT_FILE=maze.txt`   |
| `PERFECT`     | Whether the maze is perfect          | `PERFECT=True`           |

### Optional keys

| Key         | Description                                           | Example            |
|-------------|-------------------------------------------------------|--------------------|
| `SEED`      | Integer seed for reproducible generation              | `SEED=5000`        |
| `ALGORITHM` | Generation algorithm (`backtracker`, `prim`, etc.)    | `ALGORITHM=prim`   |

### Example config file

```ini
# A-Maze-ing configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=5000
```

---

## Output File Format

The maze is written row by row, one row per line, using one hexadecimal digit per cell. Each digit encodes the closed walls as bits:

| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1       | East  |
| 2       | South |
| 3       | West  |

A bit set to `1` means the wall is **closed**; `0` means **open**.

After the grid, a blank line separates three additional lines:
1. Entry coordinates
2. Exit coordinates
3. Shortest path from entry to exit using letters `N`, `E`, `S`, `W`

---

## Visual Representation

The maze is rendered in the terminal using ASCII/ANSI colour output. The visual shows:

- Maze walls (with configurable colours)
- Entry and exit cells
- The embedded **"42"** pattern (drawn by fully-closed cells)
- An optional shortest-path overlay

### Available interactions

From the interactive menu:

| Option | Action |
|--------|--------|
| `1`    | Re-generate a new maze |
| `2`    | Show / Hide the shortest path |
| `3`    | Rotate / change maze wall colours |
| `4`    | Quit |

---

## Maze Generation Algorithm

### Algorithm chosen: Recursive Backtracker (DFS)

The Recursive Backtracker (also known as the depth-first search algorithm) works by:

1. Starting from a random cell and marking it as visited.
2. Randomly choosing an unvisited neighbour, removing the wall between them, and recursing.
3. Backtracking when no unvisited neighbours remain, until all cells have been visited.

### Why this algorithm?

- It produces **perfect mazes** naturally — exactly one path exists between any two cells.
- It creates long, winding corridors with relatively few dead ends, making for satisfying visual mazes.
- It is straightforward to implement, easy to reason about, and maps cleanly to a grid-based cell structure.
- The algorithm is well-suited to seeded random generation, enabling reproducibility.

---

## Reusable Module — `mazegen`

The maze generation logic is isolated in a standalone, pip-installable package located at the root of the repository.

### Installation

```bash
pip install mazegen_samo-1.0.0.tar.gz
```

### Usage example

```python
from mazegen import MazeGenerator

# Instantiate with custom parameters
gen = MazeGenerator(config_info: dict)

# Generate the maze
gen.generate()

# Access the maze grid (2D list of cell wall bitmasks)
grid = gen.algo_perfect()  # grid[row][col] -> int (hex digit)
```

### Parameters

| Parameter | Type   | Default | Description                          |
|-----------|--------|---------|--------------------------------------|
| `width`   | `int`  | `20`    | Number of columns                    |
| `height`  | `int`  | `15`    | Number of rows                       |
| `seed`    | `int`  | `None`  | RNG seed for reproducible output     |
| `perfect` | `bool` | `True`  | Enforce a single path (perfect maze) |

> **Note:** The internal `grid` structure stores wall data per cell as integer bitmasks. This is not necessarily the same as the hexadecimal output file format.

---

## Maze Generation Algorithm

### Algorithm chosen: Iterative Random Walk with Frontier Restart

The algorithm is a custom iterative approach built around two parallel grids:

- **`grid`** — a 2D list of integers where each value encodes the closed walls of that cell as a bitmask (initialised to `15`, meaning all four walls closed).
- **`gridinfo`** — a 2D list of status flags: `0` = unvisited, `1` = visited, `2` = reserved (logo cell).

The generation proceeds as follows:

1. The entry cell is set as the current cell and marked as visited (`gridinfo = 1`).
2. The algorithm looks at the four cardinal neighbours (N, E, S, W) of the current cell and collects those that are still unvisited (`gridinfo == 0`).
3. If at least one unvisited neighbour exists, one is chosen at random. The shared wall between the current cell and the chosen neighbour is removed from both cells' bitmasks (keeping wall data coherent on both sides), and the neighbour becomes the new current cell, marked as visited.
4. If the current cell has no unvisited neighbours, the algorithm scans the entire grid row by row to find the first visited cell (`gridinfo == 1`) that still borders at least one unvisited cell, and jumps to it.
5. Steps 2–4 repeat until no visited cell has any remaining unvisited neighbour — meaning the whole maze has been carved.

For a **non-perfect maze**, the algorithm first runs the full perfect generation, then randomly selects a fixed number of internal walls and removes them, introducing extra paths and loops. Logo cells are never modified in this step.

### Why this algorithm?

- The dual-grid design keeps generation state simple and explicit — the `gridinfo` grid acts as a clear, flat visited map with no stack or recursion needed.
- The frontier-restart step ensures full connectivity without ever getting permanently stuck, guaranteeing every cell is reachable.
- It produces a **spanning tree** of the cell graph in perfect mode, ensuring exactly one path between any two cells.
- It maps naturally to the bitmask wall format, since wall removal is a direct arithmetic operation on both affected cells.
- The seeded `random` module makes any generated maze fully reproducible.

## Team & Project Management

### Team members

| Login      | Role |
|------------|------|
| `sbenkass` | Maze Generator, Parsing, display, testing|
| `mosalhi`  | linting, Path finder, packaging, testing|

### Planning 
we planned the project todo-list and and was working day by day until we started saying the maze appearance, we changed the plan along the way to be easy for both of us to finish the circle.
what could be improved: if we started earlier it would be better

### Tools used

- `flake8` for style enforcement
- `mypy` for static type checking
- `build` for packaging
- `pdb` for debugging

---

## Resources

### References

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [BFS shortest path — GeeksforGeeks](https://www.geeksforgeeks.org/shortest-path-unweighted-graph/)
- [Python Packaging User Guide](https://packaging.python.org/en/latest/)
- [PEP 257 – Docstring conventions](https://peps.python.org/pep-0257/)

### AI usage

AI  was used during this project for the following tasks:
Help debugging some errors.
learning about diffrent topics.
helping with the readme file.