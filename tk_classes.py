from tkinter import Tk, BOTH, Canvas
import time
import random

# -----------------------------------------------------------------------------
# Module: Maze Game
# Description: This module creates a maze game using tkinter for visualization.
# It includes classes for the game window, maze cells, and the maze generation
# and solving algorithms.
# -----------------------------------------------------------------------------


class Window():
    """
    Represents the main window for the maze game using tkinter.
    Handles window creation, canvas drawing, and window closing events.
    """

    def __init__(self, width, height):
        """
        Initialize the window with a specific width and height.
        
        Parameters:
            width (int): The width of the window.
            height (int): The height of the window.
        """
        self.__root = Tk()
        self.__root.title("The Maze Game")
        # Create a canvas to draw the maze, with white background.
        self.canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.canvas.pack(fill=BOTH, expand=1)
        self.running = False
        # Bind the window close event to the custom close method.
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        """
        Refresh the window by updating idle tasks and redrawing the canvas.
        """
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        """
        Enter a loop to keep the window open until it is closed.
        Once closed, print a message.
        """
        self.running = True
        while self.running:
            self.redraw()
        print("Window closed")

    def draw_line(self, line, fill_colour="black"):
        """
        Draw a line on the canvas using the provided Line object.
        
        Parameters:
            line (Line): The line to be drawn.
            fill_colour (str): The color to use for the line (default is "black").
        """
        line.draw(self.canvas, fill_colour)

    def close(self):
        """
        Close the window by stopping the main loop.
        """
        self.running = False


class Point():
    """
    Represents a point in 2D space.
    """

    def __init__(self, x=0, y=0):
        """
        Initialize the point with x and y coordinates.
        
        Parameters:
            x (int): The x-coordinate of the point.
            y (int): The y-coordinate of the point.
        """
        self.x = x
        self.y = y


class Line():
    """
    Represents a line defined by a start and an end point.
    """

    def __init__(self, start, end):
        """
        Initialize the line with starting and ending points.
        
        Parameters:
            start (Point): The starting point of the line.
            end (Point): The ending point of the line.
        """
        self.start = start
        self.end = end

    def draw(self, canvas, fill_colour="black"):
        """
        Draw the line on a given canvas.
        
        Parameters:
            canvas (Canvas): The tkinter canvas on which to draw the line.
            fill_colour (str): The color to use for the line (default is "black").
        """
        canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y,
                           fill=fill_colour, width=2)


class Cell():
    """
    Represents a single cell in the maze.
    Each cell has walls on all four sides and a visited flag used for maze generation and solving.
    """

    def __init__(self, win=None):
        """
        Initialize the cell with all walls intact and unvisited.
        
        Parameters:
            win (Window): The Window object used to draw the cell (optional).
        """
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None  # Left coordinate of the cell on the canvas
        self._x2 = None  # Right coordinate of the cell on the canvas
        self._y1 = None  # Top coordinate of the cell on the canvas
        self._y2 = None  # Bottom coordinate of the cell on the canvas
        self._win = win  # Reference to the Window object for drawing
        self.visited = False  # Flag to mark if the cell has been visited

    def draw(self, x1, y1, x2, y2):
        """
        Draw the cell on the window's canvas using its wall properties.
        
        Parameters:
            x1 (int): The x-coordinate of the top-left corner.
            y1 (int): The y-coordinate of the top-left corner.
            x2 (int): The x-coordinate of the bottom-right corner.
            y2 (int): The y-coordinate of the bottom-right corner.
        """
        if self._win is None:
            return
        # Save the cell coordinates for later use (e.g., drawing moves)
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        # Draw left wall
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line)
        else:
            # Erase wall by drawing in white
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line, "white")

        # Draw top wall
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line, "white")

        # Draw right wall
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line, "white")

        # Draw bottom wall
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line, "white")

    def draw_move(self, to_cell, undo=False):
        """
        Visualize the move from the current cell to another cell.
        Draws a connecting line between the centers of the two cells.
        
        Parameters:
            to_cell (Cell): The cell to which the move is made.
            undo (bool): If True, draw the move in 'undo' color (gray) instead of 'red'.
        """
        # Calculate the center of the current cell
        half_length = abs(self._x2 - self._x1) // 2
        x_center = half_length + self._x1
        y_center = half_length + self._y1

        # Calculate the center of the destination cell
        half_length2 = abs(to_cell._x2 - to_cell._x1) // 2
        x_center2 = half_length2 + to_cell._x1
        y_center2 = half_length2 + to_cell._y1

        # Set the color for the move (red for forward, gray for undo)
        fill_color = "red" if not undo else "gray"

        # Draw the line representing the move
        line = Line(Point(x_center, y_center), Point(x_center2, y_center2))
        self._win.draw_line(line, fill_color)


class Maze():
    """
    Represents the maze structure, including maze generation and solving algorithms.
    """

    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, window=None, seed=None):
        """
        Initialize the maze with a grid of cells.
        
        Parameters:
            x1 (int): The x-coordinate of the top-left corner where the maze starts.
            y1 (int): The y-coordinate of the top-left corner where the maze starts.
            num_rows (int): The number of rows in the maze.
            num_cols (int): The number of columns in the maze.
            cell_size_x (int): The width of each cell.
            cell_size_y (int): The height of each cell.
            window (Window): The Window object for drawing the maze.
            seed (int, optional): Seed for random maze generation for reproducibility.
        """
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
            random.seed(seed)
        # Start generating the maze using recursive backtracking from the top-left cell.
        self.break_walls_r(0, 0)
        # Reset visited flags for solving the maze later.
        self._reset_cells_visited()

    def _create_cells(self):
        """
        Create the grid of cells for the maze and draw each cell.
        """
        # Create a 2D list of Cell objects.
        for col in range(self._num_cols):
            cell_col = []
            for row in range(self._num_rows):
                cell_col.append(Cell(self._win))
            self._cells.append(cell_col)

        # Draw each cell on the canvas.
        for col in range(self._num_cols):
            for row in range(self._num_rows):
                self._draw_cell(col, row)

    def _draw_cell(self, i, j):
        """
        Draw an individual cell based on its grid position.
        
        Parameters:
            i (int): The column index of the cell.
            j (int): The row index of the cell.
        """
        if self._win is None:
            return
        # Calculate the cell's pixel coordinates.
        x1 = self._x1 + i * self.cell_size_x
        y1 = self._y1 + j * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        # Draw the cell using its own draw method.
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        """
        Update the window to reflect any drawing changes and introduce a slight delay.
        """
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        """
        Create the entrance and exit for the maze by breaking the top wall
        of the first cell and the bottom wall of the last cell.
        """
        self._cells[0][0].has_top_wall = False
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(0, 0)
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def break_walls_r(self, i, j):
        """
        Recursively generate the maze using the recursive backtracking algorithm.
        This method marks the current cell as visited and then randomly moves to
        an adjacent unvisited cell, breaking the wall between them.
        
        Parameters:
            i (int): The current cell's column index.
            j (int): The current cell's row index.
        """
        self._cells[i][j].visited = True
        while True:
            new_list = []
            # Check left neighbor
            if i > 0 and not self._cells[i - 1][j].visited:
                new_list.append((i - 1, j, 'left'))
            # Check right neighbor
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                new_list.append((i + 1, j, 'right'))
            # Check upper neighbor
            if j > 0 and not self._cells[i][j - 1].visited:
                new_list.append((i, j - 1, 'up'))
            # Check lower neighbor
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                new_list.append((i, j + 1, 'down'))

            # If there are no unvisited neighbors, finish recursion for this cell.
            if not new_list:
                self._draw_cell(i, j)
                return

            # Randomly select an unvisited neighbor.
            next_i, next_j, direction = random.choice(new_list)

            # Knock down the wall between the current cell and the chosen neighbor.
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

            # Recursively break walls from the chosen neighbor.
            self.break_walls_r(next_i, next_j)

    def _reset_cells_visited(self):
        """
        Reset the visited flag for all cells in the maze.
        This is useful before starting the maze solving algorithm.
        """
        for col in range(self._num_cols):
            for row in range(self._num_rows):
                self._cells[col][row].visited = False

    def solve(self):
        """
        Solve the maze starting from the entrance (top-left cell) and attempting to
        reach the exit (bottom-right cell).
        
        Returns:
            bool: True if a solution is found, False otherwise.
        """
        return self._solve_r(i=0, j=0)

    def _solve_r(self, i, j):
        """
        Recursively solve the maze using a backtracking algorithm.
        
        Parameters:
            i (int): The current cell's column index.
            j (int): The current cell's row index.
        
        Returns:
            bool: True if the exit is reached, False otherwise.
        """
        self._animate()
        self._cells[i][j].visited = True

        # Check if the current cell is the exit.
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        # Explore all neighboring cells.
        for new_i, new_j, direction in self._get_neighbours(i, j):
            if not self._cells[new_i][new_j].visited:
                # Check if movement in the given direction is possible (no wall exists).
                if direction == 'left' and not self._cells[i][j].has_left_wall:
                    self._cells[i][j].draw_move(self._cells[new_i][new_j])
                    if self._solve_r(new_i, new_j):
                        return True
                    else:
                        # Undo the move if it doesn't lead to a solution.
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

        # Return False if no path from the current cell leads to the exit.
        return False

    def _get_neighbours(self, i, j):
        """
        Get a list of all neighbouring cells (with their positions and relative directions)
        for a given cell at position (i, j).
        
        Parameters:
            i (int): The current cell's column index.
            j (int): The current cell's row index.
        
        Returns:
            list: A list of tuples in the format (new_i, new_j, direction) representing neighbours.
        """
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
