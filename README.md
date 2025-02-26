# Maze Solver

This project is a maze solver implemented using Python and the Tkinter library for graphical representation. The maze is generated with walls, and the solver finds a path from the start to the end of the maze.

## Features

- Generate a maze with customizable dimensions.
- Visualize the maze generation process.
- Solve the maze and visualize the solution path.
- Highlight the backtracking steps in a different color.

## Requirements

- Python 3.x
- Tkinter (usually included with Python)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/maze-solver.git
    cd maze-solver
    ```

2. (Optional) Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the maze solver, execute the [main.py](http://_vscodecontentref_/1) file:

```bash
python main.py
```

This will open a window displaying the maze generation process and the solution path.

## Project Structure
- main.py: The main entry point of the application. It sets up the window, creates the maze, and starts the solving process.
- tk_classes.py: Contains the classes for the maze, cells, and window, including the logic for maze generation and solving.
- tests.py: Contains unit tests for the maze solver.

## Classes
`Window`
Represents the application window.

- `__init__(self, width, height)`: Initializes the window with the given width and height.
- `redraw(self)`: Redraws the window.
- `wait_for_close(self)`: Keeps the window open until it is closed.
- `draw_line(self, line, fill_colour="black")`: Draws a line on the canvas.
- `close(self)`: Closes the window.

`Point`
Represents a point in 2D space.

- `__init__(self, x=0, y=0)`: Initializes the point with the given coordinates.

`Line`
Represents a line between two points.

- `__init__(self, start, end)`: Initializes the line with the given start and end points.
- `draw(self, canvas, fill_colour="black")`: Draws the line on the canvas.

`Cell`
Represents a cell in the maze.

- `__init__(self, top_left=None, bottom_right=None, win=None)`: Initializes the cell with the given coordinates and window.
- `draw(self, x1, y1, x2, y2)`: Draws the cell on the canvas.
- `draw_move(self, to_cell, undo=False)`: Draws a move between this cell and another cell.

`Maze`
Represents the maze.

- `__init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, window=None, seed=None)`: Initializes the maze with the given parameters.
- `_create_cells(self)`: Creates the cells of the maze.
- `_draw_cell(self, i, j)`: Draws a specific cell.
- `_animate(self)`: Redraws the window.
- `_break_entrance_and_exit(self)`: Breaks the entrance and exit walls.
- `break_walls_r(self, i, j)`: Recursively breaks walls to generate the maze.
- `_reset_cells_visited(self)`: Resets the visited status of all cells.
- `solve(self)`: Solves the maze.
- `_solve_r(self, i, j)`: Recursively solves the maze.
- `_get_neighbours(self, i, j)`: Gets the neighboring cells.

## Testing
To run the unit tests, execute the `tests.py` file:

```bash
python tests.py
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

