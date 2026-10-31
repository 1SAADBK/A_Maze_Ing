import sys
from typing import Any


def parsing() -> dict[str, Any]:
    args = sys.argv
    if len(args) != 2 or (args[0] != "a_maze_ing.py"):
        print("Usage: python3 a_maze_ing.py config.txt")
        quit()
    dct: dict[str, Any] = {}
    lines = []
    used_files = [
        "a_maze_ing.py",
        ".gitignore",
        "ft_display.py",
        "ft_parser.py",
        "Makefile",
        "mazegen.py",
        "output_writer.py",
        "solver.py"
    ]
    try:
        with open(args[1], "r") as config:
            for line in config:
                if line.count("=") == 1:
                    lines.append(line.rstrip("\n"))
                else:
                    if line[0] != "#" and line[0] != "\n":
                        raise Exception(
                            f"Invalid line syntax {line}"
                            " <valid syntax : key=value>"
                        )
            for line in lines:
                key = line.split("=")[0].strip().upper()
                value = line.split("=")[1].strip()
                if key == "HEIGHT":
                    dct["HEIGHT"] = int(value)
                elif key == "WIDTH":
                    dct["WIDTH"] = int(value)
                elif key == "ENTRY":
                    if len(value.split(",")) == 2:
                        parts = value.split(",")
                        entry_coords: tuple[int, int] = (
                            int(parts[0]), int(parts[1])
                        )
                        if entry_coords[0] < 0 or entry_coords[1] < 0:
                            raise Exception(
                                "entry coordinates can't have"
                                " a negative number"
                            )
                        dct["ENTRY"] = entry_coords
                    else:
                        print(
                            "Invalid ENTRY "
                            "(syntax need to be like this ENTRY=a,b)"
                        )
                        quit()
                elif key == "EXIT":
                    if len(value.split(",")) == 2:
                        parts = value.split(",")
                        exit_coords: tuple[int, int] = (
                            int(parts[0]), int(parts[1])
                        )
                        if exit_coords[0] < 0 or exit_coords[1] < 0:
                            raise Exception(
                                "exit coordinates can't have"
                                " a negative number"
                            )
                        dct["EXIT"] = exit_coords
                    else:
                        print(
                            "Invalid EXIT "
                            "(syntax need to be like this EXIT=a,b)"
                        )
                        quit()
                elif key == "OUTPUT_FILE":
                    if value in used_files:
                        print(f"{value} already used")
                        quit()
                    dct["OUTPUT_FILE"] = value
                elif key == "PERFECT":
                    dct["PERFECT"] = value.upper()
                elif key == "SEED":
                    dct["SEED"] = int(value)
            check_list = [
                "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"
            ]
            missing = False
            for item in check_list:
                if item not in dct:
                    print(f"can't find {item} in the config file")
                    missing = True
            if missing:
                quit()
            if dct["ENTRY"] == dct["EXIT"]:
                print("The entry and exit can't be the same block")
                quit()
            if dct["PERFECT"] != "TRUE" and dct["PERFECT"] != "FALSE":
                print(
                    "PERFECT parameter can only be"
                    " True or False (case insensitive)"
                )
                quit()
            if dct["PERFECT"] == "TRUE":
                dct["PERFECT"] = True
            if dct["PERFECT"] == "FALSE":
                dct["PERFECT"] = False
    except Exception as e:
        print(f"ERROR : {e}")
        quit()
    return dct
