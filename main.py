from tk_classes import *

def main():
    win = Window(800, 600)
    win.draw_line(Line(Point(0, 0), Point(800, 600)))
    win.draw_line(Line(Point(0, 600), Point(800, 0)))
    win.draw_line(Line(Point(0, 300), Point(800, 300)))
    win.draw_line(Line(Point(400, 0), Point(400, 600)))
    win.wait_for_close()
    
if __name__ == "__main__":
    main()