def ft_output_writer(grid: list[list[int]],
                     solve: str, config_info: dict) -> None:
    output: str = config_info["OUTPUT_FILE"]
    with open(output, 'w') as f:
        width: int = config_info["WIDTH"]
        height: int = config_info["HEIGHT"]
        entry: tuple = config_info["ENTRY"]
        exit: tuple = config_info["EXIT"]
        hexa = "0123456789ABCDEF"
        for i in range(height):
            line = ""
            for j in range(width):
                line += hexa[grid[i][j]]
            line += "\n"
            f.write(line)
        f.write(f"\n{entry[0]},{entry[1]}\n{exit[0]},{exit[1]}\n{solve}")
