import unittest
from tk_classes import Window, Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        window = Window(800, 600)  # Create a Window object
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, window)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

if __name__ == "__main__":
    unittest.main()