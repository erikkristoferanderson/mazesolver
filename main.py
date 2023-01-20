from graphics import Window, Line, Point, Cell
from maze import Maze
import time

def main():
    win = Window(800, 600)
    m = Maze(100, 100, 16, 24, 25, 25, win=win)

    m._break_entrance_and_exit()
    m._break_walls_r(0, 0)
    m._reset_cells_visited()
    m.solve()
    win.wait_for_close()
    
main()