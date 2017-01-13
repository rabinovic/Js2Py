# this is based on jsarray.py

from ..base import *
import numpy

@Js
def Int8Array():
    TypedArray = (PyJsInt8Array,PyJsUint8Array,PyJsUint8ClampedArray,PyJsInt16Array,PyJsUint16Array,PyJsInt32Array,PyJsUint32Array,PyJsFloat32Array,PyJsFloat64Array)
    a = arguments[0]
    if isinstance(a, PyJsNumber): # length
        length = a.to_uint32()
        if length!=a.value:
            raise MakeError('RangeError', 'Invalid array length')
        temp = Js(numpy.full(length, 0, dtype=numpy.int8))
        temp.put('length', a)
        return temp
    elif isinstance(a, PyJsString): # object (string)
        temp = Js(numpy.array(list(a.value), dtype=numpy.int8))
        temp.put('length', Js(len(list(a.value))))
        return temp
    elif isinstance(a, PyJsArray): # object (array)
        array = a.to_list()
        for i in xrange(len(array)):
            if array[i].value != None:
                array[i] = int(array[i].value)
            else:
                array[i] = 0
        temp = Js(numpy.array(array, dtype=numpy.int8))
        temp.put('length', Js(len(array)))
        return temp
    elif isinstance(a,PyObjectWrapper): # object (Python object: TypedArray (numpy.ndarray), ArrayBuffer (bytearray), etc)
        if len(arguments) > 1:
            offset = int(arguments[1].value)
        else:
            offset = 0
        if len(arguments) == 3:
            length = int(arguments[2].value)
        else:
            length = len(a.obj)
        temp = Js(numpy.frombuffer(a.obj, dtype=numpy.int8, count=length, offset=offset))
        temp.put('length', Js(length))
        return temp
    temp = Js(numpy.full(0, 0, dtype=numpy.int8))
    temp.put('length', Js(0))
    return temp

Int8Array.create = Int8Array
Int8Array.own['length']['value'] = Js(3)

Int8Array.define_own_property('prototype', {'value': Int8ArrayPrototype,
                                         'enumerable': False,
                                         'writable': False,
                                         'configurable': False})

Int8ArrayPrototype.define_own_property('constructor', {'value': Int8Array,
                                                    'enumerable': False,
                                                    'writable': True,
                                                    'configurable': True})

Int8ArrayPrototype.define_own_property('BYTES_PER_ELEMENT', {'value': Js(1),
                                                    'enumerable': False,
                                                    'writable': False,
                                                    'configurable': False})
