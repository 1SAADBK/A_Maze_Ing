def turn_solve_into_cord(solve: str, entry: tuple[int, int],
                         exit: tuple[int, int]) -> list[tuple[int, int]]:
    cord: list[tuple[int, int]] = [entry]
    for i in range(len(solve)):
        last = cord[len(cord) - 1]
        if solve[i] == "N":
            cord.append((last[0], last[1] - 1))
        elif solve[i] == "E":
            cord.append((last[0] + 1, last[1]))
        elif solve[i] == "S":
            cord.append((last[0], last[1] + 1))
        elif solve[i] == "W":
            cord.append((last[0] - 1, last[1]))
    return cord


def display(grid: list[list[int]], solve: str, config_info: dict,
            show_solve: bool = False, color: str = "\033[47m") -> None:
    width: int = config_info["WIDTH"]
    height: int = config_info["HEIGHT"]
    entry: tuple = config_info["ENTRY"]
    exit: tuple = config_info["EXIT"]
    solve_cord = turn_solve_into_cord(solve, entry, exit)
    RESET = "\033[0m"
    WALL = f"{color}  {RESET}"
    ENTRY_CELL = "🟩"
    EXIT_CELL = "🟥"
    pattern_CELL = "🟦"
    OPEN_WALL = "  "
    CELL = "  "
    CORD_CELL = f"\033[48;5;208m  {RESET}"
    if height <= 5 or width <= 7:
        print("The maze is too small, can't show the pattern")
    for i in range(height):
        top = WALL
        for j in range(width):
            if grid[i][j] & 1:
                top += WALL + WALL
            else:
                top += OPEN_WALL + WALL
        print(top)
        middle = WALL
        for j in range(width):
            if entry == (j, i):
                C = ENTRY_CELL
            elif exit == (j, i):
                C = EXIT_CELL
            elif grid[i][j] == 15:
                C = pattern_CELL
            else:
                if (j, i) in solve_cord and show_solve:
                    C = CORD_CELL
                else:
                    C = CELL
            if grid[i][j] & 2:
                middle += C + WALL
            else:
                middle += C + OPEN_WALL
        print(middle)
    bottom = WALL
    for j in range(width):
        bottom += WALL
        bottom += WALL
    print(bottom)
