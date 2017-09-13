

class symEntry(list):
    def __init__(self,dtype,varname,scope,owner = '*'):
        self.dtype = dtype
        self.varname = varname
        self.scope = scope
        self.owner = owner

    def __repr__(self):

        return ("symEntry: "+str(self.scope)+" "+str(self.dtype)+" "+str(self.varname))


def getEntry(v,symtab):
    for entry in symtab :
           if(str(v)==str(entry.varname)):
               return entry
    return None
