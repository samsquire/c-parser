from argparse import ArgumentParser
import re

parser = ArgumentParser()
parser.add_argument("--file")

args = parser.parse_args()
print(args.file)

class Parser():
  def __init__(self, program):
    self.pos = 0
    self.last_char = " "
    self.program = program
    self.regex = re.compile("[a-zA-Z0-9_]")
    self.end = False
    self.identifier = ""

  def getchar(self):
    if self.pos + 1 > len(self.program):
      self.end = True
      return self.last_char
    self.last_char = self.program[self.pos]
    self.pos = self.pos + 1
    print(self.last_char)
    return self.last_char

  def gettoken(self):
    self.type = "token" 
    while not self.end and (self.last_char == " " or self.last_char == "\n" or self.last_char == "\t"):
      self.last_char = self.getchar()
    if self.last_char == "{": 
      self.last_char = self.getchar()
      return "opencurly"
    if self.last_char == "}": 
      self.last_char = self.getchar()
      return "closecurly"
    if self.last_char == "(": 
      self.last_char = self.getchar()
      return "openbracket"
    if self.last_char == ")": 
      self.last_char = self.getchar()
      return "closebracket"
    if self.last_char == "-":
      self.last_char = self.getchar()
      return "minus"
    if self.last_char == ">":
      self.last_char = self.getchar()
      return "greaterthan"
    if self.last_char == "<":
      self.last_char = self.getchar()
      return "lessthan"
    if self.last_char == "*":
      self.last_char = self.getchar()
      return "asterisk"
    if self.last_char == "/": 
      self.last_char = self.getchar()
      return "divide"
    if self.last_char == "&": 
      self.last_char = self.getchar()
      return "amper"
    if self.last_char == ";": 
      self.last_char = self.getchar()
      return "semicolon"
    if self.last_char == ":": 
      self.last_char = self.getchar()
      return "colon"
    if self.last_char == ",": 
      self.last_char = self.getchar()
      return "comma"
    if self.last_char == ".": 
      self.last_char = self.getchar()
      return "stop"
    if self.last_char == "\"": 
      self.last_char = self.getchar()
      return "quote"
    if self.last_char == "|": 
      self.last_char = self.getchar()
      return "pipe"
    if self.last_char == "[": 
      self.last_char = self.getchar()
      return "opensquare"
    if self.last_char == "]": 
      self.last_char = self.getchar()
      return "closesquare"
    if self.last_char == "=": 
      self.last_char = self.getchar()
      return "equals"
    if self.last_char == "+": 
      self.last_char = self.getchar()
      return "plus"
    if self.last_char == "%": 
      self.last_char = self.getchar()
      return "percent"
    if self.last_char == "\\": 
      self.last_char = self.getchar()
      return "backslash"
    if self.last_char == "'": 
      self.last_char = self.getchar()
      return "singlequote"
    if self.last_char == "^": 
      self.last_char = self.getchar()
      return "caret"
    if self.last_char == "$": 
      self.last_char = self.getchar()
      return "dollar"
    if self.last_char == "!": 
      self.last_char = self.getchar()
      return "exclamation"

    if self.last_char == "#":
      self.last_char = self.getchar()
      return "hash"

    if self.regex.match(self.last_char):
      self.identifier = self.last_char
      while not self.end and self.regex.match(self.last_char):
        self.last_char = self.getchar()
        self.identifier = self.identifier + self.last_char 
      if self.end:
        self.identifier = self.identifier + self.last_char 
        
      return self.identifier

    print("unknown character: [{}]".format(self.last_char))

  def parse(self):
    while not self.end:
      print(self.gettoken())
    return None 
    
  
filedata = open(args.file).read()
codeparser = Parser(filedata)
print(codeparser.parse())

