from . constant import ATTR_GET,ITEM_GET,STATIC

def _format_call( v, k, i, mode ):
    return _fromat[mode](v, k, i)

def format_item_get( v, k, i ):
    return f"{v}['{k}']({i})"

def format_attr_get( v, k, i ):
    return f"{v}.{k}({i})"

def format_static( v, k, i ):
    return f"{k}({i})"

_fromat = {ITEM_GET: format_item_get, ATTR_GET: format_attr_get, STATIC: format_static}

def push_name( n ):
    return f'_{n}'

def format_call( self, name, key, mode ):
    if mode == STATIC:
        key = push_name(name)
    if key is None:
        key = name
    formated_call = _format_call(self, key, name, mode)
    return key, formated_call