import unittest

from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_create_cells_two(self):
        num_cols = 15
        num_rows = 7
        m2 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m2._cells),
            num_cols,
        )
        self.assertEqual(
            len(m2._cells[0]),
            num_rows,
        )

    def test_maze_break_walls_and_reset_cells(self):
        num_cols = 15
        num_rows = 7
        m = Maze(0, 0, num_rows, num_cols, 10, 10)
        m.break_entrance_and_exit()
        m.dfs_maze_generator(0, 0)
        for column in m._cells:
            for cell in column:
                self.assertEqual(cell.visited, True)
        m.reset_cells_visited()
        for column in m._cells:
            for cell in column:
                self.assertEqual(cell.visited, False)


if __name__ == "__main__":
    unittest.main()
