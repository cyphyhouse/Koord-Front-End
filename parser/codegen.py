from ast import * 
from symtab import *

#dictionary for modules
flagdict = {'Motion':"import edu.illinois.mitra.cyphyhouse.motion.MotionParameters;\nimport edu.illinois.mitra.cyphyhouse.motion.MotionParameters.COLAVOID_MODE_TYPE;\nimport edu.illinois.mitra.cyphyhouse.objects.ItemPosition;", 'Trivial' : ""}

#dictionary for module functions
moduleprefix = {'Motion': 'gvh.plat.moat.', 'Trivial' : ''}


#initialization code for modules 
initdict = {'Motion' : "MotionParameters.Builder settings = new MotionParameters.Builder();\nsettings.COLAVOID_MODE(COLAVOID_MODE_TYPE.USE_COLBACK);\nMotionParameters param = settings.build();\ngvh.plat.moat.setParameters(param);\n", 'Trivial': ""}


recvfunc = "    @Override\n    protected void receive(RobotMessage m) {\n	return;\n }\n"
destfunc = ' @SuppressWarnings("unchecked")\n    private <X, T> T getDestination(Map<X, T> map, int index) {\n        String key = Integer.toString(index) + "-A";\n       return map.get(key);}\n'

#import code
def impCodeGen():
	s = '''import java.util.HashMap;\nimport java.util.HashSet;\nimport java.util.List;\nimport java.util.Map;\n\nimport edu.illinois.mitra.cyphyhouse.comms.RobotMessage;\nimport edu.illinois.mitra.cyphyhouse.gvh.GlobalVarHolder;\nimport edu.illinois.mitra.cyphyhouse.interfaces.LogicThread;\n\n'''
	return s


#generate import statements depending on the modules and whether distributed shared memory is necessary
def flagCodeGen(flags): 
    m = ""
    print(flags)
    for flag in flags[0]: 
        if flag in flagdict:
           m += flagdict[flag]+"\n"
        else: 
           print("warning: module "+str(flag)+" not previously defined, consider checking name\n") 
           pass
    if flags[1] == True:
        m+= "import edu.illinois.mitra.cyphyhouse.interfaces.MutualExclusion;\nimport edu.illinois.mitra.cyphyhouse.functions.DSMMultipleAttr;\nimport edu.illinois.mitra.cyphyhouse.functions.GroupSetMutex;\nimport edu.illinois.mitra.cyphyhouse.functions.SingleHopMutualExclusion;\nimport edu.illinois.mitra.cyphyhouse.interfaces.DSM;\n" 
    return m


#generating package name, and appname from the high level prog
def packageNameGen(appname):
    return "package testSim."+appname.lower()+";\n\n"

def classGen(appname):
    appname = appname.capitalize() + "App"
    return "public class "+appname+" extends LogicThread {\n" 

def classInit(appname):
    appname = appname.capitalize() + "App"
    return "public "+appname+" (GlobalVarHolder gvh)" 

#initialize gvh and create robots 
  
#mandatory declarations
def mandatoryDecls(pgmast,tabs):
    indent = 4 * tabs *" "
    decls = indent+"private static final String TAG = " + '"' + pgmast.name + ' App"'  + ";\n"
    decls += indent+"int robotIndex;\n"
    decls += indent+"private int numBots;\n\n"
    flags = pgmast.getflags() 
    if flags[1] == True : 
        decls += indent+"private MutualExclusion mutex;\n"+indent+"private DSM dsm;\n\n"
    for module in pgmast.modules:
        ads = module.actuatordecls
        sds = module.sensordecls 
        for ad in ads : 
            decls += codeGen(ad,tabs)
        for sd in sds : 
            decls += codeGen(sd,tabs)
    return decls + "\n"

#adding indentations 
def mkindent(text,tabs):
    indent = tabs * 4 * " "
    textlines = text.split("\n")
    s = ""
    for line in textlines: 
        s += indent + line + "\n"
    return s 


#mandatory initializations 
def mandatoryInits(pgmast,tabs): 
    indent = 4 * tabs * " "
    inits = indent + 'robotIndex = Integer.parseInt(name.replaceAll("[^0-9]", ""));\n'
    inits += indent +"numBots = gvh.id.getParticipants().size();\n"
    flags = pgmast.getflags() 
    if flags[1] == True : 
        inits += indent+"mutex = new GroupSetMutex(gvh, 0);\n"+indent+"dsm = new DSMMultipleAttr(gvh);\n"
    for module in flags[0]:
        inits += mkindent(initdict[module],tabs) 
    return inits


#main code generation function
def codeGen(inputast,tabs):
    t =  inputast.get_type()
    #print(t)
    s = ""
    indent = tabs * 4 *" "
    if t == 'pgm':
       appname = inputast.name
       s += packageNameGen(appname)
       s += impCodeGen()
       s += flagCodeGen(inputast.getflags())+"\n"
       s += classGen(appname)
       s += mandatoryDecls(inputast,tabs+1)
       for decl in inputast.awdecls:
          s+= codeGen(decl,tabs+1) 
       s+= "\n"      
       for decl in inputast.ardecls:
          s+= codeGen(decl,tabs+1)       
       s += "\n"
       for decl in inputast.locdecls:
 	  s+= codeGen(decl,tabs+1) 
                 
             #print("map") 
             #s+= mkindent(tabs+1,str(decl)) 
       s += "\n"
       s += (tabs+1) * 4 * " "+classInit(appname)+"{\n"
       s += (tabs+2) * 4 * " "+"super(gvh);\n"
       s += mandatoryInits(inputast,tabs+2)
       s += codeGen(inputast.init,tabs+2) + (tabs+1)*4*" "+"}\n"
       s += mkindent("@Override",tabs+1)
       s += mkindent("public List<Object> callStarL() {",tabs+1)
       s += mkindent("while(true) {",tabs+2)
       s += mkindent("sleep(100);",tabs+3) 
       e = inputast.events[0]
     
       for event in inputast.events:
           s += ((tabs + 4) * 4 * " ") + "if (" + codeGen(event.pre,0) + ") {\n";
           s += codeGen(event,tabs+5)
           s += mkindent("}",tabs+4)
       s += mkindent("}",tabs+3)
     
       #s += mkindent("}",tabs+2)
       s += mkindent("}",tabs+1)
       s += mkindent(recvfunc,tabs+1)
       s += mkindent(destfunc,tabs+1)

       s += "}"

       
    elif t == 'init':
       for stmt in inputast.stmts:
         s+= codeGen(stmt,tabs)    
    elif t == 'decl':
       qualifier = "" 
       if inputast.scope == LOCAL: 
          qualifier = "private"
       elif inputast.scope ==  MULTI_WRITER:	
          qualifier = "public"
       elif inputast.scope ==  MULTI_READER: 	
          qualifier = "public"
       elif inputast.scope ==  CONTROLLER:	
          qualifier = "public"
       #print(inputast.value)
       if inputast.value is None:
          s = indent + qualifier+ " "+ str(inputast.dtype) + " " + str(inputast.varname) +";\n"  
       else:
          s = indent + qualifier+ " "+ str(inputast.dtype) + " " + str(inputast.varname) + " = " + str(inputast.value)+";\n"  
    elif t == 'map':
          s = indent + str(inputast)+";\n" 
    elif t == 'evnt':
          for stmt in inputast.eff:
             #print(stmt)
             s += codeGen(stmt,tabs)
    elif t == 'cond':
        s += str(inputast)
    elif t == 'ite':
        s += mkindent("if "+codeGen(inputast.cond,0),tabs)+"\n"
        s += mkindent("{",tabs)
        for stmt in inputast.t :
            s += (codeGen(stmt,tabs+1))
        s += mkindent("}",tabs)
        if inputast.e is not None:
            s += mkindent("else {\n",tabs)
            for stmt in inputast.e :
                s += codeGen(stmt,tabs+1)
            s += mkindent("}",tabs)
    elif t == 'asgn':
        m = str(inputast.lvar)
        m += " = "+ codeGen(inputast.rexp,0)
        s+= mkindent(str(m)+";",tabs)
    elif t == 'func':
        m = str(inputast.name)+"("
        if len(inputast.args) == 0 :
           m+= ")"
        else: 
          for i in range(len(inputast.args)-1) :
            m+= str(inputast.args[i])+", "
          m+= str(inputast.args[-1]) +")"
        s+= m
    elif t == 'mfast':
        modname = moduleprefix[inputast.modfunc[:str(inputast.modfunc).find('.')]]
        s += mkindent(str(modname)+str(inputast) +";\n",tabs)
    elif t == 'expr':
        s += str(inputast) 
    elif t == 'pass':
        pass
    return s  
