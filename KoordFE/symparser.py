#!/usr/bin/python

import sys
from scanner import * 
from ast import * 

def p_program(p):
    '''program : agent modules awdecls ardecls locdecls stagedecl init events Numdecl'''
    p[0] = (p[3]+p[4]+p[5]+[declAst('int','pid'),declAst('int','numBots',p[9])],p[9])
    

def p_Numdecl(p):
    '''Numdecl : NUM INUM NL'''
    p[0] = p[2] 


def p_stagedecl(p):
    '''stagedecl : DEF STAGE LCURLY stagelist RCURLY NL
                 | empty  
    '''
    p[0] = []

def p_stagelist(p):
    '''stagelist : LID COMMA stagelist
                 | LID 
    '''
    p[0] = [] 



def p_agent(p):
    '''agent : AGENT CID NL'''
    p[0] = []


def p_modules(p):
    '''modules : module modules 
               | empty 
    '''
    pass
def p_module(p):
    '''module : USING MODULE CID COLON NL INDENT actuatordecls sensordecls DEDENT'''
    pass
def p_actuatordecls(p):
    '''actuatordecls : ACTUATORS COLON NL INDENT decls DEDENT 
                     | empty
    '''
    if len(p) > 2 :
      p[0] = p[5]
    else :
      p[0] = []

def p_sensordecls(p):
    '''sensordecls : SENSORS COLON NL INDENT decls DEDENT 
                     | empty
    '''
    if len(p) > 2 :
      p[0] = p[5]
    else :
      p[0] = []

def p_awdecls(p):
    '''awdecls : ALLWRITE COLON NL INDENT decls DEDENT
               | empty
    ''' 
    if len(p) > 2:
      for decl in p[5]:
          decl.set_scope(MULTI_WRITER)
      p[0] = p[5]
    else:
      p[0] = []

def p_ardecls(p):
    '''ardecls : ALLREAD COLON NL INDENT rvdecls DEDENT
               | empty
    '''
    if len(p) > 2: 
      for decl in p[5]:
          decl.set_scope(MULTI_READER)
      p[0] = p[5]
    else:
      p[0] = [] 

def p_locdecls(p):
    '''locdecls : LOCAL COLON NL INDENT decls DEDENT
               | empty
    '''
    if len(p) > 2: 
      p[0] = p[5]
    else:
      p[0] = []

def p_decls(p):
    '''decls : decl decls 
            | empty
    '''
    dlist = []
    if len(p) == 3:
      dlist.append(p[1])
      dlist+= p[2]
    p[0] = dlist

def p_decl(p):
    '''decl : type varname ASGN exp NL
            |  type varname NL 
    '''
    if len(p) == 4: 
      p[0] = (declAst(p[1],p[2]))
    else:
      p[0] = (declAst(p[1],p[2],p[4]))

def p_rvdecls(p):
    '''rvdecls : rvdecl rvdecls 
               | empty
    '''
    dlist = []
    if len(p) == 3:
      dlist.append(p[1])
      dlist+= p[2]
    p[0] = dlist
    

def p_rvdecl(p) :
    '''rvdecl : type varname LBRACE owner RBRACE NL 
    '''
    p[0] = (rvdeclAst(p[1],p[2],p[4]))

def p_owner(p) : 
      '''owner : TIMES 
               | INUM'''
      p[0] = p[1]

def p_funccall(p):
    '''funccall : varname LPAR args RPAR'''
    p[0] = [] 

def p_args(p):
    '''args : neargs 
            | noargs
    '''
    p[0] = p[1]

def p_noargs(p):
    '''noargs : empty'''
    p[0] = []

def p_neargs(p):
    '''neargs : exp 
              | exp COMMA neargs
    '''
    alist = []
    alist.append(p[1])
    if len(p) > 2:
       alist+= p[3]
    p[0] = alist

       

def p_type(p):
    '''type : INT
            | STRING 
            | FLOAT
            | IPOS
            | BOOLEAN 
    '''
    p[0] = p[1]

    #print(p[0])

def p_init(p):
    '''init : INIT COLON NL INDENT stmts DEDENT
            | empty
    '''
    p[0] = []


def p_events(p):
    '''events : event events
              | empty '''
    elist = [] 
    p[0] = elist  

def p_event(p):
    '''event : LID COLON NL INDENT PRE COLON cond NL effblock DEDENT
             | LID COLON NL INDENT PRE COLON CID NL effblock DEDENT 
    '''
    p[0] = []

def p_effblock(p):
    '''effblock : EFF COLON NL INDENT stmts DEDENT 
                | EFF COLON stmt 
    '''
    p[0] = []

def p_cond(p):
    '''cond :  LPAR cond AND cond RPAR 
            | LPAR cond OR cond RPAR
            | LPAR cond op cond RPAR
            | LPAR NOT cond RPAR
            | LPAR cond RPAR
            | exp
    '''
    p[0] = []

def p_stmts(p):
    '''stmts : stmt stmts
             | empty'''
    slist = []
    p[0] = slist

def p_stmt(p):
    '''stmt : asgn 
            | wptstmt
            | EXIT NL 
            | funccall NL
            | modulefunccall NL
            | ATOMIC COLON NL INDENT stmts DEDENT 
            | IF cond COLON NL INDENT stmts DEDENT elseblock
    '''
    p[0] = [] 

def p_modulefunccall(p):
    '''modulefunccall : CID LPAR args RPAR '''
    p[0] = [] 

def p_elseblock(p):
    '''elseblock : ELSE COLON NL INDENT stmts DEDENT
                 | empty   
    '''
    p[0] = []

def p_asgn(p):
    '''asgn : varname ASGN exp NL
    '''
    #print(asgnAst(p[1],p[3]))
    p[0] = []
      
def p_wptstmt(p):
    '''wptstmt : varname ASGN GETINPUT LPAR RPAR NL'''
    p[0] = []

precedence = (('left','PLUS','MINUS'),
              ('left','TIMES','BY'))

def p_exp(p):
    '''exp : bracketexp 
           | exp PLUS exp 
           | exp TIMES exp
           | exp MINUS exp 
           | exp BY exp
           | varname
           | varname LBRACE exp RBRACE 
           | bval
           | PID
           | num
           | null
           | moduleflag
           | funccall
           | modulefunccall
    '''
    
    p[0] = []

def p_bracketexp(p):
    '''bracketexp : LPAR exp RPAR '''
    p[0] = []
def p_moduleflag(p):
    '''moduleflag : CID '''
    p[0] = []
   
def p_bval(p):
    '''bval : TRUE 
           | FALSE
    '''
    p[0] = []

def p_num(p):
    '''num : INUM 
           | FNUM
    '''
    p[0] = []

def p_varname(p):
    '''varname : LID
               | STAGE 
    '''     
    p[0] = p[1]
def p_null(p):
    '''null : NULL 
    '''     
    p[0] = [] 

def p_op(p):
    '''op : EQ 
          | NEQ 
          | GEQ
          | LEQ
          | GT
          | LT
    '''
    p[0] = []
 
def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print("syntax error in input on line ",p.lineno,p.type)



class symparser(object):
    def __init__(self,lexer=None):
        self.lexer = IndentLexer()
        self.parser = yacc.yacc()


    def parse(self,code):
        self.lexer.input(code)
        result = self.parser.parse(lexer=self.lexer)
        return result

class symcompiler(object):
    def __init__(self):
        self.parser = symparser()

    def compile(self,filename):
        code = open(filename,"r").read()
        decltab,numBots = (self.parser.parse(code))
        symtab = []
        for entry in decltab:
            symtab.append(mkEntry(entry))
        s = ""
        for item in symtab:
          s+= str(item)+"\n"
        return s
	#appname = "testAdd"
        #print(pgm.name)
'''
filename = sys.argv[1]
symfile = filename.replace("krd","symtab")
f = open(symfile,"w")
f.write(mycompiler().compile(filename))
f.close()
'''
