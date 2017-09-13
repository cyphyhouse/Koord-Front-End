

class symEntry(list):
    def __init__(self,dtype,varname,val,scope):
        self.dtype = dtype
        self.varname = varname
        self.val = val
        self.scope = scope

symtab = []



