import uuid
from cell import Cell
from line import Line
from maze import Maze
from window import Window

def start_new_maze():
    win.clear_canvas()
    maze = Maze(450, 50, 20, 20, 50, 50, win, str(uuid.uuid4()))
    win.redraw()
    maze.solve()

# Create window and initial maze
win = Window(1920, 1080, refresh_callback=start_new_maze)
start_new_maze()
win.wait_for_close()