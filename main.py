import sys

#from lexer import lexer

from Project1 import lexmemes
from ParserP2 import program

if len(sys.argv) < 2:
    print("Please Specify a File")
    sys.exit(0)

try:
    x = program(lexmemes)
    x.analyze()
    print("ACCEPT")
except Exception as e:
    # raise e
    print("REJECT")

