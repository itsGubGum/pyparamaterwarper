

ATTRUBUTES = {'appendbytes', 'appendtext', 'check', 'copy', 'copydir', 'create', 'desc', 'download', 'exists',
              'filterdir', 'getbasic', 'getbytes', 'getdetails', 'getfile', 'getinfo', 'getmeta', 'getospath',
              'getsize',
              'getsyspath', 'gettext', 'gettype', 'geturl', 'glob', 'hash', 'hassyspath', 'hasurl',
              'isdir',
              'isempty', 'isfile', 'islink', 'listdir', 'makedir', 'makedirs', 'match', 'move', 'movedir',
              'open',
              'openbin', 'opendir', 'readbytes', 'readtext', 'remove', 'removedir', 'removetree', 'scandir',
              'setbinfile', 'setbytes', 'setfile', 'setinfo', 'settext', 'settimes', 'touch', 'tree', 'upload',
              'validatepath', 'walk', 'writebytes', 'writefile', 'writetext', }


ARGUMETNS = {"s", "path", "url", "src", "dst", "dst_rul", "src_url", "destination", "src_path", "dst_path", "file_path",
             "dir_path", "file"}


def check_if_attribute_is_public_and_has_path_arguments( k: str, v:any ):
    from types import FunctionType, MethodType
    from inspect import signature
    if k.startswith("__"):
        return False
    if not isinstance(v, (FunctionType, MethodType)):
        return False
    sig = signature(v)
    param = sig.parameters
    return any((arg for arg in ARGUMETNS if arg in param))