from ft_display import display
from ft_parser import parsing
from solver import ft_solver
from mazegen import MazeGenerator
from output_writer import ft_output_writer
from typing import Any
import random
import os


def menu(
    grid: list[list[int]],
    solve: str,
    config_info: dict[str, Any] = {},
    color: str = "\033[47m",
    show_solve: bool = False,
) -> None:
    colors = [
        "\033[41m",
        "\033[42m",
        "\033[43m",
        "\033[44m",
        "\033[45m",
        "\033[46m",
        "\033[47m",
    ]
    print("=== A-Maze-ing ===")
    print("1. Re-generate a new maze")
    print("2. Show/Hide path from entry to exit")
    print("3. Rotate maze colors")
    print("4. Quit")
    try:
        choice = int(input("Choice? (1-4): "))
        if choice == 1:
            main(color)
        elif choice == 2:
            os.system("clear")
            show_solve = not show_solve
            display(
                grid, solve, config_info,
                show_solve=show_solve, color=color
            )
            menu(grid, solve, config_info, color, show_solve)
        elif choice == 3:
            os.system("clear")
            color = random.choice(colors)
            display(grid, solve, config_info, show_solve, color=color)
            menu(grid, solve, config_info, color, show_solve)
        elif choice == 4:
            os.system("clear")
            quit()
        else:
            os.system("clear")
            print("Invalid input")
            menu(grid, solve, config_info, color, show_solve)
    except (Exception, KeyboardInterrupt):
        os.system("clear")
        print("Invalid input")
        menu(grid, solve, config_info, color, show_solve)


def main(color: str = "\033[47m") -> None:
    try:
        config_info: dict[str, Any] = parsing()
        entry = config_info["ENTRY"]
        exit_ = config_info["EXIT"]
        if (entry[0] >= config_info["WIDTH"]
                or entry[1] >= config_info["HEIGHT"]):
            raise Exception("entry coordinates out of maze range")
        if (exit_[0] >= config_info["WIDTH"]
                or exit_[1] >= config_info["HEIGHT"]):
            raise Exception("exit coordinates out of maze range")
        mazegen = MazeGenerator(config_info)
        if config_info["PERFECT"] is True:
            grid = mazegen.algo_perfect()
        else:
            grid = mazegen.make_not_perfect()
        solve = ft_solver(grid, config_info)
        ft_output_writer(grid, solve, config_info)
        os.system("clear")
        display(grid, solve, config_info, False, color=color)
        menu(grid, solve, config_info, color)
    except (Exception, KeyboardInterrupt, OSError) as e:
        print(e)
        quit()


if __name__ == "__main__":
    try:
        main()
    except (Exception, KeyboardInterrupt, OSError) as e:
        print(e)
        quit()
