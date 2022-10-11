import tkinter as tk
from text_pipe import TextPipe


class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.pipe = TextPipe()
        self.text = tk.Text(self, width = 100, height = 50)
        self.text.insert('end', "Lorem ipsum...\n...\n...")
        self.text.bind("<Key>", self.key_press)
        self.text.pack()

    def key_press(self, event):
        print("key press")
        print(event)
        if event.keysym == "Return" and (event.state & 0x0004): # mask for ctrl key
            self.execute()
            return 'break'

    def execute(self):
        print("execute")
        cursor = self.text.index(tk.INSERT)
        line = cursor.split(".")[0]
        selection = self.text.get(line + "." + "0", line + "." + "end")
        print(selection)
        self.text.tag_add("sel", line + "." + "0", line + "." + "end")
        self.pipe.parse_line(selection)



if __name__ == "__main__":
    app = Gui()
    app.mainloop()
