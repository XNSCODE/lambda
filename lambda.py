#!/usr/bin/python3 or python2
#coding=utf-8

import types
import zlib
import marshal
import base64
import sys
import six

def reduce_code(c,cc=None):
    if cc is None: xx = c.co_code
    else: xx = cc
    new_code = [
        c.co_argcount,
        c.co_nlocals,
        c.co_stacksize,
        c.co_flags,
        xx,
        c.co_consts,
        c.co_names,
        c.co_varnames,
        c.co_filename,
        c.co_name,
        c.co_firstlineno,
        c.co_lnotab,
        c.co_freevars,
        c.co_cellvars,
    ]
    if six.PY3:
        try:
            new_code[1:1] = [
                c.co_posonlyargcount,
                c.co_kwonlyargcount
            ]
        except:
            new_code.insert(1, c.co_kwonlyargcount)
    if not cc is None:
        return types.CodeType(*new_code)
    return tuple(new_code)

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit("\npython2 lambda.py /sdcard/folder/file.py\npython lambda.py /sdcard/folder.py\n\n")
    with open(sys.argv[1]) as f: c = f.read()
    _ = lambda x,y: compile(x, y, 'exec')
    x = ['func_code', '__code__'][six.PY3]
    co = _(c, sys.argv[1])
    cc = bytearray(len(co.co_code))
    cc[:] = co.co_code[:]
    cc.append(0x9)
    if six.PY3: cc = bytes(cc)
    else: cc = str(cc)
    nc = reduce_code(co, cc)
    c = repr(base64.b64encode(zlib.compress(marshal.dumps(nc))))
    c = "try: exec(__import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b64decode({}))))\nexcept Exception as e: print(str(e))".format(c)
    c = _(c, sys.argv[0])
    n = reduce_code(c)
    c = ",".join([repr(i) for i in n])
    with open('lambda-enc.py', 'w') as f: f.write("_=(lambda x:x);code=type(_.{});_.{}=code({});_()".format(x, x, c))
    del c, x, n, nc, cc
