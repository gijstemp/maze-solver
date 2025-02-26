from tk_classes import *

def main():
    """
    Main function to initialize and run the maze game.
    
    This function sets up the maze configuration, calculates cell sizes,
    initializes the game window, creates and solves the maze, and finally
    starts the main loop to display the maze.
    """
    # Maze configuration parameters
    num_rows = 12      # Number of rows in the maze grid
    num_cols = 16      # Number of columns in the maze grid
    margin = 50        # Margin from the window's edges where the maze will be drawn
    screen_x = 800     # Width of the game window in pixels
    screen_y = 600     # Height of the game window in pixels
    
    # Calculate the size of each cell in the maze
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    
    # Initialize the game window with the specified screen dimensions
    win = Window(screen_x, screen_y)
    
    # Create the maze with the given parameters and attach it to the window
    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)
    
    # Solve the maze by finding a path from the entrance to the exit
    maze.solve()
    
    # Start the window's main loop to keep the game running until the window is closed
    win.wait_for_close()
    
if __name__ == "__main__":
    main()