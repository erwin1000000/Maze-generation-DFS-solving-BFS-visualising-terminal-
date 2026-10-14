import sys
from typing import List, Tuple, Dict, Any
from file_pars import parse_config
from mazegen import Grid, MazeGenerator


def output_file(
    maze_array: List[List[int]],
    solution: List[Tuple[int, int]],
    height: int,
    width: int,
    the_entry: Tuple[int, int],
    the_exit: Tuple[int, int],
    file_name: str
) -> None:
    """Writes the maze structure and solution path to a file."""
    with open(file_name, 'w') as output:
        for y in range(height):
            for x in range(width):
                cell = maze_array[y][x]
                if cell >= 100:
                    output.write("F")
                else:
                    cell = cell & 15
                    output.write(f"{cell:X}")
            output.write("\n")
        output.write("\n")
        output.write(f"{the_entry[1]},{the_entry[0]}\n")
        output.write(f"{the_exit[1]},{the_exit[0]}\n")
        i = 0
        while i < len(solution) - 1:
            y, x = solution[i]
            y2, x2 = solution[i + 1]
            if y == y2 and x > x2:
                output.write("W")
            elif y == y2 and x < x2:
                output.write("E")
            elif y > y2 and x == x2:
                output.write("N")
            elif y < y2 and x == x2:
                output.write("S")
            i += 1
        output.write("\n")


def generate_new_maze(
        config: Dict[str, Any]) -> Tuple[Grid, List[Tuple[int, int]], bool]:
    """Helper function to build a fresh maze based on config."""
    grid = Grid(config["HEIGHT"], config["WIDTH"],
                (config["ENTRY_Y"], config["ENTRY_X"]),
                (config["EXIT_Y"], config["EXIT_X"]))
    flag = grid.make_42()
    grid.make_entry_exit()
    engine = MazeGenerator(
            grid.grid,
            grid.height,
            grid.width,
            grid.exit,
            config.get("SEED"))
    engine.dfs(config["ENTRY_Y"], config["ENTRY_X"])
    if not config["PERFECT"]:
        engine.make_imperfect()
    solution = engine.bfs_solver(config["ENTRY_Y"], config["ENTRY_X"])
    return grid, solution, flag


def main() -> None:
    """Main entry point for the interactive maze terminal."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    try:
        config = parse_config(sys.argv[1])
        grid, solution, flag = generate_new_maze(config)
        output_file(grid.grid, solution, grid.height, grid.width,
                    grid.entry, grid.exit, config["OUTPUT_FILE"])

        path_visible = False
        wall_colors = [
                "\033[0m",
                "\033[31m",
                "\033[32m",
                "\033[33m",
                "\033[34m",
                "\033[35m"]
        path_colors = [
                "\033[36m",
                "\033[35m",
                "\033[33m",
                "\033[32m",
                "\033[31m",
                "\033[0m"]
        logo_colors = [
                "\033[90m",
                "\033[37m",
                "\033[34m",
                "\033[35m",
                "\033[32m",
                "\033[36m"]
        color_idx = 0

        while True:
            print("\033[H\033[J", end="")
            w_c = wall_colors[color_idx]
            p_c = path_colors[color_idx]
            l_c = logo_colors[color_idx]

            maze_render = grid.print_maze(w_c, p_c, l_c)
            for line in maze_render:
                print(line, end="")
            if not flag:
                print("maze is too small for 42 logo")

            print("\n=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path")
            print("3. Change maze wall colors")
            print("4. Quit")

            choice = input("Choice? (1-4): ")

            if choice == '1':
                grid, solution, flag = generate_new_maze(config)
                output_file(grid.grid, solution, grid.height, grid.width,
                            grid.entry, grid.exit, config["OUTPUT_FILE"])
                if path_visible:
                    grid.make_solution(solution)
            elif choice == '2':
                if path_visible:
                    grid.remove_solution(solution)
                    path_visible = False
                else:
                    grid.make_solution(solution)
                    path_visible = True
            elif choice == '3':
                color_idx += 1
                if color_idx == 5:
                    color_idx = 0
            elif choice == '4':
                print("Maze saved. Goodbye!")
                break
            else:
                input("Invalid choice. Press Enter to try again...")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
