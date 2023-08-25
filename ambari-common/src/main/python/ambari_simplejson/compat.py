"""Python 3 compatibility shims
"""
import sys
if sys.version_info[0] < 3:
    PY3 = False
    def b(s):
        return s
    try:
        from io import StringIO
    except ImportError:
        from io import StringIO
    BytesIO = StringIO
    text_type = str
    binary_type = str
    string_types = (str,)
    integer_types = (int,)
    chr = chr
    reload_module = reload
else:
    PY3 = True
    if sys.version_info[:2] >= (3, 4):
        from importlib import reload as reload_module
    else:
        from imp import reload as reload_module
    def b(s):
        return bytes(s, 'latin1')
    from io import StringIO, BytesIO
    text_type = str
    binary_type = bytes
    string_types = (str,)
    integer_types = (int,)
    chr = chr

long_type = integer_types[-1]
