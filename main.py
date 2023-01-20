from graphics import Window, Line, Point, Cell
from maze import Maze
import time

def main():
    win = Window(800, 600)
    # m = Maze(100, 100, 4, 6, 100, 100, 5, win)
    m = Maze(100, 100, 8, 12, 50, 50, seed=6, win=win)
    # for i in range(4):
    #     m._draw_cell(i, 0)

    m._break_entrance_and_exit()
    # time.sleep(3)
    m._break_walls_r(0, 0)
    win.wait_for_close()
    
main()