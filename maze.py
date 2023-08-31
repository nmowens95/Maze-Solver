from cell import Cell
import random
import time

class Maze():
    def __init__ (
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed = None
        ):

        self.cells = []
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed: 
            random.seed(seed)

        self.create_cells()
        self.break_entrance_and_exit()
        self.break_walls_r(0, 0)
        self.reset_cells_visited()

    def create_cells(self):
        for i in range(self.num_cols):
            col_cells = []
            for j in range(self.num_rows):
                col_cells.append(Cell(self.win))
            self.cells.append(col_cells)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.draw_cells(i, j)

    def draw_cells(self, i, j):
        if self.win is None:
            return 
        x1 = self.x1 + i * self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self.cells[i][j].draw(x1, y1, x2, y2)
        self.animate()

    def animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.05)

    def break_entrance_and_exit(self):
        self.cells[0][0].has_top_wall = False
        self.draw_cells(0, 0)
        self.cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self.draw_cells(self.num_cols - 1, self.num_rows - 1)

    def break_walls_r(self, i, j):
        self.cells[i][j].visted = True
        while True:
            next_index_list = []

            possible_direction_indexes = 0

            # Need to determine which cells need to be visited next

            # left
            if i > 0 and not self.cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
                possible_direction_indexes += 1
            # right
            if i < self.num_cols - 1 and not self.cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
                possible_direction_indexes += 1
            # up
            if j > 0 and not self.cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
                possible_direction_indexes += 1
            # down
            if j < self.num_rows -1 and not self.cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))
                possible_direction_indexes += 1

            # If there is nowhere to go, just break out
            if possible_direction_indexes == 0:
                self.draw_cells(i, j)
                return

            # Implement to choose random directions to go
            direction_index = random.randrange(possible_direction_indexes)
            next_index = next_index_list[direction_index]

            # Knocks out walls between this cell and the next cell
            # right
            if next_index[0] == i + 1:
                self.cells[i][j].has_right_wall = False
                self.cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self.cells[i][j].has_left_wall = False
                self.cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self.cells[i][j].has_bottom_wall = False
                self.cells[i][j + 1].has_top_wall = False
            # right
            if next_index[1] == j - 1:
                self.cells[i][j].has_top_wall = False
                self.cells[i][j - 1].has_bottom_wall = False

            # Use recursion to visit the next cell
            self.break_walls_r(next_index[0], next_index[1])

    def reset_cells_visited(self):
        for col in self.cells:
            for cell in col:
                cell.visited = False

    # returns True if this is the end cell, or if it leads to the end cell
    # returns false if this is a loser cell

    def solve_r(self, i, j):
        self.animate()

        # vist the current cell
        self.cells[i][j].visited = True

        # if we are at the end cell, we are done!
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True

        # move left if there is no wall and it hasn't been visited
        if (
            i > 0
            and not self.cells[i][j].has_left_wall
            and not self.cells[i - 1][j].visited
        ):
            self.cells[i][j].draw_move(self._cells[i - 1][j])
            if self.solve_r(i - 1, j):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i - 1][j], True)

        # move right if there is no wall and it hasn't been visited
        if (
            i < self.num_cols - 1
            and not self.cells[i][j].has_right_wall
            and not self.cells[i + 1][j].visited
        ):
            self.cells[i][j].draw_move(self.cells[i + 1][j])
            if self.solve_r(i + 1, j):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i + 1][j], True)

        # move up if there is no wall and it hasn't been visited
        if (
            j > 0
            and not self.cells[i][j].has_top_wall
            and not self.cells[i][j - 1].visited
        ):
            self.cells[i][j].draw_move(self.cells[i][j - 1])
            if self.solve_r(i, j - 1):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i][j - 1], True)

        # move down if there is no wall and it hasn't been visited
        if (
            j < self.num_rows - 1
            and not self.cells[i][j].has_bottom_wall
            and not self.cells[i][j + 1].visited
        ):
            self.cells[i][j].draw_move(self.cells[i][j + 1])
            if self.solve_r(i, j + 1):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i][j + 1], True)

        # we went the wrong way let the previous cell know by returning False
        return False


    # create the moves for the solution using a depth first search
    def solve(self):
        return self.solve_r(0, 0)

