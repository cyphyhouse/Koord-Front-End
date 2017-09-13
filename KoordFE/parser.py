#!/usr/bin/python

import sys
from scanner import * 
from ast import * 
from codegen import * 
from symtab import *

wnum = 0
symtab = []



def p_program(p):
    '''program : agent modules awdecls ardecls locdecls init events
    '''
    p[0] = pgmAst(p[1],p[2],p[3],p[4],p[5],p[6],p[7])


def p_agent(p):
    '''agent : AGENT CID NL'''
    p[0] = p[2] 


def p_modules(p):
    '''modules : module modules 
               | module
    '''
    mlist = [p[1]]
    if len(p) == 3 :
      mlist+= p[2]
    p[0] = mlist
 
def p_module(p):
    '''module : USING MODULE CID COLON NL INDENT actuatordecls sensordecls DEDENT'''
    p[0] = moduleAst(p[3],p[7],p[8])


def p_actuatordecls(p):
    '''actuatordecls : ACTUATORS COLON NL INDENT decls DEDENT
                     | ACTUATORS COLON NL INDENT pass DEDENT
    '''
    p[0] = p[5] 

def p_sensordecls(p):
    '''sensordecls : SENSORS COLON NL INDENT decls DEDENT
                   | SENSORS COLON NL INDENT pass DEDENT
    '''
    p[0] = p[5]

def p_awdecls(p):
    '''awdecls : ALLWRITE COLON NL INDENT decls DEDENT
               | ALLWRITE COLON NL INDENT pass DEDENT'''
    #print(p[5])
    for decl in p[5]:
        #print(decl)
        decl.set_scope(MULTI_WRITER)
        global symtab
        symtab.append(mkEntry(decl))
    p[0] = p[5]

def p_ardecls(p):
    '''ardecls : ALLREAD COLON NL INDENT rvdecls DEDENT
               | ALLREAD COLON NL INDENT pass DEDENT'''
    #print(p[5])    
    for decl in p[5]:
        #print(decl)
        decl.set_scope(MULTI_READER)
        global symtab
        symtab.append(mkEntry(decl))
    p[0] = p[5]

def p_locdecls(p):
    '''locdecls : LOCAL COLON NL INDENT decls DEDENT'''
    for decl in p[5]:
        global symtab
        symtab.append(mkEntry(decl))
    p[0] = p[5]

def p_decls(p):
    '''decls : decl decls 
            |  type varnames NL 
            | empty
    '''
    dlist = []
    if len(p) == 4: 
      dlist = []
      for varname in p[2] :
          dlist.append(declAst(p[1],varname))
      p[0] = dlist
    elif len(p) == 3:
      dlist.append(p[1])
      dlist+= p[2]
    p[0] = dlist

def p_decl(p):
    '''decl : type varname ASGN exp NL
            | mapdecl NL
    '''
    if len(p) == 3:
      p[0] = (p[1])
    else:
      p[0] = (declAst(p[1],p[2],p[4]))

def p_mapdecl(p):
    '''mapdecl : MAP LT type COMMA type GT varname
    '''
    p[0] = [] 

def p_rvdecls(p):
    '''rvdecls : rvdecl rvdecls 
               | empty
    '''
    p[0] = []

def p_rvdecl(p) :
    '''rvdecl : type varname LBRACE owner RBRACE NL 
              | type varname LBRACE owner RBRACE ASGN num NL

    '''
    p[0] = []
def p_owner(p) : 
      '''owner : TIMES 
               | INUM'''
      p[0] = []

def p_funccall(p):
    '''funccall : varname LPAR args RPAR'''
    p[0] = funcAst(p[1],p[3])

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

def p_varnames(p):
    '''varnames : varname 
                | varname COMMA varnames 
    '''
    if len(p) is 2:
       p[0] = [p[1]]

    else:
       vlist = []
       vlist.append( p[1])
       vlist+= p[3]
       p[0] = vlist
       

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
    p[0] = p[5]


def p_events(p):
    '''events : event events
              | empty '''
    elist = [] 
    if len(p) == 3:
      elist.append(p[1])
      elist += p[2]
    p[0] = elist  

def p_event(p):
    '''event : LID COLON NL INDENT PRE COLON cond NL effblock DEDENT'''
    p[0] = eventAst(p[1],p[7],p[9])

def p_effblock(p):
    '''effblock : EFF COLON NL INDENT stmts DEDENT 
                | EFF COLON stmt 
    '''
    if len(p) > 4:
       p[0] = p[5]
    else:
       p[0] = p[3]


def p_cond(p):
    '''cond :  LPAR cond AND cond RPAR 
            | LPAR cond OR cond RPAR
            | LPAR cond op cond RPAR
            | LPAR NOT cond RPAR
            | exp
    '''
    if len(p) == 6:
      p[0] = condAst(p[2],p[4],p[3])
    elif len(p) == 5:
      p[0] = condAst(p[3],None,p[2])
    else: 
      p[0] = condAst(p[1],None,None)

def p_stmts(p):
    '''stmts : stmt stmts
             | empty'''
    slist = []
    if len(p) > 2:
      slist.append(p[1])
      slist+= p[2]    
    p[0] = slist

def p_stmt(p):
    '''stmt : asgn
            | pass 
            | funccall NL
            | modulefunccall NL
            | ATOMIC COLON NL INDENT stmts DEDENT 
            | IF cond COLON NL INDENT stmts DEDENT elseblock
    '''
    if len(p) <= 3:
       p[0] = p[1]
    elif len(p) == 7:
       global wnum
       p[0] = atomicAst(wnum,p[5])
       wnum += 1
    else:
       p[0] = iteAst(p[2],p[6],p[8]) 

def p_modulefunccall(p):
    '''modulefunccall : CID LPAR args RPAR '''
    p[0] = mfast(p[3])

def p_elseblock(p):
    '''elseblock : ELSE COLON NL INDENT stmts DEDENT'''
    p[0] = p[5]

def p_pass(p):
    '''pass : PASS NL'''
    p[0] = passAst()
def p_asgn(p):
    '''asgn : varname ASGN exp NL
    '''
    p[0] = asgnAst(p[1],p[3])

precedence = (('left','PLUS','MINUS'),
              ('left','TIMES','BY'))

def p_exp(p):
    '''exp : bracketexp 
           | exp PLUS exp 
           | exp TIMES exp
           | exp MINUS exp 
           | exp BY exp
           | varname 
           | bval
           | num
           | funccall
    '''
    
    if len(p) is 4:
       p[0] = exprAst('arith',p[1],p[3],p[2])
    else:
       p[0] = p[1]

def p_bracketexp(p):
    '''bracketexp : LPAR exp RPAR '''
    p[0] = p[2]

def p_bval(p):
    '''bval : TRUE 
           | FALSE
    '''
    p[0] = exprAst('bval',p[1])

def p_num(p):
    '''num : INUM 
           | FNUM
    '''
    p[0] = exprAst('num',p[1])

def p_varname(p):
    '''varname : LID 
              
    '''     
    p[0] = exprAst('var',p[1])

def p_op(p):
    '''op : EQ 
          | NEQ 
          | GEQ
          | LEQ
          | GT
          | LT
    '''
    p[0] = p[1]
 
def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print("syntax error in input on line ",p.lineno,p.type)



class myparser(object):
    def __init__(self,lexer=None):
        self.lexer = IndentLexer()
        self.parser = yacc.yacc()


    def parse(self,code):
        self.lexer.input(code)
        result = self.parser.parse(lexer=self.lexer)
        return result

class mycompiler(object):
    def __init__(self):
        self.parser = myparser()

    def compile(self,filename):
        code = open(filename,"r").read()
        pgm = (self.parser.parse(code))
        
	#appname = "testAdd"
        print(pgm.name)
        appname = str(pgm.name)+"App.java"
        f = open(appname,"w")
        global wnum
        global symtab
	f.write(codeGen(pgm,0,symtab,wnum))
	f.close()
        f = open("Main.java",'w')
        f.write(mainCodeGen(str(pgm.name),str(pgm.name)+"Drawer"))
        f.close()
        drawfile = str(pgm.name)+"Drawer.java"
        f = open(drawfile,'w')
        f.write(drawCodeGen(str(pgm.name)))
        f.close()


#filename = str(raw_input("enter filename:\n"))
filename = sys.argv[1]
mycompiler().compile(filename)
