from line import Line
from point import Point
from window import Window

class Cell():
    def __init__(self, x1:int, x2:int, y1:int, y2:int, win:Window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2

    def __draw_wall(self, point1, point2, win:Window, color="black"):
        win.draw_line(Line(point1, point2), color)

    def draw(self, win:Window, color="black"):
            walls = [
                (self.has_left_wall, Point(x=self.__x1, y=self.__y1), Point(x=self.__x1, y=self.__y2)),
                (self.has_right_wall, Point(x=self.__x2, y=self.__y1), Point(x=self.__x2, y=self.__y2)),
                (self.has_top_wall, Point(x=self.__x1, y=self.__y1), Point(x=self.__x2, y=self.__y1)),
                (self.has_bottom_wall, Point(x=self.__x1, y=self.__y2), Point(x=self.__x2, y=self.__y2))
            ]

            for has_wall, point1, point2 in walls:
                wall_color = color if has_wall else "white"
                self.__draw_wall(point1, point2, win, wall_color)

    def draw_move(self, to_cell, win:Window, undo:bool=False):
        line_draw_color = "green"
        if undo:
            line_draw_color = "red"
        
        win.draw_line(Line(self.get_center(), to_cell.get_center()), line_draw_color)

    def get_center(self):
        return Point(
            (self.__x1 + self.__x2) / 2,
            (self.__y1 + self.__y2) / 2
        )