#!/usr/bin/env python

"""
pyjeopardy.py
Main script for PyJeopardy
By Kenneth Hanson
"""

from __future__ import print_function
import sys
import cmd

from lib import *
import logic
import tkgui as gui

__version__ = "0.1.0"


#
# In-program CLI
#

class CLI(cmd.Cmd):
    """Play game without GUI for testing purposes."""
    
    prompt = "<cmd> "
    intro = "Started PyJeopardy CLI. Enter 'help' for commands."
    
    def __init__(self, board):
        cmd.Cmd.__init__(self)
        self.board = board
    
    def do_EOF(self, line):
        """Quit program."""
        return True
        
    def do_gui(self, line):
        """Start GUI and hand over control."""
        print("Starting GUI. Close it to continue using the CLI.")
        run_gui(self.board)
    
    def do_init_players(self, playernames):
        """Usage: init players [name]+"""
        self.board.init_players(' '.split(playernames))
        
    def do_open(self, infilename):
        """Open quiz item database."""
        self.board.input_items(infilename)
        
    def do_print(self, dataname):
        """Usage: print [data name]
        Printable data: all items players
        """
        func = {'all':     lambda: print(board),
                'items':   lambda: pprint(board.items_as_list()),
                'players': lambda: pprint(board.players_as_list())
               }.get(dataname)
        if func is None:
            print("Unknown data item.")
        else:
            func()
        
    def do_quit(self, line):
        """Quit program."""
        return True
        

#
# Main script
#

if __name__ == '__main__':
    debug("*****Starting as script.*****")
    
    # process command line args
    infilename = None
    if len(sys.argv) == 2:
        infilename = sys.argv[1]
    elif len(sys.argv) > 2:
        print("Usage: python pyjeopardy.py CSVFILE")
        sys.exit(1) 
    
    # initialize game data
    board = logic.GameBoard(infilename)
    
    # run CLI
    #cli = CLI(board)
    #cli.cmdloop()
    
    gui.run_gui(board)
    
    debug("*****Program ended normally.*****")
    sys.exit(0)
