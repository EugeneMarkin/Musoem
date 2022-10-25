import tkinter as tk
from text_pipe import TextPipe
from command_map import CommandMap
from mary_lamb import mary_map
from now_playing import NowPlaying

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        NowPlaying.reset()
        self.frame = tk.Frame(self)
        self.frame.pack()
        self.pipe = TextPipe(mary_map)
        self.input = tk.Text(self.frame, width = 100, height = 25)
        self.output = tk.Text(self.frame, width = 100, height = 25)
        self.input.bind("<Key>", self.key_press)
        self.output.bind("<Key>", self.output_edit)
        self.input.pack(side = tk.TOP)
        self.output.pack(side = tk.BOTTOM)


    def key_press(self, event):
        print("key press")
        print(event)
        if event.keysym == "Return" and (event.state & 0x0004): # mask for ctrl key
            self.execute()
            return 'break'

    def output_edit(self, event):
        if event.keysym in ["KP_Down", "KP_Up", "KP_Left", "KP_Right"]:
            return
        elif event.keysym != "BackSpace":
            return "break"

        cursor = self.output.index(tk.INSERT)
        x = int(cursor.split(".")[0])
        y = int(cursor.split(".")[1])
        symbol = self._get_symbol(x, y-1)
        if symbol == ' ':
            return 'break'
        y_start = y
        while y_start > 0:
            symbol = self._get_symbol(x, y-1)
            print(symbol)
            if symbol == ' ':
                print("break")
                break
            y_start = y_start - 1
        y_end = y
        symbol = self._get_symbol(x, y_end)
        while (symbol != ' ') and symbol != '':
            y_end = y_end + 1
            symbol = self._get_symbol(x, y_end)

        range = (str(x) + "." + str(y_start), str(x) + "." + str(y_end))
        keyword = self.output.get(range[0], range[1])
        self.stop(keyword)
        self.output.delete(range[0], range[1])
        return 'break'

    def stop(self, keyword):
        print(keyword)
        NowPlaying.remove(keyword)

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

    def _get_symbol(self, x, y):
         return self.output.get(str(x) + "." + str(y))

if __name__ == "__main__":
    app = Gui()
    app.mainloop()


# font size for particular words, bold, italic might mean something
# Capital letters
