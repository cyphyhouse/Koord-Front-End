
from lexer import * 


def p_program(p):
    '''program : agent modules awdecls ardecls locdecls init events
    '''
    p[0] = []


def p_agent(p):
    '''agent : AGENT CID NL'''
    p[0] = []


def p_modules(p):
    '''modules : module modules
               | empty
    '''
    p[0] = []

def p_module(p):
    '''module : USING MODULE CID COLON NL INDENT actuatordecls sensordecls DEDENT'''
    p[0] = []

def p_actuatordecls(p):
    '''actuatordecls : ACTUATORS COLON NL INDENT decls DEDENT
                     | ACTUATORS COLON NL INDENT pass DEDENT
    '''
    p[0] = []

def p_sensordecls(p):
    '''sensordecls : SENSORS COLON NL INDENT decls DEDENT
                   | SENSORS COLON NL INDENT pass DEDENT
    '''
    p[0] = p[]

def p_awdecls(p):
    '''awdecls : ALLWRITE COLON NL INDENT decls DEDENT
               | ALLWRITE COLON NL INDENT pass DEDENT'''
    p[0] = p[]

def p_ardecls(p):
    '''ardecls : ALLREAD COLON NL INDENT rvdecls DEDENT
               | ALLREAD COLON NL INDENT pass DEDENT'''
    p[0] = []

def p_locdecls(p):
    '''locdecls : LOCAL COLON NL INDENT decls DEDENT'''
    p[0] = p[]

def p_decls(p):
    '''decls : decl decls 
             | empty
    '''
    p[0] = []

def p_decl(p):
    '''decl : type varnames NL
            | type varname ASGN exp NL
            | mapdecl NL
    '''
    p[0] = [] 

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
      p[0] = p[]

def p_funccall(p):
    '''funccall : varname LPAR args RPAR'''
    p[0] = []

def p_args(p):
    '''args : neargs 
            | noargs
    '''
    p[0] = []

def p_noargs(p):
    '''noargs : empty'''
    p[0] = []

def p_neargs(p):
    '''neargs : exp 
              | exp COMMA neargs
    '''
    p[0] = []

def p_varnames(p):
    '''varnames : varname 
                | varname COMMA varnames 
    '''
    p[0] = []

def p_type(p):
    '''type : INT
            | STRING 
            | FLOAT
            | IPOS
            | BOOLEAN 
    '''
    p[0] = []
    #print(p[0])

def p_init(p):
    '''init : INIT COLON NL INDENT stmts DEDENT
            | empty
    '''
    p[0] = []

def p_events(p):
    '''events : event events
              | empty '''
    p[0] = []

def p_event(p):
    '''event : LID COLON NL INDENT PRE COLON cond NL effblock DEDENT'''
    p[0] = []

def p_effblock(p):
    '''effblock : EFF COLON NL INDENT stmts DEDENT 
                | EFF COLON stmt 
    '''
    p[0] = []


def p_cond(p):
    '''cond :  LPAR cond AND cond RPAR 
            | LPAR cond OR cond RPAR
            | LPAR exp op exp RPAR
            | LPAR NOT cond RPAR
            | exp
    '''
    p[0] = []

def p_stmts(p):
    '''stmts : stmt stmts
             | empty'''
    p[0] = []

def p_stmt(p):
    '''stmt : asgn
            | funccall NL
            | modulefunccall NL
            | IF cond COLON NL INDENT stmts DEDENT elseblock
            | pass 
   '''
   p[0] = []

def p_modulefunccall(p):
    '''modulefunccall : CID LPAR args RPAR '''
    p[0] = []

def p_elseblock(p):
    '''elseblock : ELSE COLON NL INDENT stmts DEDENT'''
    p[0] = []

def p_pass(p):
    '''pass : PASS NL'''
    p[0] = []

def p_asgn(p):
    '''asgn : varname ASGN exp NL
    '''
    p[0] = []

precedence = (('left','PLUS','MINUS'),
              ('left','TIMES','BY'))

def p_exp(p):
    '''exp : exp PLUS exp 
           | exp TIMES exp
           | exp MINUS exp 
           | exp BY exp
           | varname 
           | TRUE
           | FALSE
           | num
           | funccall
    '''
    p[0] = []


def p_num(p):
    '''num : INUM 
           | FNUM
    '''
    p[0] = []

def p_varname(p):
    '''varname : LID 
              
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
        pgm = self.parser.parse(code)
	appname = str(pgm.name)+"App.java"
        f = open(appname,"w")
	f.write(codeGen(pgm,0))
	f.close()



filename = raw_input("enter filename:\n")
compile = mycompiler().compile(filename)
