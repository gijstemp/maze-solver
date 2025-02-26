from tkinter import Tk, BOTH, Canvas
import time

class Window():
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("The Maze Game")
        self.height = height
        self.width = width
        self.__root.geometry(f"{width}x{height}")
        self.canvas = Canvas(self.__root, bg="white")
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
    def __init__(self, top_left, bottom_right, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = top_left.x
        self._y1 = top_left.y
        self._x2 = bottom_right.x
        self._y2 = bottom_right.y
        self._win = window
        
    def draw(self, canvas, fill_colour="black"):
        if self.has_left_wall:
            canvas.create_line(self._x1, self._y1, self._x1, self._y2, fill=fill_colour, width=2)
        if self.has_right_wall:
            canvas.create_line(self._x2, self._y1, self._x2, self._y2, fill=fill_colour, width=2)
        if self.has_top_wall:
            canvas.create_line(self._x1, self._y1, self._x2, self._y1, fill=fill_colour, width=2)
        if self.has_bottom_wall:
            canvas.create_line(self._x1, self._y2, self._x2, self._y2, fill=fill_colour, width=2)
            
    def draw_move(self, to_cell, undo=False):
        # Calculate the center points of the current cell and the target cell
        x1_center = (self._x1 + self._x2) // 2
        y1_center = (self._y1 + self._y2) // 2
        x2_center = (to_cell._x1 + to_cell._x2) // 2
        y2_center = (to_cell._y1 + to_cell._y2) // 2
        
        # Determine the color of the line
        line_color = "red" if not undo else "gray"
        
        # Draw the line connecting the centers of the two cells
        self._win.canvas.create_line(x1_center, y1_center, x2_center, y2_center, fill=line_color, width=2)
        
class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, window=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._win = window
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._cells = []
        self._create_cells()
        
    def _create_cells(self):
        for row in range(self._num_rows):
            cell_row = []
            for col in range(self._num_cols):
                top_left = Point(self._x1 + col * self.cell_size_x, self._y1 + row * self.cell_size_y)
                bottom_right = Point(self._x1 + (col + 1) * self.cell_size_x, self._y1 + (row + 1) * self.cell_size_y)
                cell = Cell(top_left, bottom_right, self._win)
                cell_row.append(cell)
                cell._draw_cell(row, col)
            self._cells.append(cell_row)
    
    def _draw_cell(self, i, j):
        cell = self._cells[i][j]
        cell.draw(self._win.canvas)
        self._animate()
        
    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)