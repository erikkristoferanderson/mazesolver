from graphics import Window
from maze import Maze


def main():
    """
    Creates and solves a maze.
    :return:
    """
    rows, columns = 10, 10
    cell_width, cell_height = 25, 25
    # solve_algorithms = "depth first search", "right hand rule", "breadth first search"
    solve_algorithm = "breadth first search"

    window_height = rows*cell_height+40
    window_width = columns*cell_width+40

    win = Window(window_width, window_height)

    m = Maze(20, 20, rows, columns, cell_width, cell_height, win=win, frame_delay=0.02)

    m.break_entrance_and_exit()
    m.dfs_maze_generator(0, 0)

    m.reset_cells_visited()
    m.solve(algorithm=solve_algorithm)

    win.wait_for_close()


main()
