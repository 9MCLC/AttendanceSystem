import tkinter as tk
from lobby import Lobby
from registration import Registration
from namelist import NameList

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Application")

        self.button1 = tk.Button(root, text="Lobby", command=self.open_window1)
        self.button1.pack()
        
        self.button2 = tk.Button(root, text="Registration", command=self.open_window2)
        self.button2.pack()

        self.button3 = tk.Button(root, text="NameList", command=self.open_window3)
        self.button3.pack()

    def open_window1(self):
        self.new_window = tk.Toplevel(self.root)
        self.app = Lobby(self.new_window)

    def open_window2(self):
        self.new_window = tk.Toplevel(self.root)
        self.app = Registration(self.new_window)

    def open_window3(self):
        self.new_window = tk.Toplevel(self.root)
        self.app = NameList(self.new_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
