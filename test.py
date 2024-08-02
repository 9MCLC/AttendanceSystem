import tkinter as tk
from playsound import playsound

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Application")

        self.button1 = tk.Button(root, text="Lobby", command=self.open_window1)
        self.button1.pack()

    def open_window1(self):
        playsound("C:/Users/yewho/Downloads/success.mp3")
        


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
