"""
lib.py
Auxiliary functions for PyJeopardy
By Kenneth Hanson
"""

def log(msg):
    print(msg)

def debug(obj):
    print(obj)

def error(ex):
    print(ex)

def trunc(string, maxlen):
    return string[:maxlen-3] + "..." if len(string) > maxlen else string