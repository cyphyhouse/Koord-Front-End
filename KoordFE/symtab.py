from ast import * 

class symEntry(list):
    def __init__(self,dtype,varname,scope,owner = '*',module = None):
        self.dtype = dtype
        self.varname = varname
        self.scope = scope
        self.owner = owner
        self.module = module

    def __repr__(self):

        return ("symEntry: "+str(self.scope)+" "+str(self.dtype)+" "+str(self.varname) + " "+ str(self.module))

    def set_module(self,module):
        self.module = module 
