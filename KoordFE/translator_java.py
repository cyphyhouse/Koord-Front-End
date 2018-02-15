from codegen import *
import parser
from symparser import symparser

class mycompiler(object):
    def __init__(self):
        self.parser = parser.myparser()

    def compile(self,filename):
        code = open(filename,"r").read()
        pgm = (self.parser.parse(code))
        symtab = symparser().parse(code)
        appname = str(pgm.name)+"App.java"
        f = open(appname,"w")
	f.write(codeGen(pgm,0,symtab,False,None,parser.wnum))
	f.close()
        f = open("Main.java",'w')
        f.write(mainCodeGen(str(pgm.name),str(pgm.name)+"Drawer"))
        f.close()
        drawfile = str(pgm.name)+"Drawer.java"
        f = open(drawfile,'w')
        f.write(drawCodeGen(str(pgm.name)))
        f.close()
        f = open(str(pgm.name)+".symtab","w")
        f.write(str(symtab))
        f.close()
