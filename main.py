from graphics import Window, Line, Point, Cell

def main():
    win = Window(800, 600)
    # my_line = Line(Point(50, 500), Point(30, 40))
    # win.draw_line(my_line)
    # my_line_2 = Line(Point(3, 4), Point(50, 300))
    # win.draw_line(my_line_2)
    cell_1 = Cell(300, 450, 200, 400, win)
    cell_1.draw()
    cell_2 = Cell(100, 200, 100, 200, win)
    cell_2.has_bottom_wall = False
    cell_2.has_left_wall = False
    cell_2.draw()
    cell_3 = Cell(600, 700, 400, 500, win)
    cell_3.has_top_wall = False
    cell_3.has_right_wall = False
    cell_3.draw()
    cell_3.draw_move(cell_2)
    cell_2.draw_move(cell_1, undo=True)
    win.wait_for_close()


main()