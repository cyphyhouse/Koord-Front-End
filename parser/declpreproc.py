from modulelist import * 


#input : file, output: list of lines in the file
def getlines(filename):
  return(open(filename,"r").readlines())  

#input : line, output the first word of a line
def getfirstword(line):
  firstword = line.strip().split(" ")[0]
  return (firstword)

#input : program file, output : module name of blackbox used in a program . we only allow one blackbox . 
def getmodule(progfile):
  lines = getlines(progfile)
  for line in lines:
    if getfirstword(line) == "using":
       return line.strip().split(" ")[-1]


#input : program file, output: the declaration file of a program
def getdeclfile(progfile):
  lines = getlines(progfile)
  for line in lines:
    if getfirstword(line) == "import":
      return line.strip().split(" ")[-1]
    

#input : program file, declaration file, output : list of lines in program where the import line is replaced by the list of lines in the declarations
def insertdecls(progfile):
  proglines = getlines(progfile)
  #decls = ""
  declfile = getdeclfile(progfile)
  if declfile == 'trivial':
    for i in range(0,len(proglines)):
      if getfirstword(proglines[i]) == "import" :
        return proglines[0:i]+list(trivialdecls())+proglines[i+1:]
     
  decls = getlines(getdeclfile(progfile))
  for i in range(0,len(proglines)):
    if getfirstword(proglines[i]) == "import" :
      return proglines[0:i]+decls+proglines[i+1:]

#generate trivial declarations . input : Program file, output: no shared declarations. 

def trivialdecls():
  s = "allwrite:\n"+" "*4+"pass\n"+"allread:\n"+" "*4+"pass\n" 
  return s 

#insert module declarations 
def insertmoduledecls(progfile):

  proglines = getlines(progfile)
  moduledecls = ":\n"+moduleparts[str(getmodule(progfile))] 
  for i in range(0,len(proglines)):
    if getfirstword(proglines[i]) == "using" :
      proglines[i] = proglines[i].rstrip()
      return (proglines[0:i+1])+list(moduledecls)+(proglines[i+1:])

 
#input : list of lines, ouput: text composed of the lines in the list
def gettextfromlines(lines):
  text = ""
  for line in lines: 
    text+= line 
  return text   

#input : program file . creates a backup of the file.
def backupfile(progfile):
  prog = open(progfile,"r").read()
  backup = open(progfile+".backup","w")
  backup.write(prog)
  backup.close()

def declpreproc(progfile):
  backupfile(progfile)
  progwithmods = insertmoduledecls(progfile)
  text = gettextfromlines(progwithmods)
  f = open(progfile,"w")
  f.write(text)
  f.close()
  progwithdecls = insertdecls(progfile)
  text = gettextfromlines(progwithdecls)
  #print(text)
  f = open(progfile,"w")
  f.write(text)
  f.close()
  
#test
filename = raw_input("enter filename:\n") 
declpreproc(filename) 
