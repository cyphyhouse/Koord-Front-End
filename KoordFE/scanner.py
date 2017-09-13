from ply import * 


#reserved keywords
RESERVED = {
  "map"  : 'MAP',
  "pass" : "PASS", 
  "agent" : "AGENT",'atomic':'ATOMIC',
  "using" : "USING",
  "module" : "MODULE",
  "sensors" : "SENSORS",
  "actuators" : "ACTUATORS", 
  "String" : "STRING", "int" : "INT", "float" : 'FLOAT', 'boolean': 'BOOLEAN','ItemPosition':'IPOS', #'Stage' : 'STAGE', 
  "allwrite" : "ALLWRITE",
  "allread" : "ALLREAD",
  "local" : "LOCAL",
  "init" : "INIT",
  "if" : 'IF' , 'else' : 'ELSE', "pre" : "PRE", "eff" :"EFF", "true" : 'TRUE', 'false' : 'FALSE' }

#additional required tokens
tokens = [
  'COLON', 'COMMA',
  'AND','OR','NOT',
  'LID', 'CID',
  'INUM','FNUM',
  'LPAR','RPAR', 'LBRACE','RBRACE', #'LCURLY', 'RCURLY',
  'PLUS','MINUS','TIMES','BY',
  'LT','GT','EQ','GEQ','LEQ', 'NEQ',
  'ASGN',
  'WS','NL',
  'INDENT','DEDENT',
]+ list(RESERVED.values())


#integer numbers 
def t_INUM(t):
  r'[-]?[0-9]+'
  t.value = int(t.value)
  return t 

#decimal numbers
def t_FNUM(t):
  r'[-]?[0-9]+([.][0-9]+)?'
  t.value = float(t.value) 
  return t 

#delimiters
t_COLON = r':'
t_COMMA = r','


#arithmetic operators
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_BY = r'/'


#relational operators
t_GT = r'>'
t_LT = r'<'
t_GEQ = r'>='
t_LEQ = r'<='
t_EQ = r'=='
t_NEQ = r'\!='
t_AND = r'\&\&'
t_OR = r'\|\|'
t_NOT = r'\!'
#assignment 
t_ASGN = r'='

#bracketing
t_LBRACE = r'\['
t_RBRACE = r'\]'
#t_LCURLY = r'\{'
#t_RCURLY = r'\}'


#capitalized identifiers
def t_CID(t):
  r'[A-Z][a-zA-Z0-9\.]*'
  t.type = RESERVED.get(t.value,'CID')
  return t 

#lowercase identifiers
def t_LID(t):
  r'[a-z][a-zA-Z0-9\.]*'
  t.type = RESERVED.get(t.value,'LID')
  return t

#comments, start with a #
def t_comment(t): 
  r"[ ]*\#[^\n]*" 
  pass

#whitespace, ignore if not at start of line or if within a paranthesis
def t_WS(t):
  r' [ ]+ '
  if t.lexer.paren_count == 0 and t.lexer.line_start : 
    return t

#newline, ignore if within paranthesis
def t_newline(t): 
  r'\n+'
  t.lexer.lineno += len(t.value)
  t.type = 'NL'
  if t.lexer.paren_count == 0 : 
    return t 

#left parenthesis , increment counter
def t_LPAR(t):
  r'\('
  t.lexer.paren_count += 1
  return t 

#right paranthesis 
#TODO: check for underflow in parser or a separate checker. 
def t_RPAR(t):
  r'\)'
  t.lexer.paren_count -= 1
  return t 

#unrecognized
def t_error(t):
  raise SyntaxError("Unknown symbol %r" %(t.value[0]))
  print("Skipping",repr(t.value[0]))
  t.lexer.skip(1)

#auxiliary function for synthesizing tokens
def _new_token(type,lineno):
  tok = lex.LexToken()
  tok.type = type
  tok.value = None
  tok.lineno = lineno
  tok.lexpos = 0
  return tok 

#generate dedent token
def DEDENT(lineno):
  return _new_token("DEDENT",lineno)

#generate indent token
def INDENT(lineno):
  return _new_token("INDENT",lineno)

#macros 
NO_INDENT = 0
MAY_INDENT = 1
MUST_INDENT = 2


#implementing a white space filter which makes sure to ignore white spaces which are not at the start of a line
def ws_filter(lexer,tokens):
  lexer.line_start = line_start = True 
  indent = NO_INDENT
  saw_colon = False


  for token in tokens:
    token.line_start = line_start

    #if a colon is seen, the next line may be indented if a complex statement, not indented if simple statement 
    if token.type == 'COLON':
      line_start = False
      indent = MAY_INDENT
      token.must_indent = False 
    
    #if a new line is seen, if it saw a colon before, then it must indent . otherwise ignore. 
    elif token.type == "NL":
      line_start = True 
      if indent == MAY_INDENT:
        indent = MUST_INDENT
      token.must_indent = False 

    #white spaces must be at the start of a line. 
    elif token.type == 'WS':
      assert token.line_start == True 
      line_start = True 
      token.must_indent = False


    else: 
      if indent == MUST_INDENT:
        token.must_indent = True
      else: 
        token.must_indent = False
      line_start = False
      indent = NO_INDENT

    yield token
    lexer.line_start = line_start

#see gardensnake.py in the ply distribution for documentation on this. copied almost line by line. 

def indent_filter(tokens): 
  levels = [0]
  token = None
  depth = 0 
  prev_ws = False 

  for token in tokens: 
    if token.type == 'WS':
      assert depth == 0

      depth = len(token.value)
      prev_ws = True 

      continue

    if token.type == 'NL':
      depth = 0
      if prev_ws or token.line_start:
        continue
      yield token
      continue  
     
    prev_ws = False
    if token.must_indent:
      if not(depth > levels[-1]):
        raise IndentationError("expected an indented block at line %r" %(token.lineno))
      levels.append(depth)
      yield INDENT(token.lineno)

    elif token.line_start: 
      if depth == levels[-1]:  
        pass 
      elif depth > levels[-1]:
        raise IndentationError("indentation increase but not in new block")
      else: 
        try:
          i = levels.index(depth)
        except ValueError:
          raise IndentationError("inconsistent indentation")
        for _ in range(i+1,len(levels)):
          yield DEDENT(token.lineno)
          levels.pop()
    yield token

  if len(levels) > 1 :
    assert token is not None 
    for _ in range(1, len(levels)):
      yield DEDENT(token.lineno)      

#final filter. may need an endmarker.         

def filter(lexer):
  token = None 
  tokens = iter(lexer.token,None)
  tokens = ws_filter(lexer,tokens)
  for token in indent_filter(tokens):
    yield token

class IndentLexer(object):
  def __init__(self):
    self.lexer = lex.lex()
    self.token_stream = None


  def input(self,s):
    self.lexer.paren_count = 0
    self.lexer.input(s)
    self.token_stream = filter(self.lexer)


  def token(self):
    try:
      #print(self.lexer.paren_count)
      return self.token_stream.next()
    except StopIteration: 
      return None 

#create a lexer. 
lexer = IndentLexer()
'''
#test
s = raw_input("Enter filename\n:")
lexer.input(open(s).read())
while True :
   tok = lexer.token()
   if not tok:
     break
   else: 
     print(tok)
'''
