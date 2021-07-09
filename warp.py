
from .format_call import format_call
from .format_paramater import format_parameter
from .constant import ITEM_GET,STATIC,ATTR_GET
from inspect import signature

@s
class Warper:
    def __init__(self,obj,sig,par,typ,cou=0):
        self.obj         = obj
        self.sig         = sig
        self.par         = par
        self.typ         = typ
        self.cou         = cou
    @classmethod
    def from_obj( self, obj):
        sig = signature(obj)
        par = sig.parameters
        typ = type(obj)
        return self(obj,sig,par,typ)

    def diff( self ,names):
        return self.par.keys()&names


    @property
    def longest( self ):
        return max(self.par.keys())

    @property
    def name( self ):
        return self.obj.__name__

    @property
    def gunique( self ):
        name = "%s%s" % (self.longest,self.cou)
        self.cou+=1
        return name

    def warp( self ,names,mode=ITEM_GET):
        changelog           = self.diff(names.keys())
        arguments           = []
        paramaters_factory  = []
        name_kwargs         = self.gunique
        paramaters_factory.append(name_kwargs)
        for key, item in self.par.items():
            kind    = item.kind
            value   = key
            if key in changelog:
                #func_key,value = format_call(name_kwargs,key,names[key],mode) # :DEAD-CODE:
                func_key,value = format_call(name_kwargs,key,None,mode)
            argument = format_parameter(kind, key, value)
            arguments.append(argument)
        func_block = """
def {fac} ({obj},{par_fac}):
    def {warped}{sig_obj}:
        return {obj}({par_warped})
    return {warped}
"""
        par_warped  = ",".join(arguments)
        name_fac    = self.gunique
        name_obj    = self.gunique
        name_war    = self.gunique
        par_fac     = ",".join(paramaters_factory)
        f_map = dict(
            fac=name_fac,
            obj=name_obj,
            par_fac=par_fac,
            warped=name_war,
            sig_obj=self.sig,
            par_warped=par_warped)
        src         = func_block.format_map(f_map)
        code        = compile(src,"<ast>","exec")
        exec (code)
        self.cou    = 0
        return eval(name_fac)(self.obj,names)

def warp(kwargs):
    def warper(obj):
        return Warper.from_obj(obj).warp(kwargs)
    return warper

def inverse_warp(obj):
    def warp_func(func):
        kwargs = {func.__name__ :func}
        return warp(kwargs)(obj)
    return warp_func

def warp_attrs(cls,register,attributes):
    warper = warp(register)
    new    = dict()
    for name in attributes:
        attr = getattr(cls,name)
        new[name] = warper(attr)
    return new

def warp_attrs_gen(cls,register,attributes):
    warper          = warp(register)
    for name in attributes:
        attr        = getattr(cls,name)
        new_attr    = warper(attr)
        yield name,attr,new_attr
    return warper
"""
def warp_class(cls):#TODO waarp cls in way that i can generate mutiple version of same fuction warped in differently ways
    def warper(reg,attr):
        pass
    return warper
"""
def warp_cls(cls,reg,attributes):
    new_attributes = warp_attrs(cls,reg,attributes)
    return type(cls.__name__,(cls,),new_attributes)



if __name__ == '__main__':

    from std.marker import SimpleRegister



    register = SimpleRegister()
    mark     = register.marker

    @mark.x.y
    def convert_to_cm(x):
        return x*100

    @mark.z
    def multiply(x):
        return x*100000

    @warp(register)
    def sample(x,y,z=1):
        print(x,y,z)
        return (x+y+z)

    @mark.point
    def convert_to_point(cord):
        return cord['row'] * cord["column"] * 4

    class Some():
        @warp(register)
        def seek(self,point):
            # this stuff that you dont have to be changed or subclassed
            print(point)
            pass

    sample(1,2,3)
    obj = Some()
    cord = dict(row=2,column=1)
    r   = obj.seek(cord)
    print("__end__")

