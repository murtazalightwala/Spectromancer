import tkinter as Tk
from snakesAndLadders import Board
import os
import tksvg
 

class SvgImage(Tk.PhotoImage):
    """Widget which can display images in PGM, PPM, GIF, PNG format."""
    _tksvg_loaded = False
    _svg_options = ['scale', 'scaletowidth', 'scaletoheight']
    def __init__(self, name=None, cnf={}, master=None, **kw):
        # load tksvg
        if not SvgImage._tksvg_loaded:
            if master is None:
                master = Tk._default_root
                if not master:
                    raise RuntimeError('Too early to create image')
            master.tk.eval('package require tksvg')
            SvgImage._tksvg_loaded = True
        # remove specific svg options from keywords
        svgkw = {opt: kw.pop(opt, None) for opt in self._svg_options}
        Tk.PhotoImage.__init__(self, name, cnf, master, **kw)
        # pass svg options
        self.configure(**svgkw)
    def configure(self, **kw):
        svgkw = {opt: kw.pop(opt) for opt in self._svg_options if opt in kw}
        # non svg options
        if kw:
            Tk.PhotoImage.configure(self, **kw)
        # svg options
        options = ()
        for k, v in svgkw.items():
            if v is not None:
                options = options + ('-'+k, str(v))
        self.tk.eval('%s configure -format {svg %s}' % (self.name, ' '.join(options)))


Board().draw_board()
main = Tk.Tk(screenName="Snakes and Ladders")
main.title("Snakes and Ladders")
main.attributes("-fullscreen", True)
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()
frame = Tk.Frame(master = main, padx = 10, pady = 10, width = 750, height = 750, background= "grey")
board = SvgImage(name = "board", master = main, file = "test.svg", scale = 1)
label = Tk.Label(master = frame, image=board)
label.pack()
frame.pack(side = Tk.TOP, anchor= "nw")
main.mainloop()
