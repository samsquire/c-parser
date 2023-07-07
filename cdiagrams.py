from argparse import ArgumentParser
import re

parser = ArgumentParser()
parser.add_argument("--file")

args = parser.parse_args()
print(args.file)

class Comment:
  def __init__(self, comment):
    self.comment = comment
  def __repr__(self):
    return "/* {} */".format(self.comment)

class Parser():
  def __init__(self, program):
    self.pos = 0
    self.program = program
    self.last_char = self.getchar()
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

  def peek(self, amount):
    if self.pos + amount > len(self.program):
      self.end = True
      return self.last_char
    peeked = self.program[self.pos + amount]
    return peeked

  def gettoken(self):
    token = self.gettoken_inner() 
    self.last_token = token
    return token

  def gettoken_inner(self):
    self.type = "token" 
    while not self.end and (self.last_char == " " or self.last_char == "\n" or self.last_char == "\t"):
      self.last_char = self.getchar()
    self.symbol = self.last_char


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
      print("found slash")
      self.last_char = self.getchar()
      if self.last_char == "*":
        print("found asterisk")
        comment = ""
        self.last_char = self.getchar()
        comment += self.last_char
        print("found char" + comment)
        print("peeked" + self.peek(1))
        print(not self.end, self.last_char != "*", not self.peek(1) == "/")
        while not self.end and self.last_char != "*" and not (self.peek(1) == "/"):
          print("found char for coment")
          self.last_char = self.getchar()
          comment += self.last_char
        self.getchar() # consume the /
        self.type = "comment"
        self.comment = comment
        return comment
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
      self.type = "identifier"
      self.identifier = ""
      while not self.end and self.regex.match(self.last_char):
        self.identifier = self.identifier + self.last_char 
        self.last_char = self.getchar()
      if self.end:
        self.identifier = self.identifier + self.last_char 
        
      return self.identifier

    print("unknown character: [{}]".format(self.last_char))



  def parse(self):
    ast = []
    while not self.end:
      token = self.gettoken()
      if self.type == "comment":
        ast.append(Comment(self.comment)) 
      # token = self.gettoken()
      # if token == "asterisk":
      #   comment = ""
      #   while not self.end:
      #     token = self.gettoken()
      #   
      #     if token == "asterisk":
      #       token = self.gettoken()
      #       if token == "divide":
      #         ast.append(Comment(comment)) 
      #         break 
      #       else:
      #         if self.type == "identifier":
      #           comment += token + " "
      #         else:
      #           comment += self.symbol + " "
      #     else:
      #       if self.type == "identifier":
      #         comment += token + " "
      #       else:
      #         comment += self.symbol + " "
            
      
    return ast
    
  
filedata = open(args.file).read()
codeparser = Parser(filedata)
print(codeparser.parse())

