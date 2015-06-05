#!/usr/bin/env python

import Tkinter as tk

parent = tk.Tk()

menubar = tk.Menu(parent, relief=tk.FLAT)
show_all = tk.IntVar()
show_all.set(1)

view_menu = tk.Menu(menubar)
view_menu.add_radiobutton(label="Show All", value=1, variable=show_all)
view_menu.add_radiobutton(label="Show Done", value=2, variable=show_all)
view_menu.add_radiobutton(label="Show Not Done", value=3, variable=show_all)
menubar.add_cascade(label='View', menu=view_menu)
parent.config(menu=menubar)

parent.mainloop()