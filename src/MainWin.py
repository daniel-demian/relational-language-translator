from ContentFrame import *

class MainWin:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Prekladac")
        self.root.config(background="white")

        self.frame = tk.Frame(self.root, width=1000, height=600, borderwidth=1, relief="sunken")
        self.frame.grid_propagate(0)

        self.content = ContentFrame(self.root, self.frame)

    def start(self):
        self.root.mainloop()
