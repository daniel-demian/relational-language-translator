from LangFrame import *
from SqlFrame import *
from RaFrame import *
from RkFrame import *
from RaOptimize import *

class ContentFrame:
    def __init__(self, root, frame):
        self.root = root
        self.frame = frame

        #left frame
        self.leftFrame = tk.Frame(self.root, width=300, height=600, borderwidth=1, relief="sunken")
        self.leftFrame.grid(row=0, column=0, padx=10, pady=2)
        self.leftFrame.grid_propagate(0)

        self.btnFrame = tk.Frame(self.leftFrame, width=300, height=600, borderwidth=1)
        self.btnFrame.grid(row=1, column=0, padx=10, pady=2)
        self.btnFrame.rowconfigure(2, weight=1)
        self.btnFrame.rowconfigure(3, weight=1)
        self.btnFrame.rowconfigure(4, weight=1)
        self.btnFrame.rowconfigure(5, weight=1)
        self.btnFrame.rowconfigure(6, weight=1)
        self.btnFrame.rowconfigure(7, weight=1)
        self.btnFrame.grid_propagate(0)

        self.langBtn = tk.Button(self.btnFrame, text="Prirodzeny jazyk", width=30, font=("Arial", 10), command=lambda: self.frameShow(LangFrame))
        self.langBtn.grid(row=2, column=0, padx=10, pady=2)

        self.sqlBtn = tk.Button(self.btnFrame, text="SQL", width=30, font=("Arial", 10), command=lambda: self.frameShow(SqlFrame))
        self.sqlBtn.grid(row=3, column=0, padx=10, pady=2)

        self.raBtn = tk.Button(self.btnFrame, text="Relačna algebra", width=30, font=("Arial", 10), command=lambda: self.frameShow(RaFrame))
        self.raBtn.grid(row=4, column=0, padx=10, pady=2)

        self.raBtn = tk.Button(self.btnFrame, text="Optimalizácia", width=30, font=("Arial", 10), command=lambda: self.frameShow(RaOptimize))
        self.raBtn.grid(row=5, column=0, padx=10, pady=2)

        self.rkBtn = tk.Button(self.btnFrame, text="Relačný Kalkulus", width=30, font=("Arial", 10), command=lambda: self.frameShow(RkFrame))
        self.rkBtn.grid(row=6, column=0, padx=10, pady=2)

        self.exBtn = tk.Button(self.btnFrame, text="Exit", width=30, bg="red", font=("Arial", 10), command=self.exitFunction)
        self.exBtn.grid(row=7, column=0, padx=10, pady=2)


        #right frame
        self.rightFrame = tk.Frame(self.root, width=700, height=600, borderwidth=1, relief="sunken")
        self.rightFrame.grid(row=0, column=1, padx=10, pady=2)
        self.rightFrame.grid_propagate(0)

        self.startPage = tk.Frame(self.rightFrame, width=300, height=600, borderwidth=1)
        self.startPage.grid(row=0, column=0, padx=10, pady=2)

        self.label = tk.Label(self.startPage, text="Prekladač relačných jazykov", font=("Arial", 25))
        self.label.grid(row=2, column=0, padx=10, pady=2)



    def exitFunction(self):
        self.root.destroy()
        exit()

    def frameShow(self, frameClass):
        new_frame = frameClass(self.root, self.rightFrame)
        if self.startPage is not None:
            self.startPage.destroy()
        self.startPage = new_frame
