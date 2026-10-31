from collections import deque


def ft_solver(grid: list[list[int]], config_info: dict) -> str:
    entry: tuple[int, int] = config_info["ENTRY"]   # (col, row)  ->  (x, y)
    exit:  tuple[int, int] = config_info["EXIT"]

    if entry == exit:
        return ""

    moves = [
        (0, -1, "N", 1),
        (1,  0, "E", 2),
        (0,  1, "S", 4),
        (-1,  0, "W", 8),
    ]

    width:  int = config_info["WIDTH"]
    height: int = config_info["HEIGHT"]

    queue: deque = deque()
    queue.append((entry[0], entry[1], ""))
    visited: set[tuple[int, int]] = {entry}

    while queue:
        x, y, path = queue.popleft()

        for dx, dy, char, wall_bit in moves:
            nx, ny = x + dx, y + dy

            if not (0 <= nx < width and 0 <= ny < height):
                continue

            if grid[y][x] & wall_bit:
                continue

            if (nx, ny) in visited:
                continue

            new_path: str = path + char

            if (nx, ny) == exit:
                return new_path

            visited.add((nx, ny))
            queue.append((nx, ny, new_path))

    return ""
