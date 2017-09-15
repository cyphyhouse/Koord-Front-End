from ast import *

#dictionary for modules
flagdict = {'Motion':"import edu.illinois.mitra.cyphyhouse.motion.MotionParameters;\nimport edu.illinois.mitra.cyphyhouse.motion.MotionParameters.COLAVOID_MODE_TYPE;\nimport edu.illinois.mitra.cyphyhouse.objects.ItemPosition;", 'Trivial' : ""}

#dictionary for module functions
moduleprefix = {'Motion': 'gvh.plat.moat.'}

#initialization code for modules 
initdict = {'Motion' : "MotionParameters.Builder settings = new MotionParameters.Builder();\nsettings.COLAVOID_MODE(COLAVOID_MODE_TYPE.USE_COLBACK);\nMotionParameters param = settings.build();\ngvh.plat.moat.setParameters(param);\n", 'Trivial': ""}
def flagCodeGen(flags): 
    m = ""
    for flag in flags[0]: 
        if flag in flagdict:
           m += flagdict[flag]+"\n"
        else: 
           print("warning: module "+str(flag)+" not previously defined, consider checking name\n") 
           pass
    if flags[1] == True:
        m+= "import edu.illinois.mitra.cyphyhouse.interfaces.MutualExclusion;\nimport edu.illinois.mitra.cyphyhouse.functions.DSMMultipleAttr;\nimport edu.illinois.mitra.cyphyhouse.functions.GroupSetMutex;\nimport edu.illinois.mitra.cyphyhouse.functions.SingleHopMutualExclusion;\nimport edu.illinois.mitra.cyphyhouse.interfaces.DSM;\n" 
    return m


#adding indentations 
def mkindent(text,tabs):
    indent = tabs * 4 * " "
    textlines = text.split("\n")
    s = ""
    for line in textlines: 
        s += indent + line + "\n"
    return s 


recvfunc = "    @Override\n    protected void receive(RobotMessage m) {\n	return;\n   }\n"
#import code

def impCodeGen():
  s = '''import java.util.HashMap;\nimport java.util.HashSet;\nimport java.util.List;\nimport java.util.Map;\n\nimport edu.illinois.mitra.cyphyhouse.comms.RobotMessage;\nimport edu.illinois.mitra.cyphyhouse.gvh.GlobalVarHolder;\nimport edu.illinois.mitra.cyphyhouse.interfaces.LogicThread;\nimport edu.illinois.mitra.cyphyhouse.objects.ItemPosition;\n\n'''
  return s


#generating package name, and appname from the high level prog
def packageNameGen(appname):
    return "package testSim."+appname.lower()+";\n\n"


#generate class name 
def classGen(appname):
    appname = appname.title() + "App"
    return "public class "+appname+" extends LogicThread {\n" 


def getVars(expr):
   if expr is None : 
      return []
   elif expr.get_type() == 'var':
      return [expr.lexp]
   elif expr.get_type() == 'num':
      return []
   elif expr.get_type() == 'bval':
      return []
   else:
      return getVars(expr.lexp)+getVars(expr.rexp)


#initialize gvh and create robots
def mandatoryDecls(pgmast,tabs,wnum):
    
    decls = mkindent("private static final String TAG = " + '"' + pgmast.name + ' App"'  + ";",tabs)
    decls += mkindent("int pid;\nprivate int numBots;",tabs)
    flags = pgmast.getflags() 
    if flags[1] == True :
        for i in range(0,wnum):
           decls+= mkindent("private MutualExclusion mutex"+str(i)+";\n",tabs) 
        decls += mkindent("private DSM dsm;\n",tabs)
    '''
    for module in pgmast.modules:
        ads = module.actuatordecls
        sds = module.sensordecls 
        for ad in ads : 
            decls += codeGen(ad,tabs)
        for sd in sds : 
            decls += codeGen(sd,tabs)
    '''
    return decls + "\n"

#constructor method
def classInit(appname):
    appname = appname.capitalize() + "App"
    return "public "+appname+" (GlobalVarHolder gvh)" 

#mandatory initializations 
def mandatoryInits(pgmast,tabs,wnum): 
    inits = mkindent('pid = Integer.parseInt(name.replaceAll("[^0-9]", ""));',tabs)
    inits += mkindent("numBots = gvh.id.getParticipants().size();",tabs)
    flags = pgmast.getflags() 
    if flags[1] == True :
        for i in range(0,wnum): 
           s = "mutex"+str(i)+ "= new GroupSetMutex(gvh, 0);\n"
        s+="dsm = new DSMMultipleAttr(gvh);"
        inits += mkindent(s,tabs)
    for module in flags[0]:
        inits += mkindent(initdict[module],tabs)
    return inits

#code generation for Casting. 
def createval(dtype):
    if dtype == 'int':
       return 0
    if dtype == 'float':
       return 0.0



def mkDsms(symtab):
    s = ""
    for symentry in symtab :
        if symentry.scope == MULTI_WRITER:
           s+= 'dsm.createMW("'+str(symentry.varname)+'",'+str(createval(str(symentry.dtype)))+");\n"    
    return s
        
def cast(dtype):
    if dtype == 'int':
       return "Integer.parseInt"
      
def getCodeGen(v,symtab):
    e= getEntry(v,symtab)
    if e is not None:
       if e.scope is not LOCAL:
          return str(e.varname)+" = "+cast(e.dtype)+"("+"dsm.get("+'"'+ str(e.varname) +'","'+ str(e.owner)+'"'  +"));"
       return ""
    return ""

def putCodeGen(lv,symtab):
      if lv.scope is not LOCAL: 
        return ("dsm.put("+'"'+ str(lv.varname)+'","'+ str(lv.owner)+'"'+","+str(lv.varname)+ ");")
      return "" 

def codeGen(inputAst,tabs,symtab = [],wnum = 0):
    s= ""  
    if inputAst is None :
       return s 
    if inputAst.get_type() == pgmtype :
      pgm = inputAst
      s+= packageNameGen(pgm.name)
      s+= impCodeGen()
      s+= flagCodeGen(pgm.getflags())+"\n\n" 
      s+= classGen(pgm.name)
      
      s+= mandatoryDecls(pgm,tabs+1,wnum)
      for decl in inputAst.awdecls:
         s+= codeGen(decl,tabs+1) 
      s+= "\n"      
      for decl in inputAst.ardecls:
         s+= codeGen(decl,tabs+1)       
      s += "\n"
      for decl in inputAst.locdecls:
 	  s+= codeGen(decl,tabs+1) 
    
      for i in range(0,wnum):
        declstr = "private boolean wait"+str(i)+" = false;"
        s+= mkindent(declstr,tabs+2) 

      s+= mkindent(classInit(pgm.name),tabs+1).rstrip()+"{\n"
      s+= mkindent("super(gvh);",tabs+2)
      s+= mandatoryInits(pgm,tabs+2,wnum)
      for stmt in pgm.init:
        s+= codeGen(stmt,tabs+2,symtab)
      s+= mkindent("}\n",tabs+1)
      s+= mkindent("@Override",tabs+1)
      s+= mkindent("public List<Object> callStarL() {",tabs+1)
      s+= mkindent(mkDsms(symtab),tabs+2)
      s+= mkindent("while(true) {",tabs+2)
      s+= mkindent("sleep(100);",tabs+3)
      events = pgm.events
      for e in events:
        s+=codeGen(e,tabs+3,symtab)      
      s+= mkindent("}",tabs+2)
      s+= mkindent("}",tabs+1)
      s+= recvfunc
      s+= mkindent("}",tabs)
    if inputAst.get_type() == 'var':
      e = getEntry(inputAst,symtab) 
      if e is not None:
        if e.module is not None: 
           return modulePrefix+str(inputAst)
        else:
           return str(inputAst)
    if inputAst.get_type() == 'num':
      return str(inputAst)
    if inputAst.get_type() == 'bval':
      return str(inputAst) 
    if inputAst.get_type() == 'var':
      return str(inputAst) 

    if inputAst.get_type() == 'arith':
      return codeGen(inputAst.lexp,0,symtab) +" " + str(inputAst.op) + " "+ codeGen(inputAst.rexp,0,symtab)      

    if inputAst.get_type() == inittype:
     for stmt in inputAst.stmts:
      s+= codeGen(stmt,tabs)  
    if inputAst.get_type() == evnttype :
      event = inputAst
      vs = getVars(event.pre)
      for v in vs:
        s+= mkindent(getCodeGen(v,symtab),tabs)
      #print(event)
      s += mkindent("if ("+ codeGen(event.pre,0,symtab)+"){\n",tabs)

      for stmt in event.eff:
          #s+= str(stmt)
          s+= codeGen(stmt,tabs+1,symtab)
          s+= mkindent("continue;\n",tabs+1)
      s+= mkindent("}",tabs)
       
    if inputAst.get_type() == condtype :
      cond = inputAst
      if cond.rexp is not None:
        s += "("+codeGen(cond.lexp,0,symtab) + str(cond.op) + codeGen(cond.rexp,0,symtab)+")"
      elif cond.op is not None:
        s += "("+ str(cond.op)+codeGen(cond.lexp,0,symtab)+")"
      else:
        s+= "("+ codeGen(cond.lexp,0,symtab)+")"
    if inputAst.get_type() == 'pass':
      s+= ""
    if inputAst.get_type() == atomictype: 
      atst = inputAst
      p = "if(!wait"+str(atst.wnum)+"){\n"
      s+= mkindent(p,tabs)
      p = "mutex"+str(atst.wnum)+".requestEntry(0);\nwait"+str(atst.wnum)+" = true;\n"
      s+= mkindent(p,tabs+1)
      s+= mkindent("}",tabs)
      s+= mkindent("if (mutex"+str(atst.wnum)+".clearToEnter(0)) {\n",tabs)
      for stmt in atst.stmts: 
        s+= codeGen(stmt,tabs+1,symtab)
      s+= mkindent("mutex"+str(atst.wnum)+".exit(0);\n",tabs+1)
      s+= mkindent("}\n",tabs)
    if inputAst.get_type() == 'asgn':
      #print(inputAst)
      vs = (getVars(inputAst.rexp))
      
      lv = getEntry((inputAst.lvar),symtab)
      #print(inputAst.lvar,lv)
     
      for v in vs:
          s+= mkindent(getCodeGen(v,symtab),tabs) 
      s+=  mkindent(codeGen(inputAst.lvar,0,symtab)+" = "+codeGen(inputAst.rexp,0,symtab)+";",tabs)
      s+= mkindent(putCodeGen(lv,symtab),tabs)
      #print(s)
    if inputAst.get_type() == 'ite':
      vs = getVars(inputAst.cond)
      for v in vs:
         s+= mkindent(getCodeGen(v,symtab),tabs)
      istr = "if"+ codeGen(inputAst.cond,tabs)+ "{\n"
      for stmt in inputAst.t :
         istr+= codeGen(stmt,1,symtab)
      istr+= "}\n"
      istr+= "else {\n"
      for stmt in inputAst.e :
         istr+= codeGen(stmt,1,symtab)
      istr+= "}\n"
      s+= mkindent(istr,tabs) 
    elif inputAst.get_type() == 'decl':
       qualifier = "" 
       if inputAst.scope == LOCAL: 
          qualifier = ""
       elif inputAst.scope ==  MULTI_WRITER:	
          qualifier = "public"
       elif inputAst.scope ==  MULTI_READER: 	
          qualifier = "public"
       elif inputAst.scope ==  CONTROLLER:	
          qualifier = "public"
       #print(inputast.value)
       if inputAst.value is None:
          s = mkindent(qualifier+ " "+ str(inputAst.dtype) + " " + str(inputAst.varname) +";",tabs)  
       else:
          s = mkindent(qualifier+ " "+ str(inputAst.dtype) + " " + str(inputAst.varname) + " = " + str(inputAst.value)+";",tabs)
    return s

def mainCodeGen(name,drawname):

    s= "package testSim." + name.lower()+";\n\n"

    s+= "import testSim.main.SimSettings;\n"
    s+= "import testSim.main.Simulation;\n"
    s+= "public class Main {\n" 
    s+= mkindent("public static void main(String[] args) {",1)
    s+= mkindent("SimSettings.Builder settings = new SimSettings.Builder();",2)
    s+= mkindent("settings.N_IROBOTS(4);",2)
    s+= mkindent("settings.N_QUADCOPTERS(0);",2)
	
    s+= mkindent("settings.TIC_TIME_RATE(2);",2)
    s+= mkindent('settings.WAYPOINT_FILE("square.wpt");',2)
    s+= mkindent('settings.DRAW_WAYPOINTS(false);',2)
    s+=mkindent('settings.DRAW_WAYPOINT_NAMES(false);',2)

    s+= mkindent('settings.DRAWER(new '+str(drawname)+'());',2)
		
    s+= mkindent('Simulation sim = new Simulation('+str(name)+'App.class, settings.build());',2)

    s+= mkindent('sim.start();',2)
    s+= mkindent('}',1)
    s+= '}'
    return s

def drawCodeGen(name):
  s= 'package testSim.'+str(name).lower() +';'

  s+='import java.awt.BasicStroke;\n'
  s+='import java.awt.Color;\n'
  s+='import java.awt.Graphics2D;\n'
  s+='import java.awt.Stroke;\n'
  s+='import org.apache.log4j.Logger;\n\n'

  s+='import edu.illinois.mitra.cyphyhouse.interfaces.LogicThread;\n'
  s+='import testSim.draw.Drawer;\n\n'

  s+='public class ' +str(name) +'Drawer extends Drawer {\n'

  s+=mkindent('private Stroke stroke = new BasicStroke(8);',1)
  s+=mkindent('private Color selectColor = new Color(0,0,255,100);',1)
  s+=mkindent('private static org.apache.log4j.Logger log = Logger.getLogger('+ str(name) +'Drawer.class);',1)
  s+=mkindent('@Override',1)
  s+=mkindent('public void draw(LogicThread lt, Graphics2D g) {',1)
  s+=mkindent(str(name) +'App app = ('+str(name)+'App) lt;',2)
		
  s+=mkindent('g.setColor(Color.RED);',2)
  s+=mkindent('g.setColor(selectColor);',2)
  s+=mkindent('g.setStroke(stroke);',2)
  s+=mkindent('//log.info("sum :"+String.valueOf(app.sum));',2)  
  s+=mkindent('//g.drawString("current total "+String.valueOf(app.currentTotal),100+10*app.robotIndex,150);',2)
  s+=mkindent('}',1)

  s+='}'
  return s  
