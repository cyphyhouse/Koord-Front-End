from ast import *

includecode = "import java.util.HashMap;\nimport java.util.HashSet;\nimport edu.illinois.mitra.cyphyhouse.interfaces.MutualExclusion;\nimport java.util.List;\nimport java.util.Map;\nimport edu.illinois.mitra.cyphyhouse.functions.DSMMultipleAttr;\nimport edu.illinois.mitra.cyphyhouse.comms.RobotMessage;\nimport edu.illinois.mitra.cyphyhouse.gvh.GlobalVarHolder;\nimport edu.illinois.mitra.cyphyhouse.interfaces.LogicThread;\nimport edu.illinois.mitra.cyphyhouse.motion.MotionParameters;\nimport edu.illinois.mitra.cyphyhouse.motion.RRTNode;\nimport edu.illinois.mitra.cyphyhouse.motion.MotionParameters.COLAVOID_MODE_TYPE;\nimport edu.illinois.mitra.cyphyhouse.objects.ItemPosition;\nimport edu.illinois.mitra.cyphyhouse.objects.ObstacleList;\nimport edu.illinois.mitra.cyphyhouse.objects.PositionList;\nimport edu.illinois.mitra.cyphyhouse.interfaces.DSM;\nimport edu.illinois.mitra.cyphyhouse.functions.GroupSetMutex;"

moduleprefix = {'Motion': 'gvh.plat.moat.','Gps' : 'gvh.gps.'}

initcode = "MotionParameters.Builder settings = new MotionParameters.Builder();\nsettings.COLAVOID_MODE(COLAVOID_MODE_TYPE.USE_COLBACK);\nMotionParameters param = settings.build();\ngvh.plat.moat.setParameters(param);\n"

recvfunc = "    @Override\n    protected void receive(RobotMessage m) {\n    }\n"

def mkindent(text,tabs):
    indent = tabs * 4 * " "
    textlines = text.split("\n")
    s = ""
    for line in textlines: 
        s += indent + line + "\n"
    return s

def addnl(s,n):
    s+="\n"*n
    return s

def packageNameGen(appname):
    return "package testSim."+appname.lower()+";\n\n"

    
def classGen(appname):
    appname = appname.title() + "App"
    return "public class "+appname+" extends LogicThread {\n" 

def stageGen(stagelist):
    s = "private enum Stage { \n    "
    for i in range(0,len(stagelist)-1):
       s += stagelist[i].upper() 
       s +=", "
    s+= stagelist[-1].upper()+"\n"
    s+= "};\n"
    s+= "private Stage stage;\n"
    return s  

def mandatoryDecls(pgmast,tabs,wnum):
    decls = mkindent("private static final String TAG = " + '"' + pgmast.name + ' App"'  + ";",tabs)
    
    for i in range(0,wnum):
        decls+= mkindent("private MutualExclusion mutex"+str(i)+";\n",tabs) 
    decls += mkindent("private DSM dsm;\n",tabs)
    decls += mkindent("int pid;\nprivate int numBots;",tabs)
    flags = pgmast.getflags() 
    return decls + "\n"

def classInit(appname):
    appname = appname.capitalize() + "App"
    return "public "+appname+" (GlobalVarHolder gvh) {\n    super(gvh);" 

def mandatoryInits(pgmast,wnum):
    inits ='pid = Integer.parseInt(name.replaceAll("[^0-9]", ""));\nnumBots = gvh.id.getParticipants().size();\ndsm = new DSMMultipleAttr(gvh);'
    for i in range(0,wnum):
        inits+= ("mutex"+str(i)+" = new GroupSetMutex(gvh,0);\n") 
    return inits

def createval(dtype):
    if dtype == 'int':
       return 0
    if dtype == 'float':
       return 0.0

def mkDsms(symtab):
    s = ""
    for symentry in symtab[0] :
        if symentry.scope == MULTI_WRITER:
           s+= 'dsm.createMW("'+str(symentry.varname)+'",'+str(createval(str(symentry.dtype)))+");\n"    
    return s

def getVars(expr):
   if not(isAst(expr)) :
      return []
   if expr is None : 
      return []
   elif expr.get_type() == nulltype:
      return []
   elif expr.get_type() == vartype:
      return [(expr.lexp,None)]
   elif expr.get_type() == rvtype:
      return [(expr.varname,expr.access)]
   elif expr.get_type() == numtype:
      return []
   elif expr.get_type() == bvaltype:
      return []
   elif expr.get_type() == functype :
      l = []
      for var in expr.args:
         l+= getVars(var)
      return l 
   elif expr.get_type() == mfasttype:
      l = []
      for var in expr.args:
         l+= getVars(var)
      return l 
      
   else:
      return getVars(expr.lexp)+getVars(expr.rexp)

def rvgetCodegen(var,owner):
    s = 'dsm.get("'+str(var)+'",name.replaceAll("[0-9]","")+String.valueOf('+str(owner)+'))'
    return s
def mwgetCodegen(var,owner):
    s = 'dsm.get("'+str(var)+'","*")'
    return s
 
def rvputCodegen(var):
    s = 'dsm.put("'+str(var)+'"+name,name,'+str(var)+');'
    return s
def mwputCodegen(var):
    s = 'dsm.put("'+str(var)+'","*",'+str(var)+');'
    return s

def checknull(var,stages,event = None):
    stmt = ""
    if (stages):
       stmt = "break" 
    else:
       stmt = "continue"
    return "if ("+str(var) +" == null) {"+stmt + ";}"




def codeGen(inputAst,tabs,symtab = [],stages = False, ename= None,wnum = 0):
    s = ""
    if not(isAst(inputAst)):
       return s
    t = inputAst.get_type()
    if t == pgmtype:
       pgm = inputAst
       appname = pgm.name
       s+= packageNameGen(appname)
       s+= includecode
       s = addnl(s,2)
       s+= classGen(appname)
       print wnum
       s+= mandatoryDecls(pgm,1,wnum)
       sl = pgm.stages
       if sl is not None:
          s+= mkindent(stageGen(sl),tabs+1)
          stages = True
       awd = pgm.awdecls
       ard = pgm.ardecls 
       loc = pgm.locdecls
   
       if awd is not None:
         for decl in awd:
 	   s+= codeGen(decl,tabs+1,symtab,stages,ename) 
       if ard is not None:
         for decl in ard:
 	   s+= codeGen(decl,tabs+1,symtab,stages,ename) 
       if loc is not None:
         for decl in loc:
 	   s+= codeGen(decl,tabs+1,symtab,stages,ename) 
       declstr = ""
       for i in range(0,wnum):
         declstr += "private boolean wait"+str(i)+" = false;"
       s+= mkindent(declstr,tabs+2) 
       s+= mkindent(classInit(appname),tabs+1)
       s+= mkindent(initcode,tabs+2)
       s+= mkindent(mandatoryInits(pgm,wnum),tabs+2)
       s+= mkindent("}",tabs+1)
       s+= mkindent("@Override",tabs+1)
       s+= mkindent("public List<Object> callStarL() {",tabs+1)
       s+= mkindent(mkDsms(symtab),tabs+2)
       s+= codeGen(pgm.init,tabs+2,symtab,stages,ename)
       s+= mkindent("while(true) {",tabs+2)
       s+= mkindent("sleep(100);",tabs+3)
       if pgm.stages is not None:
         s+= mkindent("switch(stage) {",tabs+3) 
         for event in pgm.events:
           epre = "case "+str(event.pre).upper()+":\n"
           s+=mkindent(epre,tabs+4)
           for stmt in event.eff: 
               s+= codeGen(stmt,tabs+5,symtab,stages,ename)
           s+= mkindent("break;",tabs+4)
         s+= mkindent("}",tabs+3)
       else:
         for event in pgm.events:
            s+= codeGen(event, tabs+4, symtab,stages,ename) 
       s+= mkindent("}",tabs+2)
       s+= mkindent("}",tabs+1)
       s+= recvfunc
       s+= "}"
    elif (t == decltype):
       decl = inputAst
       if decl.value is None :
          s = mkindent(str(decl.dtype) + " " + str(decl.varname) +";",tabs)     
       else: 
          s = mkindent(str(inputAst.dtype) + " " + str(inputAst.varname) + " = " + str(inputAst.value)+";",tabs)
    elif (t == rvdecltype):
       decl = inputAst
       if decl.value is None :
          s = mkindent(str(decl.dtype) + " " + str(decl.varname) +";",tabs)     
       else: 
          s = mkindent(str(inputAst.dtype) + " " + str(inputAst.varname) + " = " + str(inputAst.value)+";",tabs)   
    elif (t == inittype):
       initstr = ""
       for stmt in inputAst.stmts:
         initstr += codeGen(stmt,0,symtab,stages,ename)
       s = mkindent(initstr,tabs)
    elif t == exittype:
       s = mkindent("return null;",tabs)
    elif t == stctype:
       newst = str(inputAst.newst)
       s = mkindent("stage = Stage."+newst.upper()+";",tabs)
    elif t == vartype:
      e = getEntry(inputAst,symtab) 
      if e is not None:
        if e.module is not None:
           s = moduleprefix[e.module]+str(inputAst)
        else:
           s = str(inputAst)
    elif t == atomictype: 
      atst = inputAst
      p = "if(!wait"+str(atst.wnum)+"){\n"
      s+= mkindent(p,tabs)
      p = "mutex"+str(atst.wnum)+".requestEntry(0);\nwait"+str(atst.wnum)+" = true;\n"
      s+= mkindent(p,tabs+1)
      s+= mkindent("}",tabs)
      s+= mkindent("if (mutex"+str(atst.wnum)+".clearToEnter(0)) {\n",tabs)
      for stmt in atst.stmts: 
        s+= codeGen(stmt,tabs+1,symtab,stages,ename)
      s+= mkindent("mutex"+str(atst.wnum)+".exit(0);\n",tabs+1)
      s+= mkindent("}\n",tabs)
    elif t == numtype:
       s = str(inputAst)
    elif t == restype:
       s = str(inputAst)
    elif t == bvaltype:
       s = str(inputAst)
    elif t == arithtype:
       s = "("+codeGen(inputAst.lexp,0,symtab,stages,ename) +" " + str(inputAst.op) + " "+ codeGen(inputAst.rexp,0,symtab,stages,ename)+")"      
    elif t == rvtype:
       if str(getEntry(inputAst.varname,symtab).dtype) == 'int':
         s = "Integer.parseInt("+rvgetCodegen(inputAst.varname,inputAst.access)+")"
       else:
         s = rvgetCodegen(inputAst.varname,inputAst.access)
    elif t == evnttype :
      event = inputAst 
      ename = event.name
      #print(event)
      vs = getVars(event.pre)
      for var in vs:
          e = getEntry(var[0],symtab).scope
          if e == MULTI_READER:
	     m = checknull(rvgetCodegen(var.varname,var.access),stages,ename)+"\n"
             cast = ""
             lbr = ""
             rbr = ""
             if str(getEntry(var[0],symtab).dtype) == 'int':
                cast = "Integer.parseInt"
                lbr = "("
                rbr = ")"
             m+= str(var[0])+ " = "+cast+lbr+(rvgetCodegen(var.varname,var.access))+rbr+";\n"
             s+= mkindent(m,tabs)
          elif e == MULTI_WRITER:
             cast = ""
             lbr = ""
             rbr = ""
             if str(getEntry(var[0],symtab).dtype) == 'int':
                cast = "Integer.parseInt"
                lbr = "("
                rbr = ")"
	     m = checknull(mwgetCodegen(var[0],symtab),stages,ename)+"\n"
             m+= str(var[0])+ " = "+cast+lbr+(mwgetCodegen(var[0],symtab))+rbr+";\n"
             s+= mkindent(m,tabs)
      s += mkindent("if ("+ codeGen(event.pre,0,symtab,stages,ename)+"){\n",tabs)

      for stmt in event.eff:
          #s+= str(stmt)
          s+= codeGen(stmt,tabs+1,symtab,stages,ename)
      s+= mkindent("continue;",tabs+1)
      s+= mkindent("}",tabs)
    elif t == moduletype:
       pass
    elif t == condtype :
       cond = inputAst
       if cond.rexp is not None:
         s += "("+codeGen(cond.lexp,0,symtab,stages,ename) + " "+ str(cond.op) + " "+ codeGen(cond.rexp,0,symtab,stages,ename)+")"
       elif cond.op is not None:
         s += str(cond.op) +"(" +codeGen(cond.lexp,0,symtab,stages,ename)+")"
       else:
         s+=  codeGen(cond.lexp,0,symtab,stages,ename)
    elif t == exprtype:
       pass
    elif t == functype:
       funcname = str(inputAst.name)
       if funcname == 'newPos':
         funcname = "new ItemPosition"
       m = funcname+"("
       if len(inputAst.args) == 0 :
          m+= ")"
       else:
         if funcname == 'new ItemPosition':
            m+= '"temp",' 
         for i in range(len(inputAst.args)-1) :
           arg = inputAst.args[i] 
           m+= codeGen(arg,0,symtab,stages,ename)+", "
 
         m+= codeGen(inputAst.args[-1],0,symtab,stages,ename) +")"
       if inputAst.isstmt :
          m = mkindent(m+";\n",tabs)
          nc = ""
          for i in range(len(inputAst.args)) :
            arg = inputAst.args[i] 
            v = getVars(arg)
            for var in v:
                nc+= checknull(rvgetCodegen(var[0],var[1]),stages,ename)+"\n"
          s+= mkindent(nc,tabs) 
       s+= m         
    elif t == atomictype:
       pass
    elif t == asgntype :
       lv =  getVars(inputAst.lvar)
       rv = getVars(inputAst.rexp) 
       e = getEntry(lv[0][0],symtab).scope
       for var in rv: 
          e = getEntry(var[0],symtab).scope
          if e == MULTI_READER:
	     m = checknull(rvgetCodegen(var.varname,var.access),stages,ename)+"\n"
             cast = ""
             lbr = ""
             rbr = ""
             if str(getEntry(var[0],symtab).dtype) == 'int':
                cast = "Integer.parseInt"
                lbr = "("
                rbr = ")"
             m+= str(var[0])+ " = "+cast+lbr+(rvgetCodegen(var.varname,var.access))+rbr+";\n"
             s+= mkindent(m,tabs)
          elif e == MULTI_WRITER:
             cast = ""
             lbr = ""
             rbr = ""
             if str(getEntry(var[0],symtab).dtype) == 'int':
                cast = "Integer.parseInt"
                lbr = "("
                rbr = ")"
	     m = checknull(mwgetCodegen(var[0],symtab),stages,ename)+"\n"
             m+= str(var[0])+ " = "+cast+lbr+(mwgetCodegen(var[0],symtab))+rbr+";\n"
             s+= mkindent(m,tabs)
        
       s+=  mkindent(codeGen(inputAst.lvar,0,symtab,stages,ename)+" = "+codeGen(inputAst.rexp,0,symtab,stages,ename)+";",tabs)
       if e == MULTI_READER: 
         s+= mkindent(rvputCodegen(inputAst.lvar),tabs) 
       if e == MULTI_WRITER: 
         s+= mkindent(mwputCodegen(inputAst.lvar),tabs) 
    elif t == mfasttype :
       
        modname = moduleprefix[inputAst.modfunc[:str(inputAst.modfunc).find('.')]]
        newfunc = funcAst(inputAst.modfunc[str(inputAst.modfunc).find('.')+1:],inputAst.args)
        
        l = (str(modname)+codeGen(newfunc,0,symtab,stages,ename))
        if inputAst.isstmt :
           l = mkindent(l+";",tabs)
           nc = ""
           for i in range(len(inputAst.args)) :
             arg = inputAst.args[i] 
             v = getVars(arg)
             for var in v:
                nc+= checknull(rvgetCodegen(var[0],var[1]),stages,ename)+"\n"
           s+= mkindent(nc,tabs)
        s += l
    elif t == itetype :
       ite = inputAst
       istr = "if("+ codeGen(ite.cond,0,symtab,stages,ename) +") {\n"
       for stmt in ite.t :
         istr += codeGen(stmt,1,symtab,stages,ename)
       istr+= "}\n"
       if ite.e is not None:
          istr+= "else {\n"
          for stmt in ite.e : 
            istr += codeGen(stmt,1,symtab,stages,ename)
          istr+= "}\n"
       s+= mkindent(istr,tabs)
       pass
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
