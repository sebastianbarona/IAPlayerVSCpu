from functools import partial
import tkinter as tk



class MainFrame(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        b=""
        for r in range(10): 
            for c in range(9,-1,-1):
                new_button = tk.Button(self, text= str(b), borderwidth = 1, height=3, width=5)
                print(r,c)
                new_button.grid(row=r, column=c)
                new_button["command"] = partial(self.press, new_button, r, c)                 
                b = f'({r}, {c})' 
                



                #print("0 1 2 3 4 5 6 7 8 9")
    def press(self, btn, row ,col):
        print(row, col) 
        btn.configure(bg="gold")
        btn.configure(activebackground="gold")


if __name__ == "__main__":
    root = tk.Tk()
    MainFrame(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
                                                                                              