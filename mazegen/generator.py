import random


class MazeGenerator():
    """
    Reusable Module — `mazegen`
    ===========================
    The maze generation logic is isolated in a standalone,
    pip-installable package
    located at the root of the repository.

    Installation
    ------------
        pip install mazegen_samo-1.0.0.tar.gz

    Usage Example
    -------------
        from mazegen import MazeGenerator

        # Instantiate with custom parameters
        gen = MazeGenerator(config_info: dict)

        # Generate the maze
        gen.generate()

        # Access the maze grid (2D list of cell wall bitmasks)
        grid = gen.algo_perfect()  # grid[row][col] -> int (hex digit)

    Parameters
    ----------
    width : int, default=20
        Number of columns.
    height : int, default=15
        Number of rows.
    seed : int, default=None
        RNG seed for reproducible output.
    perfect : bool, default=True
        Enforce a single path (perfect maze).

    Notes
    -----
    The internal `grid` structure stores wall data per cell.
    This is not necessarily the same as the hexadecimal output file format.
    """
    def __init__(self, config_info: dict) -> None:
        self.width: int = config_info["WIDTH"]
        self.height: int = config_info["HEIGHT"]
        self.entry: tuple = config_info["ENTRY"]
        self.exit: tuple = config_info["EXIT"]
        self.perfect: bool = config_info["PERFECT"]
        if "SEED" in config_info:
            self.seed_usage = True
            self.seed: int = config_info["SEED"]
        else:
            self.seed_usage = False
        self.grid: list[list[int]] = [
            [15 for _ in range(self.width)] for _ in range(self.height)
        ]
        self.gridinfo: list[list[int]] = [
            [0 for _ in range(self.width)] for _ in range(self.height)
        ]

    def inject_logo(self, gridinfo: list[list[int]]) -> list[list[int]]:
        entry = ((self.width - 7) // 2, (self.height - 5) // 2)
        self.gridinfo[entry[1]][entry[0]] = 2
        self.gridinfo[entry[1] + 1][entry[0]] = 2
        self.gridinfo[entry[1] + 2][entry[0]] = 2
        self.gridinfo[entry[1] + 2][entry[0] + 1] = 2
        self.gridinfo[entry[1] + 2][entry[0] + 2] = 2
        self.gridinfo[entry[1] + 3][entry[0] + 2] = 2
        self.gridinfo[entry[1] + 4][entry[0] + 2] = 2
        self.gridinfo[entry[1]][entry[0] + 4] = 2
        self.gridinfo[entry[1]][entry[0] + 5] = 2
        self.gridinfo[entry[1]][entry[0] + 6] = 2
        self.gridinfo[entry[1] + 1][entry[0] + 6] = 2
        self.gridinfo[entry[1] + 2][entry[0] + 6] = 2
        self.gridinfo[entry[1] + 2][entry[0] + 5] = 2
        self.gridinfo[entry[1] + 2][entry[0] + 4] = 2
        self.gridinfo[entry[1] + 3][entry[0] + 4] = 2
        self.gridinfo[entry[1] + 4][entry[0] + 4] = 2
        self.gridinfo[entry[1] + 4][entry[0] + 5] = 2
        self.gridinfo[entry[1] + 4][entry[0] + 6] = 2
        return self.gridinfo

    @staticmethod
    def not_valid_entry_exit(entry: tuple[int, int],
                             exit: tuple[int, int],
                             grid: list[list[int]]
                             ) -> bool:
        if grid[entry[1]][entry[0]] == 2:
            return True
        if grid[exit[1]][exit[0]] == 2:
            return True
        return False

    def algo_perfect(self) -> list[list[int]]:
        ccell = self.entry
        self.gridinfo[self.entry[1]][self.entry[0]] = 1
        if self.height > 5 and self.width > 7:
            self.gridinfo = self.inject_logo(self.gridinfo)
        if self.not_valid_entry_exit(self.entry, self.exit, self.gridinfo):
            raise Exception("ERROR : Exit or entry cell inside the logo.")
        if self.seed_usage:
            random.seed(self.seed)
        while True:
            ne = []
            x, y = ccell[0], ccell[1]
            if y > 0 and self.gridinfo[y - 1][x] == 0:
                ne.append((x, y - 1, 'N'))
            if x < self.width - 1 and self.gridinfo[y][x + 1] == 0:
                ne.append((x + 1, y, 'E'))
            if y < self.height - 1 and self.gridinfo[y + 1][x] == 0:
                ne.append((x, y + 1, 'S'))
            if x > 0 and self.gridinfo[y][x - 1] == 0:
                ne.append((x - 1, y, 'W'))
            if ne:
                next = random.choice(ne)
                if next[2] == 'N':
                    self.grid[ccell[1]][ccell[0]] -= 1
                    self.grid[ccell[1] - 1][ccell[0]] -= 4
                elif next[2] == 'E':
                    self.grid[ccell[1]][ccell[0]] -= 2
                    self.grid[ccell[1]][ccell[0] + 1] -= 8
                elif next[2] == 'S':
                    self.grid[ccell[1]][ccell[0]] -= 4
                    self.grid[ccell[1] + 1][ccell[0]] -= 1
                else:
                    self.grid[ccell[1]][ccell[0]] -= 8
                    self.grid[ccell[1]][ccell[0] - 1] -= 2
                ccell = (next[0], next[1])
                self.gridinfo[next[1]][next[0]] = 1
            else:
                found = False
                for j in range(self.height):
                    for i in range(self.width):
                        if self.gridinfo[j][i] == 1:
                            has_ne = ((i > 0
                                       and self.gridinfo[j][i - 1] == 0) or
                                      (i < self.width - 1
                                       and self.gridinfo[j][i + 1] == 0) or
                                      (j > 0
                                       and self.gridinfo[j - 1][i] == 0) or
                                      (j < self.height - 1
                                       and self.gridinfo[j + 1][i] == 0)
                                      )
                            if has_ne:
                                found = True
                                ccell = (i, j)
                                break
                    if found:
                        break
                if not found:
                    break
        return self.grid

    def make_not_perfect(self) -> list[list[int]]:
        self.algo_perfect()
        walls_to_break = self.height * self.width * 4 // 60
        broken = 0
        while broken < walls_to_break:
            not_applicable = True
            while not_applicable:
                x = random.choice([i for i in range(self.width)])
                y = random.choice([i for i in range(self.height)])
                if self.gridinfo[y][x] == 2:
                    break
                if (
                    y > 0
                    and self.grid[y][x] & 1
                    and self.gridinfo[y - 1][x] != 2
                ):
                    self.grid[y][x] -= 1
                    self.grid[y - 1][x] -= 4
                    not_applicable = False
                elif (
                    y < self.height - 1
                    and self.grid[y][x] & 4
                    and self.gridinfo[y + 1][x] != 2
                ):
                    self.grid[y][x] -= 4
                    self.grid[y + 1][x] -= 1
                    not_applicable = False
                elif (
                    x > 0
                    and self.grid[y][x] & 8
                    and self.gridinfo[y][x - 1] != 2
                ):
                    self.grid[y][x] -= 8
                    self.grid[y][x - 1] -= 2
                    not_applicable = False
                elif (
                    x < self.width - 1
                    and self.grid[y][x] & 2
                    and self.gridinfo[y][x + 1] != 2
                ):
                    self.grid[y][x] -= 2
                    self.grid[y][x + 1] -= 8
                    not_applicable = False
                if not not_applicable:
                    broken += 1
                else:
                    break
        return self.grid
