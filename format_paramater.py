from inspect import _ParameterKind

_ParameterMapping = {param.value: param.name for param in _ParameterKind}


class _FormatParameters:

    def POSITIONAL_ONLY( *, v, **kwargs ):
        """format position only arg"""
        return f"{v}"

    def POSITIONAL_OR_KEYWORD( *, v, **kwargs ):
        """format position or keyword arg"""
        return f"{v}"

    def VAR_KEYWORD( *, v, **kwargs ):
        """format kwargs"""
        return f"**{v}"

    def VAR_POSITIONAL( *, v, **kwargs ):
        """format args"""
        return f"*{v}"

    def KEYWORD_ONLY( *, k, v, **kwargs ):
        """format key only arg"""
        return f"{k}={v}"

    def _get( self, item ):
        if isinstance(item, int):
            item = _ParameterMapping[item]
        return getattr(self, item)

    __class_getitem__ = _get
    __getitem__ = _get


def format_parameter( kind, k=None, v=None ):
    return _FormatParameters[kind](k=k, v=v)