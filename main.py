from graphics import Window, Line, Point, Cell
from maze import Maze

def main():
    win = Window(800, 600)
    m = Maze(100, 100, 4, 6, 100, 100, win)
    for i in range(4):
        m._draw_cell(i, 0)
    win.wait_for_close()

main()