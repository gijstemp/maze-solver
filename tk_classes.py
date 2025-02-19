from tkinter import Tk, BOTH, Canvas

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