import tkinter as tk

from line import Line

class Window():
    def __init__(self, width, height, refresh_callback=None):
        self.width = width
        self.height = height
        self.__root = tk.Tk()
        self.__canvas = tk.Canvas(height=height, width=width, bg="white")
        self.running = False
        self.__refresh_callback = refresh_callback
        self.pending_callback = None

        self.__root.title("Boot Dev Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas.pack()

        self.init_buttons()

    def __handle_refresh(self):
        self.running = False
        # Cancel any pending callback
        if self.pending_callback:
            self.__root.after_cancel(self.pending_callback)
            self.pending_callback = None
        
        if self.__refresh_callback:
            self.clear_canvas()
            self.__refresh_callback()
    
    def __schedule_update(self):
        if self.running:
            self.redraw()
            self.__root.after(16, self.__schedule_update)  # roughly 60 FPS

    def after(self, delay, callback):
        if self.running:  # Only schedule if window is still running
            if self.pending_callback:
                self.__root.after_cancel(self.pending_callback)
        self.pending_callback = self.__root.after(delay, callback)
        print(self.pending_callback)

    def clear_canvas(self):
        self.__canvas.delete("all")
        self.__root.update()

    def redraw(self):
        self.__root.update()

    def init_buttons(self):
        refresh_maze_button = tk.Button(self.__root,text="Refresh maze",command=self.__handle_refresh)
        refresh_maze_button.pack()

    def wait_for_close(self):
        self.running = True
        self.__schedule_update()
        self.__root.mainloop()
    
    def close(self):
        self.running = False
        self.__root.destroy()

    def draw_line(self, line:Line, fill_color:str):
        line.draw(self.__canvas, fill_color)