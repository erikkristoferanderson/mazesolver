from graphics import Window, Line, Point, Cell
from maze import Maze

def main():
    win = Window(800, 600)
    Maze(100, 100, 4, 6, 100, 100, win)
    win.wait_for_close()

main()