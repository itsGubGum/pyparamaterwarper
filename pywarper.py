from inspect import _ParameterKind
from inspect import signature

__all__ = ["warp_cls", "warp", "warp_attrs"]

ITEM_GET = 0
ATTR_GET = 1
STATIC = 2
SELF_GET = 3


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

    _fromat = {ITEM_GET: format_item_get, ATTR_GET: format_attr_get, STATIC: format_static}

    if mode == STATIC:
        key = push_name(name)
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


class Warper:
    def __init__(self, obj, sig, par, typ, cou=0):
        self.obj = obj
        self.sig = sig
        self.par = par
        self.typ = typ
        self.cou = cou

    @classmethod
    def from_obj(self, obj):
        sig = signature(obj)
        par = sig.parameters
        typ = type(obj)
        return self(obj, sig, par, typ)

    def diff(self, names):
        return self.par.keys() & names

    @property
    def longest(self):
        return max(self.par.keys())

    @property
    def name(self):
        return self.obj.__name__

    @property
    def gunique(self):
        name = "%s%s" % (self.longest, self.cou)
        self.cou += 1
        return name

    def warp(self, names, mode=ITEM_GET):
        changelog = self.diff(names.keys())
        arguments = []
        paramaters_factory = []
        name_kwargs = self.gunique
        paramaters_factory.append(name_kwargs)
        for key, item in self.par.items():
            kind = item.kind
            value = key
            if key in changelog:
                # func_key,value = format_call(name_kwargs,key,names[key],mode) # :DEAD-CODE:
                func_key, value = _format_call(name_kwargs, key, None, mode)
            argument = _format_parameter(kind, key, value)
            arguments.append(argument)
        func_block = """
def {fac} ({obj},{par_fac}):
    def {warped}{sig_obj}:
        return {obj}({par_warped})
    return {warped}
"""
        par_warped = ",".join(arguments)
        name_fac = self.gunique
        name_obj = self.gunique
        name_war = self.gunique
        par_fac = ",".join(paramaters_factory)
        f_map = dict(
            fac=name_fac,
            obj=name_obj,
            par_fac=par_fac,
            warped=name_war,
            sig_obj=self.sig,
            par_warped=par_warped)
        src = func_block.format_map(f_map)
        code = compile(src, "<ast>", "exec")
        exec(code)
        self.cou = 0
        return eval(name_fac)(self.obj, names)


def warp(kwargs):
    def warper(obj):
        return Warper.from_obj(obj).warp(kwargs)

    return warper


def warp_attrs(cls, register, attributes):
    warper = warp(register)
    new = dict()
    for name in attributes:
        attr = getattr(cls, name)
        new[name] = warper(attr)
    return new


def warp_cls(cls, reg, attributes):
    new_attributes = warp_attrs(cls, reg, attributes)
    return type(cls.__name__, (cls,), new_attributes)
