from textwrap import fill
import tkinter as tk


class Canvas(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.base = master.base

        self.config(width=50, bg="#1e1e1e", highlightthickness=0)


class LineNumbers(tk.Frame):
    def __init__(self, master, tw, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.base = master.base

        self.config_appearance()

        self.tw = tw

        self.cw = Canvas(self)
        self.cw.pack(fill=tk.BOTH, expand=True)
    
    def set_bar_width(self, width):
        self.configure(width=width)

    def config_appearance(self):
        self.font = self.base.config.font
        self.fill = "#858585"
        self.highlight_fill = "#c6c6c6"
        self.config(bg="#1e1e1e")
    
    def attach(self, tw):
        self.tw = tw
    
    def clear(self):
        self.cw.delete(tk.ALL)
    
    def highlight_current_line(self):
        dline = self.tw.get_line_info(tk.INSERT)
        y = dline[1]
        self.cw.create_text(50, y, anchor=tk.NE, text=">", font=self.font, fill="red")

    def redraw(self, *args):
        self.clear()
        self.highlight_current_line()
        self.redraw_line_numbers()

    def redraw_line_numbers(self):
        i = self.tw.get_origin()
        while True:
            dline = self.tw.get_line_info(i)
            if not dline:
                break

            y = dline[1]
            ln = str(i).split(".")[0]

            curline = self.tw.get_line_info(tk.INSERT)
            cur_y = None
            if curline:
                cur_y = curline[1]

            if y == cur_y:
                self.cw.create_text(35, y, anchor=tk.NE, text=ln, font=self.font, fill=self.highlight_fill)
            else:
                self.cw.create_text(35, y, anchor=tk.NE, text=ln, font=self.font, fill=self.fill)

            i = self.tw.textw.index(f"{i}+1line")

