from functools import partial
from inspect import (_ParameterKind,
                     _VAR_POSITIONAL,
                     _VAR_KEYWORD,
                     _KEYWORD_ONLY,
                     _POSITIONAL_OR_KEYWORD,
                     _POSITIONAL_ONLY)
from inspect import signature
from enum import IntEnum

class GetMode(IntEnum):
    getItem = 0
    getAttr = 1


def _format_call(self, name, key, mode):
    def format_item_get(v, k, i):
        return f"{v}['{k}']({i})"

    def format_attr_get(v, k, i):
        return f"{v}.{k}({i})"

    def format_static(v, k, i):
        return f"{k}({i})"

    def _format_call(v, k, i, mode):
        return _fromat[mode](v, k, i)

    def push_name(n):
        return f'_{n}'

    _fromat = {GetMode.getItem: format_item_get, GetMode.getAttr: format_attr_get}

    if key is None:
        key = name
    formated_call = _format_call(self, key, name, mode)
    return key, formated_call


_ParameterMapping = {param.value: param.name for param in _ParameterKind}


class _FormatParameters:

    def POSITIONAL_ONLY(*, v, **kwargs):
        """format position only arg"""
        return f"{v}"

    def POSITIONAL_OR_KEYWORD(*, v, **kwargs):
        """format position or keyword arg"""
        return f"{v}"

    def VAR_KEYWORD(*, v, **kwargs):
        """format kwargs"""
        return f"**{v}"

    def VAR_POSITIONAL(*, v, **kwargs):
        """format args"""
        return f"*{v}"

    def KEYWORD_ONLY(*, k, v, **kwargs):
        """format key only arg"""
        return f"{k}={v}"

    def _get(self, item):
        if isinstance(item, int):
            item = _ParameterMapping[item]
        return getattr(self, item)

    __class_getitem__ = _get
    __getitem__ = _get


def _format_parameter(kind, k=None, v=None):
    return _FormatParameters[kind](k=k, v=v)

#TODO support classes (__call__,__init__)
# warp classes methods in batch based on pattern ,return type ,
#TODO tests
def warp_by_name(obj, kwargs, mode=None):
    if mode is None:
        if isinstance(kwargs,dict):
            mode = GetMode.getItem
        else:
            mode = GetMode.getAttr
    sig = signature(obj)
    par = sig.parameters
    cou = 0
    longest = max(par.keys())
    if mode == None:
        if isinstance(kwargs, dict):
            mode = GetMode.getItem
        elif isinstance(kwargs, (object, type)):
            mode = GetMode.getAttr

    def generate_unique_name():
        nonlocal cou
        name = "%s%s" % (longest, cou)
        cou += 1
        return name

    kwargs_keys = dict().keys()
    if isinstance(kwargs, dict):
        kwargs_keys = kwargs.keys()
    elif isinstance(kwargs, type):
        kwargs_keys = kwargs.__dict__.keys()
    elif isinstance(kwargs, object):#TODO fix this line
        kwargs_keys = type(kwargs).__dict__.keys()

    changelog = par.keys() & kwargs_keys
    arguments = []
    paramaters_factory = []
    name_kwargs = generate_unique_name()

    paramaters_factory.append(name_kwargs)
    for key, item in par.items():
        kind = item.kind
        value = key
        if key in changelog:  # formating get (item|attr|static)depend so on
            # func_key,value = format_call(name_kwargs,key,names[key],mode) # :DEAD-CODE:
            func_key, value = _format_call(name_kwargs, key, None, mode)
        argument = _format_parameter(kind, key, value)
        arguments.append(argument)
    # Formating-String
    func_block = """
def {fac} ({obj},{par_fac}):
    def {warped}{sig_obj}:
        return {obj}({par_warped})
    return {warped}
    """
    par_warped = ",".join(arguments)
    function_name = generate_unique_name()
    argument_for_object = generate_unique_name()
    name_war = generate_unique_name()
    par_fac = ",".join(paramaters_factory)
    f_map = dict(
            fac=function_name,
            obj=argument_for_object,
            par_fac=par_fac,
            warped=name_war,
            sig_obj=sig,
            par_warped=par_warped)
    src = func_block.format_map(f_map)
    # Compileing exceuting
    code = compile(src, "<ast>", "exec")
    exec(code)
    return eval(function_name)(obj, kwargs)


def warp(kwargs, mode=None):
    def _newobjct(obj):
        return warp_by_name(obj, kwargs, mode=mode)
    return _newobjct

def dwarp(kwargs,mode=None):
    def _warp(obj):
        def _newobjct(*args,**kws):
            return warp_by_name(obj, kwargs, mode=mode)(*args, **kws)
        return _newobjct
    return _warp



def warp_first_kind(obj, function, kind):
    par = signature(obj).parameters
    key = None
    for k,v in par.items():
        if v.kind ==kind:
            key = k
            break
    if key:
        return warp_by_name(obj, {key:function}, mode=GetMode.getItem)
    return obj

def warp_first_in_kinds(obj,function,kind):
    par = signature(obj).parameters
    key = None
    for k,v in par.items():
        if v.kind in kind:
            key = k
            break
    if key:
        return warp_by_name(obj, {key:function}, mode=GetMode.getItem)
    return obj
def warp_nfirst_in_kinds(obj,functions,kind):
    par     = signature(obj).parameters
    keys    = []
    for k,v in par.items():
        if v.kind  in kind:
            keys.append(k)
    if len(keys)> 0:
        return warp_by_name(obj, {k:v for k,v in zip(keys,functions)}, mode=GetMode.getItem)
    return obj

def warp_first_paramater(obj,function):
    par = signature(obj).parameters
    if len(par)>0:
        key = next(iter(par.keys()))
        return warp_by_name(obj, {key:function}, mode=GetMode.getItem)
    return obj

def warp_nfirst_paramaters(obj,functions):
    par = signature(obj).parameters
    if len (par) > 0:
        return warp_by_name(obj, {k:v for k,v in zip(par.keys(),functions)}, mode=GetMode.getItem)
    return obj


warp_args    = partial(warp_first_kind, kind=_VAR_POSITIONAL)

warp_kwargs = partial(warp_first_kind, kind=_VAR_KEYWORD)
