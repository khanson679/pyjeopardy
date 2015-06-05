"""
tkgui.py
Tkinter GUI classes for PyJeopardy
By Kenneth Hanson
"""

from __future__ import print_function
import csv
import itertools

import Tkinter as tk
import ttk
import tkMessageBox
import tkFileDialog 

from lib import *


def run_gui(board):
    """Start GUI with PyJeopardy game board."""
    root = tk.Tk()
    root.title("PyJeopardy")
    
    main_frame = MainFrame(board)
    
    root.mainloop()


class MainFrame(ttk.Frame):
    def __init__(self, board=None, master=None):
        ttk.Frame.__init__(self, master)
        self._board = board
        
        # place frame in the root window and make resizable
        self.master.geometry('640x480')
        self.pack(fill=tk.BOTH, expand=1)
        
        # make menu
        self._menubar = Menubar(self)
        self.master.config(menu=self._menubar) # attach to window
        
        # make question grid
        self._question_grid = QuestionGrid(self)
        if board != None:
            self._question_grid.init_widgets(board)
        self._question_grid.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        
        # make status bar
        self._status = StatusBar(self.master)
        self._status.pack(side=tk.BOTTOM, fill=tk.X)
        self._status.set("Started PyJeopardy.")

        # Font for buttons and labels
        self._style = ttk.Style()
        # self._style.theme_use("default")
        self._style.configure(".", font=("Helvetica", 12))

    def init_question_grid(self, infilename):
        try:
            successful = self._board.input_items(infilename)
        except IOError as err:
            tkMessageBox.showerror(
                message="Unable to open file: " + infilename)
            raise err
        except csv.Error as err:
            tkMessageBox.showerror(
                message="Unable to parse file: " + infilename)
            raise err
        else:
            self._question_grid.init_widgets(self._board)          


class Menubar(tk.Menu):
    def __init__(self, master=None):
        tk.Menu.__init__(self, master, relief=tk.FLAT)
        
        # File menu
        filemenu = tk.Menu(self, tearoff=0)
        filemenu.add_command(label="Open Question File", command=self._on_open)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self._on_quit)
        self.add_cascade(label="File", menu=filemenu)

        # Mode menu
        self.game_mode = tk.IntVar()
        self.game_mode.set(1)
        modemenu = tk.Menu(self, tearoff=0)
        modemenu.add_radiobutton(label="Mode1",
                                 variable=self.game_mode, value=1)
        modemenu.add_radiobutton(label="Mode2",
                                 variable=self.game_mode, value=2)
        self.add_cascade(label="Mode", menu=modemenu)

        # Help menu
        helpmenu = tk.Menu(self, tearoff=0)
        helpmenu.add_command(label="About", command=self._on_about)
        self.add_cascade(label="Help", menu=helpmenu)

    def _on_about(self):
        tkMessageBox.showinfo(title="About PyJeopardy",
        message="""This is PyJeopardy version {} \
                   by Kenneth Hanson""".format(__version__))

    def _on_open(self):
        infilename = tkFileDialog.askopenfilename()
        if infilename != "":
            self.master.init_question_grid(infilename)
        
    def _on_quit(self):
        raise NotImplementedError()
        
        
class QuestionGrid(ttk.Frame):
    """
    Grid of category of labels and question buttons laid out as follows:
        CatA    CatB    CatC    ...
        Q A1    Q B1    Q C1
        Q A2    Q B2    Q C2
        Q A2    Q B2    Q C2
        ...
    """
    
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        
        self.labels = []
        self.buttons = []

        # self.style = ttk.Style().configure("TButton", borderwidth=5, margin=50)
        
    def init_widgets(self, board):
        """Build new quiz item grid, removing all existing items."""
        
        # clear existing board
        for widget in itertools.chain(self.labels, self.buttons):
            widget.destroy()
        del self.labels[:]
        del self.buttons[:]

        # create new category labels and quiz item buttons
        for i, cat in enumerate(board.items):
            new_label = ttk.Label(self, text=cat)
            new_label.grid(row=0,column=i)
            self.labels.append(new_label)
            for j, item in enumerate(board.items[cat]):
                new_button = ttk.Button(self, text=str(item.value),
                                        command=lambda: self._on_button(item))
                new_button.grid(row=j+1, column=i, sticky=tk.N+tk.S+tk.E+tk.W)
                self.buttons.append(new_button)
        
        # make grid resizable
        n_columns, n_rows = self.grid_size()
        for c in xrange(n_columns):
            self.columnconfigure(c, weight=1)
        for r in xrange(n_rows):
            self.rowconfigure(r, weight=1)
    
    def _on_button(self, quizitem):
        """Display quiz item."""
        tkMessageBox.showinfo(message=quizitem.pformat())


class StatusBar(ttk.Frame):
    """
    Based on <http://effbot.org/tkinterbook/tkinter-application-windows.htm>.
    """
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.label = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.label.pack(fill=tk.X)

    def set(self, msg):
        self.label.config(text=msg)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()
