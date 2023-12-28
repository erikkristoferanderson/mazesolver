from tkinter import Tk, BOTH, Canvas, Label


def line_draw(canvas, start_x, start_y, end_x, end_y, color, width, dash=()):
    canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=width, dash=dash)


class Window:
    """
    A Tkinter window with a canvas widget.
    """
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.algorithm_label = Label(self.__root, text="", font=("Arial", 25))
        self.algorithm_label.pack()
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def get_canvas(self):
        return self.__canvas

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
    
    def close(self):
        self.__running = False


class Cell:
    """
    _x1 and _y1 represent the top left corner of the cell
    _x2 and _y2 represent the bottom right corner of the cell
    """
    def __init__(
        self, _x1, _x2, _y1, _y2,
        visited: bool = False,
        _win: Window = None,
        has_left_wall=True,
        has_right_wall=True,
        has_top_wall=True,
        has_bottom_wall=True
    ):
        self._x1, self._x2 = _x1, _x2
        self._y1, self._y2 = _y1, _y2
        self.x_center = (_x1 + _x2)/2
        self.y_center = (_y1 + _y2)/2
        self.visited = visited
        self._win = _win
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self.neighbours = ["top", "bottom", "left", "right"]
        self.path_history = []

    def draw(self):
        if self._win is None:
            return

        # tf means tidy factor to prevent formation of holes in the corners of cells

        (color, tf) = ("black", 0) if self.has_top_wall else ("white", 1)
        line_draw(self._win.get_canvas(), self._x1 + tf, self._y1, self._x2 - tf, self._y1, color=color, width=2)

        (color, tf) = ("black", 0) if self.has_right_wall else ("white", 1)
        line_draw(self._win.get_canvas(), self._x2, self._y1 + tf, self._x2, self._y2 - tf, color=color, width=2)

        (color, tf) = ("black", 0) if self.has_bottom_wall else ("white", 1)
        line_draw(self._win.get_canvas(), self._x1 + tf, self._y2, self._x2 - tf, self._y2, color=color, width=2)

        (color, tf) = ("black", 0) if self.has_left_wall else ("white", 1)
        line_draw(self._win.get_canvas(), self._x1, self._y1 + tf, self._x1, self._y2 - tf, color=color, width=2)

    def __repr__(self):
        return f'Cell: ({self._x1},{self._y1}),({self._x2},{self._y2})'
    
    def draw_move(self, to_cell, undo=False):
        if undo:
            line_draw(self._win.get_canvas(), self.x_center, self.y_center, to_cell.x_center, to_cell.y_center,
                      color="white", width=2)
        color = "red" if undo else "green"
        line_draw(self._win.get_canvas(), self.x_center, self.y_center, to_cell.x_center, to_cell.y_center,
                  color=color, width=2, dash=(10, 1))
