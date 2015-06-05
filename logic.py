"""
logic.py
Game logic classes for PyJeopardy
By Kenneth Hanson
"""

from __future__ import print_function
import csv
from collections import OrderedDict
from pprint import pprint, pformat

from lib import *

FIELDNAMES = ("Category", "Value", "Question", "Answer")


class QuizItem(object):
    def __init__(self, category, value, question, answer):
        assert isinstance(category, str)
        assert isinstance(value, int)
        assert isinstance(question, str)
        assert isinstance(answer, str)
        self.category = category
        self.value = value
        self.question = question
        self.answer = answer
   
    def __repr__(self):
        # return "QuizItem({}, {}, {}, {})".format(self.category, self.value,
            # repr(self.question), repr(self.answer))
        return "QuizItem({}, {}, {}, {})".format(
            repr(trunc(self.category, 10)), self.value,
            repr(trunc(self.question, 20)), repr(trunc(self.answer, 20)))
        
    def __str__(self):
        return "<QuizItem>" + \
            "\n\tCat/Val:  '{}' for {}".format(self.category, self.value) + \
            "\n\tQuestion: " + self.question + \
            "\n\tAnswer:   " + self.answer

    def pformat(self):
        return "<QuizItem: '{}' for {}>".format(self.category, self.value) + \
            "\nQuestion: " + self.question + \
            "\nAnswer:   " + self.answer
            

        
class PlayerRecord(object):
    def __init__(self, name):
        self.name = name
        
        self.anwered_questions = []
    
    def __repr__(self):
        return "PlayerRecord({})".format(repr(self.name))
        
        
class GameBoard(object):
    def __init__(self, infilename=None, playernames=None):
        # dictionary of category names to lists of quiz items
        self.items = OrderedDict() 
        if infilename is not None:
            self.input_items(infilename)
            
        # dictionary of player names to records
        self.players = OrderedDict() 
        if playernames is not None:
            self.init_players(playernames)
        
    def __repr__(self):
        return "GameBoard({}, {})".format(repr(self.items), repr(self.players))
        
    def __str__(self):
        return "<GameBoard>\nItems:\n{}\nplayers:\n{}".format(
            pformat(self.items_as_list()), pformat(self.players_as_list()))
        
    def pformat(self):
        return "<GameBoard>\nItems:\n{}\nplayers:\n{}".format(
            '\n'.join(map(str, self.items_as_list())),
            pformat(self.players_as_list()))
    
    def items_as_list(self):
        return [item for cat in self.items.itervalues() for item in cat]
    
    def _add_item(self, item):
        if not item.category in self.items:
            self.items[item.category] = []
        self.items[item.category].append(item)
    
    # def get_item(self, index):
        # try:
            # return self.items_as_list()[index]
        # except IndexError:
            # return None
    
    def input_items(self, infilename):
        """Open given CSV file name and load contents.
        Replaces any previous data.

        Exceptions passed up:
        --IOError:   if unable to read file
        --csv.Error: if unable to parse file
        """
        log("Reading question file '{}'...".format(infilename))
        with open(infilename) as csvfile:
            reader = csv.DictReader(csvfile, dialect='excel')
            
            # enforce column headers
            if set(reader.fieldnames) != set(FIELDNAMES):
                raise csv.Error("Column headers must be exactly '{}'".format(
                        ','.join(FIELDNAMES)))
            
            self.items.clear()

            # build database
            for row in reader:
                cat = str(row['Category'])
                val = int(row['Value'])
                q =   str(row['Question'])
                a =   str(row['Answer'])
                self._add_item(QuizItem(cat, val, q, a))      
        log("Input successful.")
    
    def players_as_list(self):
        return self.players.items()
        
    def init_players(self, playernames):
        debug(playernames)
        self.players.clear()
        for name in playernames:
            self.players[name] = PlayerRecord(name)
        debug(self.players_as_list())