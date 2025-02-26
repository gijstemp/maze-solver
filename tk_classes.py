from tkinter import Tk, BOTH, Canvas
import time
import random

class Window():
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("The Maze Game")
        self.canvas = Canvas(self.__root, bg="white",  height=height, width=width)
        self.canvas.pack(fill=BOTH, expand=1)
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
        
    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
        print("Window closed")
    
    def draw_line(self, line, fill_colour="black"):
        line.draw(self.canvas, fill_colour)
            
    def close(self):
        self.running = False
        
class Point():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
class Line():
    def __init__(self, start, end):
        self.start = start
        self.end = end
        
    def draw(self, canvas, fill_colour="black"):
        canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y, fill=fill_colour, width=2)
        
class Cell():
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win
        self.visited = False
        

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line, "white")
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line, "white")    
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line, "white")
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line, "white")

    def draw_move(self, to_cell, undo=False):
        half_length = abs(self._x2 - self._x1) // 2
        x_center = half_length + self._x1
        y_center = half_length + self._y1

        half_length2 = abs(to_cell._x2 - to_cell._x1) // 2
        x_center2 = half_length2 + to_cell._x1
        y_center2 = half_length2 + to_cell._y1

        fill_color = "red"
        if undo:
            fill_color = "gray"

        line = Line(Point(x_center, y_center), Point(x_center2, y_center2))
        self._win.draw_line(line, fill_color)
        
class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, window=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._win = window
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._cells = []
        
        self._create_cells()
        self._break_entrance_and_exit()
        if seed is not None:
            self._seed = random.seed(seed)
        self.break_walls_r(0, 0)
        self._reset_cells_visited()
  
        
    def _create_cells(self):
        for col in range(self._num_cols):
            cell_col = []
            for row in range(self._num_rows):
                cell_col.append(Cell(self._win))
            self._cells.append(cell_col)
        
        # Draw all cells
        for col in range(self._num_cols):
            for row in range(self._num_rows):
                self._draw_cell(col, row)
    
    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self.cell_size_x
        y1 = self._y1 + j * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()
        
    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.01)
        
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(0, 0)
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)
    
    def break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            new_list = []
            if i > 0 and not self._cells[i - 1][j].visited:
                new_list.append((i - 1, j, 'left'))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                new_list.append((i + 1, j, 'right'))
            if j > 0 and not self._cells[i][j - 1].visited:
                new_list.append((i, j - 1, 'up'))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                new_list.append((i, j + 1, 'down'))
            
            if not new_list:
                self._draw_cell(i, j)
                return
            
            # Pick a random direction
            next_i, next_j, direction = random.choice(new_list)
            
            # Knock down the walls between the current cell and the chosen cell
            if direction == 'left':
                self._cells[i][j].has_left_wall = False
                self._cells[next_i][next_j].has_right_wall = False
            elif direction == 'right':
                self._cells[i][j].has_right_wall = False
                self._cells[next_i][next_j].has_left_wall = False
            elif direction == 'up':
                self._cells[i][j].has_top_wall = False
                self._cells[next_i][next_j].has_bottom_wall = False
            elif direction == 'down':
                self._cells[i][j].has_bottom_wall = False
                self._cells[next_i][next_j].has_top_wall = False
            
            # Move to the chosen cell
            self.break_walls_r(next_i, next_j)
        
    def _reset_cells_visited(self):
        for col in range(self._num_cols):
            for row in range(self._num_rows):
                self._cells[col][row].visited = False
                
    def solve(self):
        return self._solve_r(i=0, j=0)
    
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        
        for new_i, new_j, direction in self._get_neighbours(i, j):
            if not self._cells[new_i][new_j].visited:
                if direction == 'left' and not self._cells[i][j].has_left_wall:
                    self._cells[i][j].draw_move(self._cells[new_i][new_j])
                    if self._solve_r(new_i, new_j):
                        return True
                    else:
                        self._cells[i][j].draw_move(self._cells[new_i][new_j], undo=True)
                elif direction == 'right' and not self._cells[i][j].has_right_wall:
                    self._cells[i][j].draw_move(self._cells[new_i][new_j])
                    if self._solve_r(new_i, new_j):
                        return True
                    else:
                        self._cells[i][j].draw_move(self._cells[new_i][new_j], undo=True)
                elif direction == 'up' and not self._cells[i][j].has_top_wall:
                    self._cells[i][j].draw_move(self._cells[new_i][new_j])
                    if self._solve_r(new_i, new_j):
                        return True
                    else:
                        self._cells[i][j].draw_move(self._cells[new_i][new_j], undo=True)
                elif direction == 'down' and not self._cells[i][j].has_bottom_wall:
                    self._cells[i][j].draw_move(self._cells[new_i][new_j])
                    if self._solve_r(new_i, new_j):
                        return True
                    else:
                        self._cells[i][j].draw_move(self._cells[new_i][new_j], undo=True)
        
        return False

    def _get_neighbours(self, i, j):
        neighbours = []
        if i > 0:
            neighbours.append((i - 1, j, 'left'))
        if i < self._num_cols - 1:
            neighbours.append((i + 1, j, 'right'))
        if j > 0:
            neighbours.append((i, j - 1, 'up'))
        if j < self._num_rows - 1:
            neighbours.append((i, j + 1, 'down'))
        return neighbours
                    
        