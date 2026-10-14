from collections import deque
import random
from typing import List, Tuple, Union


class Grid:
    """Handles the creation, manipulation, and rendering of the maze grid."""

    def __init__(
        self,
        height: int,
        width: int,
        the_entry: Tuple[int, int],
        the_exit: Tuple[int, int]
    ) -> None:
        self.height = height
        self.width = width
        self.entry = the_entry
        self.exit = the_exit
        self.grid = [[15 for x in range(width)] for y in range(height)]

    def make_42(self) -> bool:
        """Attempts to embed the '42' logo into the center of the grid."""
        if self.width >= 9 and self.height >= 7:
            h = int(self.height / 2)
            w = int(self.width / 2)
            lst = [
                    (h, w - 1),
                    (h, w - 2),
                    (h, w - 3),
                    (h - 1, w - 3),
                    (h - 2, w - 3),
                    (h + 1, w - 1),
                    (h + 2, w - 1),
                    (h, w + 1),
                    (h, w + 2),
                    (h, w + 3),
                    (h + 1, w + 1),
                    (h + 2, w + 1),
                    (h + 2, w + 2),
                    (h + 2, w + 3),
                    (h - 1, w + 3),
                    (h - 2, w + 3),
                    (h - 2, w + 2),
                    (h - 2, w + 1)]
            entry_y = self.entry[0]
            entry_x = self.entry[1]
            exit_y = self.exit[0]
            exit_x = self.exit[1]
            for cor in lst:
                y = cor[0]
                x = cor[1]
                if (y == entry_y and x == entry_x)\
                        or (y == exit_y and x == exit_x):
                    raise ValueError("entry or exit is inside the 42 logo")

            for cor in lst:
                y = cor[0]
                x = cor[1]
                self.grid[y][x] = 100
            return True
        return False

    def make_entry_exit(self) -> None:
        """Marks the entry and exit points on the grid."""
        self.grid[self.entry[0]][self.entry[1]] += 16
        self.grid[self.exit[0]][self.exit[1]] += 16

    def make_solution(self, solution: List[Tuple[int, int]]) -> None:
        """Marks the solution path cells on the grid."""
        for y, x in solution[1:-1]:
            self.grid[y][x] += 16

    def remove_solution(self, solution: List[Tuple[int, int]]) -> None:
        """Removes solution path marks from the grid."""
        for y, x in solution[1:-1]:
            self.grid[y][x] -= 16

    def r_row(
        self,
        array: List[int],
        high: int,
        i: int,
        wall_color: str = "\033[0m",
        path_color: str = "\033[36m",
        logo_color: str = "\033[90m"
    ) -> List[str]:
        """Renders a single row of the maze with colors."""
        w = f"{wall_color}█\033[0m"
        p = f"{path_color}█\033[0m"
        lg = f"{logo_color}█\033[0m"
        row = []

        for j, v in enumerate(array):
            if v & 1 or v == 100:
                row.extend([w, w, w, w, w, w, w])
            elif v & 16 and self.grid[i - 1][j] & 16:
                row.extend([w, w, p, p, p, p, p])
            else:
                if (j > 0 and i > 0 and not self.grid[i][j - 1] & 1
                        and self.grid[i][j - 1] != 100
                        and not self.grid[i - 1][j - 1] & 2
                        and not self.grid[i][j - 1] & 2):
                    row.extend([" ", " ", " ", " ", " ", " ", " "])
                else:
                    row.extend([w, w, " ", " ", " ", " ", " "])
        row.extend([w, w, "\n"])

        for _ in range(2):
            for j, v in enumerate(array):
                if v & 8 or v == 100:
                    if v == 100:
                        row.extend([w, w, lg, lg, lg, lg, lg])
                    elif v & 16:
                        row.extend([w, w, p, p, p, p, p])
                    else:
                        row.extend([w, w, " ", " ", " ", " ", " "])
                else:
                    if v & 16:
                        if self.grid[i][j - 1] & 16:
                            row.extend([p, p, p, p, p, p, p])
                        else:
                            row.extend([" ", " ", p, p, p, p, p])
                    else:
                        row.extend([" ", " ", " ", " ", " ", " ", " "])
            row.extend([w, w, "\n"])

        if i == (high - 1):
            for v in array:
                if v & 4:
                    row.extend([w, w, w, w, w, w, w])
            row.extend([w, w, "\n"])
        return row

    def print_maze(
        self,
        wall_color: str = "\033[0m",
        path_color: str = "\033[36m",
        logo_color: str = "\033[90m"
    ) -> List[str]:
        """Generates the full visual representation of the maze."""
        visual = []
        for i, array in enumerate(self.grid):
            visual.extend(self.r_row(
                array, self.height, i, wall_color, path_color, logo_color
            ))
        return visual


class MazeGenerator:
    """Generates and solves the maze using DFS and BFS algorithms."""

    def __init__(
        self,
        grid_array: List[List[int]],
        height: int,
        width: int,
        exit_coord: Tuple[int, int],
        seed: Union[int, str, None] = None
    ) -> None:
        self.grid = grid_array
        self.height = height
        self.width = width
        self.exit = exit_coord
        self.rdm = random.Random(seed)

    def dfs(self, y: int, x: int) -> None:
        """Generates a perfect maze using Depth-First Search."""
        lst = []
        while 1:
            moves = [(-1, 0, 1), (0, 1, 2), (0, -1, 8), (1, 0, 4)]
            self.rdm.shuffle(moves)
            flag = True
            for move in moves:
                yy, xx, wall = move
                yyy, xxx = y + yy, x + xx
                if (0 <= xxx < self.width and 0 <= yyy < self.height
                        and (self.grid[yyy][xxx] == 15
                             or self.grid[yyy][xxx] == 31)):
                    self.grid[y][x] -= wall
                    if wall == 1:
                        self.grid[yyy][xxx] -= 4
                    elif wall == 2:
                        self.grid[yyy][xxx] -= 8
                    elif wall == 4:
                        self.grid[yyy][xxx] -= 1
                    elif wall == 8:
                        self.grid[yyy][xxx] -= 2
                    lst.append((y, x))
                    y, x = yyy, xxx
                    flag = False
                    break
            if flag:
                if lst:
                    y, x = lst.pop()
                else:
                    break

    def bfs_solver(self, y: int, x: int) -> List[Tuple[int, int]]:
        """Solves the maze using Breadth-First Search."""
        queue: deque[
                Tuple[
                    int,
                    int,
                    List[
                        Tuple[
                            int,
                            int]]]] = deque([(y, x, [])])
        visited = {(y, x)}
        while queue:
            cy, cx, solution = queue.popleft()
            if cy == self.exit[0] and cx == self.exit[1]:
                return solution + [(cy, cx)]
            neighbors = (
                (cy - 1, cx + 0, 1),
                (cy + 1, cx + 0, 4),
                (cy + 0, cx - 1, 8),
                (cy + 0, cx + 1, 2))
            for ny, nx, wall in neighbors:
                if 0 <= ny < self.height and 0 <= nx < self.width:
                    if not self.grid[cy][cx] & wall:
                        if (ny, nx) not in visited:
                            visited.add((ny, nx))
                            queue.append((ny, nx, solution + [(cy, cx)]))
        raise ValueError("Impossible maze parameters: exit unreachable.")

    def make_imperfect(self) -> None:
        """Introduces loops to the maze to make it imperfect."""
        for y in range(self.height):
            for x in range(self.width):
                if x < self.width - 1:
                    if (self.grid[y][x] & 2 and self.grid[y][x + 1] != 100
                            and self.grid[y][x] != 100):
                        if self.rdm.random() < 0.25:
                            self.grid[y][x] -= 2
                            self.grid[y][x + 1] -= 8
