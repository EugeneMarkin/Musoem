import tkinter as tk
from text_pipe import TextPipe
from command_map import CommandMap, test_map
from now_playing import NowPlaying

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        NowPlaying.reset()
        self.frame = tk.Frame(self)
        self.frame.pack()
        self.pipe = TextPipe(test_map)
        self.input = tk.Text(self.frame, width = 100, height = 25)
        self.output = tk.Text(self.frame, width = 100, height = 25)
        self.input.insert('end', "Lorem ipsum...\n...\n...")
        self.input.bind("<Key>", self.key_press)
        self.input.pack(side = tk.TOP)
        self.output.pack(side = tk.BOTTOM)


    def key_press(self, event):
        print("key press")
        print(event)
        if event.keysym == "Return" and (event.state & 0x0004): # mask for ctrl key
            self.execute()
            return 'break'

    def execute(self):
        print("execute")
        cursor = self.input.index(tk.INSERT)
        line = cursor.split(".")[0]
        selection = self.input.get(line + "." + "0", line + "." + "end")
        print(selection)
        self.input.tag_add("sel", line + "." + "0", line + "." + "end")
        self.pipe.parse_line(selection)
        self.display_output()

    def display_output(self):
        self.output.delete("1.0", "end")
        self.output.insert("end", NowPlaying.display())

if __name__ == "__main__":
    app = Gui()
    app.mainloop()


# font size for particular words, bold, italic might mean something
# Capital letters
