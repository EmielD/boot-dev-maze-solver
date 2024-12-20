import random
import time
from cell import Cell
import uuid

class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed = None,
        ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._cells = []
        self.win = win
        self.seed = seed

        if seed is not None:
            random.seed(seed)
        
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
    
    def solve(self):
        self.win.running = True
        self._solve_r(0, 0)

    def _solve_r(self, row_number, column_number):
        if not self.win.running:
            self.win.clear_canvas()
            return False
        
        self._animate()

        current_cell:Cell = self._cells[row_number][column_number]
        current_cell.visited = True
        last_cell = self._cells[-1][-1]

        if current_cell == last_cell:
            return True
        
        directions = [
            ((-1, 0), 'has_top_wall'),    # top
            ((0, 1), 'has_right_wall'),   # right
            ((1, 0), 'has_bottom_wall'),  # bottom
            ((0, -1), 'has_left_wall')    # left
        ]

        possible_moves = []
        for (row_offset, col_offset), wall_attr in directions:
            new_row = row_number + row_offset
            new_col = column_number + col_offset
    
            if (0 <= new_row < self.num_rows and 
                0 <= new_col < self.num_cols):
        
                next_cell = self._cells[new_row][new_col]

                if not getattr(current_cell, wall_attr) and not next_cell.visited:
                    possible_moves.append(((row_offset, col_offset), next_cell))

        if len(possible_moves) == 0:
            return False

        for direction, random_next_cell in possible_moves:
            current_cell.draw_move(random_next_cell, self.win)
            if self._solve_r(row_number + direction[0], column_number + direction[1]):
                return True
            else:
                current_cell.draw_move(random_next_cell, self.win, True)
        
        return False


    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False

    def _break_entrance_and_exit(self):
        top_left_cell:Cell = self._cells[0][0]
        bottom_right_cell:Cell = self._cells[self.num_rows - 1][self.num_cols -1]
        
        top_left_cell.has_left_wall = False
        bottom_right_cell.has_right_wall = False
        
        self._draw_cell(0, 0, "black")
        self._draw_cell(self.num_rows -1, self.num_cols -1, "black")

    def _draw_cell(self, row, column, color = "black"):
        cell:Cell = self._cells[row][column]
        cell.draw(self.win, color)
        self._animate(10)

    def _animate(self, delay=50):  # delay in milliseconds instead of seconds
        if self.win:
            self.win.redraw()
            done_waiting = False
            def continue_solving():
                nonlocal done_waiting
                done_waiting = True
            self.win.after(delay, continue_solving)
            while not done_waiting:
                self.win.redraw()

    def _create_cells(self):
        for row in range(self.num_rows):

            y1 = self.y1 + (row * self.cell_size_y)
            y2 = self.y1 + ((row + 1) * self.cell_size_y)

            row_list = []

            for col in range(self.num_cols):

                x1 = self.x1 + (col * self.cell_size_x)
                x2 = self.x1 + ((col + 1) * self.cell_size_x)

                row_list.append(Cell(x1, x2, y1, y2, self.win))
                
            self._cells.append(row_list)
            
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self._draw_cell(row, col)

    def _break_walls_r(self, row_number, column_number):
        current_cell:Cell = self._cells[row_number][column_number]
        current_cell.visited = True

        while True:
            adjacent_cells = []
            if row_number > 0:
                adjacent_cells.append(((-1, 0), self._cells[row_number - 1][column_number])) # top
            if column_number < self.num_cols - 1:
                adjacent_cells.append(((0, 1), self._cells[row_number][column_number + 1])) # right
            if row_number < self.num_rows - 1:
                adjacent_cells.append(((1, 0), self._cells[row_number + 1][column_number])) # bottom
            if column_number > 0:
                adjacent_cells.append(((0, -1), self._cells[row_number][column_number - 1])) # left

            possible_directions = []
            for direction, adjacent_cell in adjacent_cells:
                cell:Cell = adjacent_cell
                if cell.visited is False:
                    possible_directions.append((direction, cell))
            
            if len(possible_directions) == 0:
                return
            
            direction, direction_cell = random.choice(possible_directions)
            direction_cell.visited = True

            if direction == (-1, 0): # moving up
                self._cells[row_number][column_number].has_top_wall = False
                self._cells[row_number -1][column_number].has_bottom_wall = False
                self._draw_cell(row_number -1, column_number)
            if direction == (0, 1): # moving right
                self._cells[row_number][column_number].has_right_wall = False
                self._cells[row_number][column_number + 1].has_left_wall = False
                self._draw_cell(row_number, column_number + 1)
            if direction == (1, 0): # moving down
                self._cells[row_number][column_number].has_bottom_wall = False
                self._cells[row_number + 1][column_number].has_top_wall = False
                self._draw_cell(row_number + 1, column_number)
            if direction == (0, -1): # moving left
                self._cells[row_number][column_number].has_left_wall = False
                self._cells[row_number][column_number -1].has_right_wall = False
                self._draw_cell(row_number, column_number - 1)

            self._draw_cell(row_number, column_number)
            self._break_walls_r(row_number + direction[0], column_number + direction[1])

