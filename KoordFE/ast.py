#abstract syntax trees. 
from symtab import * 
LOCAL = -1
MULTI_WRITER = -2
MULTI_READER = -3
CONTROLLER = -4

pgmtype = 'pgm'
decltype = 'decl'
rvdecltype = 'rvdecl'
inittype = 'init'
evnttype = 'evnt'
moduletype = 'mdl'
condtype = 'cond'
exprtype = 'expr'
functype = 'func' 
atomictype = 'atom'

#program
class pgmAst(list):
    def __init__(self,name,modules,awdecls,ardecls,locdecls,init,events):
        self.name = name 
        self.modules = modules 
        self.awdecls = awdecls 
        self.ardecls = ardecls 
        self.locdecls = locdecls 
        self.init = init
        self.events = events 

    def __repr__(self):
        name_str =  self.name
        module_str = ""
        for module in self.modules:
            module_str+=str(module)+"\n"
        awdecl_str = "allwrite:\n"
        for decl in self.awdecls:
            awdecl_str+=str(decl)+"\n"
        ardecl_str = "allread:\n"
        for decl in self.ardecls:
            ardecl_str+=str(decl)+"\n"
        locdecl_str = "local:\n"
        for decl in self.locdecls:
            locdecl_str+=str(decl)+"\n"
        event_str = ""
        for event in self.events:
            event_str+=str(event)+"\n"


        return (name_str+"\n"+module_str+"\n"+awdecl_str+"\n"+ardecl_str+"\n"+locdecl_str+str(self.init)+event_str)


#flags = ([list of module names], whether the program has shared variables)
    def getflags(self):
        modules = []
        hasShared = False
        if self.modules == []:
            pass
        else :
            for module in self.modules: 
               modules.append(module.getName());
        if self.awdecls == []:
            pass
        else :
            hasShared = True 
        if self.ardecls == []:
            pass
        else :
            hasShared = True 
        return (modules, hasShared) 

    def get_type(self):
        return pgmtype 

class mfast(list):
    def __init__(self,modfunc,args):
       self.modfunc = modfunc
       self.args = args

    def __repr__(self):
        #modname = "s"#str(self.modfunc)[(str(self.modfunc)).index('.'):-1]
        m = str(self.modfunc)+"("
        if len(self.args) == 0 :
           m+= ")"
        else: 
          for i in range(len(self.args)-1) :
            m+= str(self.args[i])+", "
          m+= str(self.args[-1]) +")"
        return(m) 

    def get_type(self):
       return moduletype 

class funcAst(list):
    def __init__(self,name,args):
       self.name = name
       self.args = args
    def __repr__(self):
        m = str(self.name)+"("
        if len(self.args) == 0 :
           m+= ")"
        else: 
          for i in range(len(self.args)-1) :
            m+= str(self.args[i])+", "
          m+= str(self.args[-1]) +")"
        return(m) 

    def get_type(self):
       return functype 

class passAst(list):
    def __init__(self):
        pass
    
    def get_type(self):
	return 'pass'


class moduleAst(list):
    def __init__(self,name,actuatordecls,sensordecls):
        self.name = name
        self.actuatordecls = actuatordecls
        self.sensordecls = sensordecls

    def __repr__(self):
        name_str = str(self.name)
        actuator_str = "actuators :"+"\n"
        for decl in self.actuatordecls:
            actuator_str+= str(decl)+"\n"
        sensor_str = "sensors :"+"\n"
        for decl in self.sensordecls:
            sensor_str+= str(decl)+"\n"
        return name_str+":\n"+actuator_str+sensor_str
    

    def getName(self):
	return self.name
 
    def get_type(self):
        return moduletype 

class initAst(object):
    def __init__(self,stmts):
        self.stmts = stmts 

    def __repr__(self):
        init_str = "init:\n"
        for stmt in self.stmts:
            init_str += str(stmt)+"\n"
        return init_str
    
    def get_type(self):
        return inittype 

class stmtAst(list):
    def __init__(self,stype):
        self.stype = stype 
    
    def get_type(self):
        return self.stype 

class atomicAst(stmtAst):
    def __init__(self,wnum,stmts):
        self.stype = atomictype
        self.wnum = wnum
        self.stmts = stmts

    def __repr__(self):
        s = "atomic:"
        for stmt in self.stmts:
           s+= str(stmt)
        return s
    def get_type(self):
        return atomictype


class asgnAst(stmtAst):
    def __init__(self,lvar,rexp):
        self.stype = 'asgn'
        self.lvar = lvar
        self.rexp = rexp

    def __repr__(self):
        return str(self.lvar)+" = "+str(self.rexp)

class iteAst(stmtAst): 
    def __init__(self,cond,t,e):
        self.stype = 'ite'
        self.cond  = cond
        self.t = t
        self.e = e 
    def __repr__(self):
        s = "if "+str(self.cond)+"\n"
        for stmt in self.t:
          s+= str(stmt)
        s += "else"
        for stmt in self.e:
          s+= str(stmt)
        return s 
        
class eventAst(list):
    def __init__(self,name,pre,eff):
        self.name = name
        self.pre = pre
        self.eff = eff

    def __repr__(self):
        
        pre_str = "pre:\n"+str(self.pre)+"\n"
        eff_str = "eff:\n"
        for stmt in self.eff:
            eff_str += str(stmt)+"\n"
        return (self.name+":\n"+pre_str+eff_str)

    def get_type(self):
        return evnttype 

class condAst(list):
    def __init__(self,lexp,rexp=None,op=None):
        self.lexp = lexp
        self.rexp = rexp
        self.op = op
    
    def __repr__(self):
        if self.rexp is not None:
            return "( "+str(self.lexp) +" "+ str(self.op) +" "+str(self.rexp)+" )"
	if self.op is not None: 
	    return "(" + str(self.op)+"( " +str(self.lexp)+" )"+")"
	else: 
	    return "("+str(self.lexp)+")"


    def get_type(self):
        return condtype
 
class exprAst(list):
    def __init__(self,etype,lexp,rexp= None,op= None):
        self.etype = etype
        self.lexp = lexp 
        self.rexp = rexp
        self.op = op
   
    def __repr__(self):
        if self.op is None:
	   return str(self.lexp)
        if self.rexp is None:
	    return str(self.lexp)+ str(self.op)
        if self.lexp is None:
	    return str(self.op) + str(self.rexp)
	else:
            return "( "+str(self.lexp) +" "+ str(self.op) +" "+str(self.rexp)+" )"
    
    def get_type(self):
        return self.etype

class declAst(list):
    def __init__(self,dtype, varname, value= None ,scope=LOCAL):
        self.scope = scope
        self.dtype = dtype
        self.varname = varname
        self.value = value

    def __repr__(self):
        dtype_str = str(self.dtype)+" "
        varname_str = str(self.varname)+" "
	value_str = ""
        if self.value is not None : 
            value_str = "= "+str(self.value)
        return (dtype_str+varname_str+value_str)

    def get_scope(self):
        return self.scope

    def set_scope(self,scope):
        self.scope = scope

    def get_type(self):
        return decltype
 
class mapAst(list):
    def __init__(self,t1,t2, varname,scope=LOCAL):
        self.scope = scope
        self.t1 = t1
        self.t2 = t2
        self.varname = varname
        self.scope = scope

    def __repr__(self):
        dtype_str = "final Map <"+str(self.t1)+" , "
        dtype_str += str(self.t2)+"> "
        varname_str = str(self.varname)+" "
        value_str = "= "+ "new HashMap<" + str(self.t1)+ ","+ str(self.t2)+">()"
        return (dtype_str+varname_str+value_str)

    def get_scope(self):
        return self.scope

    def set_scope(self,scope):
        self.scope = scope

    def get_type(self):
        return 'map' 

class rvdeclAst(list):

    def __init__(self,dtype, varname, owner, value= None ,scope=LOCAL):
        self.scope = scope
        self.dtype = dtype
        self.varname = varname
        self.owner = owner
        self.value = value

    def __repr__(self):
        dtype_str = str(self.dtype)+" "
        varname_str = str(self.varname)+" "
        owner_str = "["+str(self.owner)+"] "
	value_str = ""
        if self.value is not None : 
            value_str = "= "+str(self.value)
        return (dtype_str+varname_str+owner_str+value_str)

    def get_scope(self):
        return self.scope

    def set_scope(self,scope):
        self.scope = scope 

    def get_type(self):
        return rvdecltype

def mkEntry(decl):
    return symEntry(decl.dtype,decl.varname,decl.scope)  

def isAst(ast):
   try:
      t = ast.get_type()
      return True
   except:
      return False 
