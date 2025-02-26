from tk_classes import *

def main():
    # Create a window
    window = Window(800, 600)
    # Define points for the corners of the cells
    top_left_1 = Point(50, 50)
    bottom_right_1 = Point(150, 150)

    top_left_2 = Point(200, 50)
    bottom_right_2 = Point(300, 150)

    top_left_3 = Point(50, 200)
    bottom_right_3 = Point(150, 300)

    top_left_4 = Point(200, 200)
    bottom_right_4 = Point(300, 300)
    
    # Create cells with different wall configurations
    cell1 = Cell(top_left_1, bottom_right_1, window)
    cell2 = Cell(top_left_2, bottom_right_2, window)
    cell2.has_left_wall = False

    cell3 = Cell(top_left_3, bottom_right_3, window)
    cell3.has_top_wall = False

    cell4 = Cell(top_left_4, bottom_right_4, window)
    cell4.has_right_wall = False
    cell4.has_bottom_wall = False

    # Draw the cells
    cell1.draw(window.canvas)
    cell2.draw(window.canvas)
    cell3.draw(window.canvas)
    cell4.draw(window.canvas)

    # Start the window's main loop
    window.wait_for_close()
    
if __name__ == "__main__":
    main()