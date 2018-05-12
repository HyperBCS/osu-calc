import Tkinter
import ttk
import calc


def calculate_pp():
    global map_link, c100, c50, miss, combo
    Tkinter.Label(root, text=calc.return_values(int(c100.get()),
                                                int(c50.get()),
                                                int(miss.get()),
                                                int(combo.get()),
                                                filename)).grid(row=6, column=0, columnspan=2)

while True:
    root = Tkinter.Tk()
    root.resizable(width=False, height=False)
    root.title("osu-calc")

    Tkinter.Label(root, text="Map link:").grid(row=0, column=0)
    Tkinter.Label(root, text="Amount of 100s:").grid(row=1, column=0)
    Tkinter.Label(root, text="Amount of 50s:").grid(row=2, column=0)
    Tkinter.Label(root, text="Amount of misses:").grid(row=3, column=0)
    Tkinter.Label(root, text="Combo:").grid(row=4, column=0)

    map_link = Tkinter.Entry(root)
    map_link.grid(row=0, column=1)

    c100 = Tkinter.Entry(root)
    c100.grid(row=1, column=1)

    c50 = Tkinter.Entry(root)
    map_link.grid(row=2, column=1)

    miss = Tkinter.Entry(root)
    miss.grid(row=3, column=1)

    combo = Tkinter.Entry(root)
    combo.grid(row=4, column=1)

    Tkinter.Button(root, fg="blue", text="Calculate pp!").grid(row=5, column=0, columnspan=2)

    root.mainloop()