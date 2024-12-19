from tkinter import Canvas
from point import Point


class Line():
    def __init__(self, point_one:Point, point_two:Point):
        self.x1 = point_one.x
        self.y1 = point_one.y
        self.x2 = point_two.x
        self.y2 = point_two.y
    
    def draw(self, canvas:Canvas, fill_color:str, width:int=20):
        canvas.create_line(
            self.x1, self.y1, self.x2, self.y2, fill=fill_color, width=width
        )
