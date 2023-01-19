from graphics import Window, Line, Point

def main():
    win = Window(800, 600)
    my_line = Line(Point(50, 500), Point(30, 40))
    win.draw_line(my_line)
    my_line_2 = Line(Point(3, 4), Point(50, 300))
    win.draw_line(my_line_2)
    win.wait_for_close()

main()