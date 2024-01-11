from argparse import ArgumentParser
import re
from pprint import pprint

parser = ArgumentParser()
parser.add_argument("--file")

args = parser.parse_args()
# print(args.file)

class Ast:
  def __init__(self, kind, arguments):
    self.kind = kind
    self.arguments = arguments
    self.children = []

  def __repr__(self):
    return "{} {}".format(self.kind, self.arguments)

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
    self.return_type = []
    self.types = {
      "int": {},
      "void": {},
      "char": {}
    }

  def getchar(self):
    if self.pos + 1 >= len(self.program):
      self.end = True
      return self.last_char
    self.last_char = self.program[self.pos]
    self.pos = self.pos + 1
    # print(self.last_char)
    return self.last_char

  def peek(self, amount):
    if self.pos + amount >= len(self.program):
      self.end = True
      return self.last_char
    peeked = self.program[self.pos + amount]
    return peeked

  def gettoken(self):
    token = self.gettoken_inner() 
    self.last_token = token
    return token

  def peektoken(self):
    origpos = self.pos
    origlast_char = self.last_char
    token = self.gettoken()
    self.pos = origpos
    self.last_char = origlast_char
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
      # print("found slash")
      self.last_char = self.getchar()
      # print(self.last_char)
      if self.last_char == "*":
        # print("found asterisk")
        comment = ""
        self.last_char = self.getchar()
        comment += self.last_char
        # print("found char" + comment)
        # print("peeked" + self.peek(1))
        # print(not self.end, self.last_char == "*" and self.peek(2) == "/")
        while not self.end and not (self.last_char == "*" and (self.peek(0) == "/")):
          self.last_char = self.getchar()
          if self.last_char == "*" and self.peek(2) == "/":
            break
          comment += self.last_char
          # print("multi peeked" + self.peek(1))
        self.getchar() # consume the /
        self.type = "comment"
        self.comment = comment
        return comment
      elif self.last_char == "/":
        comment = ""
        self.last_char = self.getchar()
        comment += self.last_char
        while not self.end and self.last_char != "\n":
          # print("found char for slash coment")
          self.last_char = self.getchar()
          comment += self.last_char
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

    # print("unknown character: [{}]".format(self.last_char))

  def parse_struct(self):
    pass  

  def parse_function(self):
    finding = True
    token = self.gettoken() 
    if token == "asterisk":  
      self.return_type.append(Ast("pointer", {}))
      # print("is a pointer {}".format(self.return_type)) 
      name = self.gettoken() 
    elif token in self.types:
      print("known type")
      self.return_type.append(Ast("type", {"name": token}))
      name = self.gettoken()
    else:
      name = token
    name_or_type = Ast("name", {"name": name})
    self.return_type.append(name_or_type)
    determiner = self.gettoken()
    # print("determiner - {}".format(determiner))
    if determiner == "opencurly" and self.return_type[0].kind == "struct":
      print("Found struct definition")
      struct = self.return_type[0] 
      while not self.end and self.peek(1) != "}":
        self.return_type = []
        token = self.gettoken()
        if token in self.types: 
          self.return_type.append(Ast("type", {"name": token}))
        elif token == "struct":
          self.return_type.append(Ast("struct", {}))
        self.parse_function()
        struct.children.append(self.return_type)
      pprint("end of struct")
      pprint(struct.children)
       


    elif determiner == "openbracket":
      print("Found function, return type: {}".format(self.return_type))
    else:
      while finding:
        print("determiner", determiner)
        if determiner == "stop":
          print("end of line");
          finding = False
        elif determiner == "opensquare":
          size = self.gettoken()  
          if size.isdigit():
            self.return_type.append(Ast("array", {"size": size}))
            close = self.gettoken()
            print("close", close)
            if close == "closesquare":
              print("end of array")
              finding = False
          else:
            constant = size
            self.return_type.append(Ast("array-constant", {"constant": constant}))
            close = self.gettoken() 
            if close == "closesquare":
              print("end of array")
              finding = False
        elif determiner == "asterisk":
          self.return_type.append(Ast("pointer", {}))
          determiner = self.gettoken()
        elif determiner == "semicolon":
          print("end of declaration")
          finding = False
        else:
          # name
          name_or_type.kind = "type"
          self.return_type.append(Ast("name", {"name": determiner}))
          finding = False
        print("type declaration: {}".format(self.return_type))

    nexttoken = self.peektoken()
    print("peeked token", nexttoken)
    if nexttoken == "semicolon":
      self.gettoken()
      print("EXPECTED WAS ", nexttoken)
    return self.return_type

  def parse(self):
    ast = []
    while not self.end:
      token = self.gettoken()
      print("token", token)
      if token == "struct":
        self.return_type = [Ast("struct", {})]
        self.parse_function()
        print(self.return_type)
        
      if token in self.types:
        self.return_type = [Ast("type", {"name": token})]
        self.parse_function()
              
      if self.type == "comment":
        ast.append(Comment(self.comment)) 
      if token == "hash":
        include = self.gettoken()
        if include == "define":
          definevar = self.gettoken()
          value = self.gettoken()
          print("Found define {} = {}".format(definevar, value))
        if include == "include": 
          lessthan = self.gettoken()
          print("include", lessthan)
          newlocation = ""
          importlocation = ""
          if lessthan == "quote":
            while not self.end and self.peek(1) != "\"":
              newlocation = self.gettoken()
              if newlocation == "divide":
                importlocation += "/"
              else:
                importlocation += newlocation
            print(importlocation)
            stop = self.gettoken()
            if stop == "stop":
              extension = self.gettoken()
              if extension == "h":
                endofimport = self.gettoken()
                if endofimport == "quote":
                  print("Found import #include \"{}.h\"".format(importlocation))

          if lessthan == "lessthan":
            newlocation = ""
            importlocation = self.gettoken()
            while not self.end and self.peek(1) != ">":
              newlocation = self.gettoken()
              if newlocation == "divide":
                importlocation += "/"
              else:
                importlocation += newlocation
              
            print(importlocation)
            stop = self.gettoken()
            if stop == "stop":
              extension = self.gettoken()
              if extension == "h":
                greaterthan = self.gettoken()
                if greaterthan == "greaterthan":
                  print("Found import #include <{}.h>".format(importlocation))

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

