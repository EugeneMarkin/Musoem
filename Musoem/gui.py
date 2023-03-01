import tkinter as tk
from tkinter import filedialog as fd
from functools import reduce
from uuid import uuid4
import os

from music.survival_kit import survival_kit_map
from lib.player.now_playing import NowPlaying
from lib.command.command_parser import TextParser
from lib.score.score_dir import ScoreDir


class Tag:

    def __init__(self, line, range, playable):
        self.id = str(uuid4())
        self.line = line
        self.range = range
        self.playable = playable

    def apply_to(self, text):
        start = str(self.line) + "." + str(self.range[0])
        end = str(self.line) + "." + str(self.range[-1])
        text.tag_add(self.id, start, end)
        self._apply_style(text)

    def _apply_style(self, text):
        font = tk
        if self.playable.display_style == "italic":
            font = ("Helvetica", 20, "italic")

    def has_cursor(self, x, y):
        return x == self.line and y in self.range

    def __str__(self):
        return "id " + self.id + "kw " + self.playable.keyword

class Menu:

    def __init__(self, app):
        # TODO: add some kind of a default demo project
        # that will open.
        # TODO: add a preferences file serialization to open the most
        # recent project
        self.command_map = None

        self.menubar = tk.Menu(app)
        filemenu = tk.Menu(self.menubar, tearoff = 0)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Reload", command=self.reload)
        self.menubar.add_cascade(label="File", menu = filemenu)
        app.config(menu = self.menubar)
        app.winfo_toplevel().title("Musoem")

    # TODO: add hot keys to these both functions
    def open_file(self):
        print("open file")
        self.dir_path = fd.askdirectory(initialdir = os.path.expanduser('~'))
        self._load(self.dir_path)

    def reload(self):
        print("reload")
        NowPlaying.reset()
        self._load(self.dir_path)

    def _load(self, path):
        command_map = ScoreDir(path).load()
        app.command_parser = TextParser(command_map)

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        NowPlaying.reset()
        NowPlaying.bind_callback(self.display_output)
        self.playing = []
        self.frame = tk.Frame(self)
        self.frame.configure(padx=0, pady=0, relief = "flat", bd=1)
        self.frame.pack(fill = "both", expand = True, ipadx=0, ipady=0)
        self.input = tk.Text(self.frame, width = 50, height = 1)
        self.output = tk.Text(self.frame, width = 50, height = 20)

        self.input.bind("<Key>", self.key_press)
        self.output.bind("<Key>", self.output_edit)

        self.input.pack(side = tk.TOP, fill = "both",  expand = True, ipady = 0)
        self.output.pack(side = tk.BOTTOM, fill = "both", expand = True, ipady = 0)
        font = ("Helvetica", 20, "normal")
        self.input.configure(font = ("Helvetica", 28, "normal"), background = "black", foreground = "white", bd=1, selectborderwidth = 0, insertbackground = "white")
        self.output.configure(font = ("Helvetica", 20, "normal"),  background = "black", foreground = "white", bd=1, selectborderwidth = 0, insertbackground = "white")

        self.menu = Menu(self)


    def key_press(self, event):
        if event.keysym == "Return" and (event.state & 0x0004): # mask for ctrl key
            self.execute()
            return 'break'

    def output_edit(self, event):
        if event.keysym in ["Down", "Up", "Left", "Right"]:
            return
        elif event.keysym != "BackSpace":
            return "break"

        cursor = self.output.index(tk.INSERT)
        x = int(cursor.split(".")[0])
        y = int(cursor.split(".")[1])

        tag = list(filter(lambda t: t.has_cursor(x,y), self.playing))[0]
        ~tag.playable
        print(tag)

        return 'break'

    def execute(self):
        cursor = self.input.index(tk.INSERT)
        line = cursor.split(".")[0]
        selection = self.input.get(line + "." + "0", line + "." + "end")
        print(selection)
        self.input.delete("1.0", "1.end")
        #self.input.tag_add("sel", line + "." + "0", line + "." + "end")
        statement = self.command_parser.parse_line(selection)
        statement.execute()


    def display_output(self):
        self.output.delete("1.0", "end")
        lines = NowPlaying.display()
        out = ""
        self.playing = []
        for l in lines:
            y = 0
            for p in l:
                kw = p.keyword
                r = range(y, y + len(kw) + 1)
                tag = Tag(lines.index(l) + 1, r, p)
                y += len(kw) + 1
                out += kw + " "
                self.playing.append(tag)
                tag.apply_to(self.output)
            out += "\n"
        self.output.insert("end", out)
        self.output.tag_add("highlightline", "1.0", "1.5")
        #self.output.tag_bind("highlightline", "<KeyPress>", lambda t: print("my tag", t))
        self.output.tag_bind("highlightline", "<KeyRelease>", lambda t: print("my tag", t))

    def _get_symbol(self, x, y):
         return self.output.get(str(x) + "." + str(y))


if __name__ == "__main__":
    app = Gui()
    app.mainloop()


# font size for particular words, bold, italic might mean something
# Capital letters

# litmus test

# looping the whole section ?
