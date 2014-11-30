from __future__ import print_function

import inspect

def get_self():
    return inspect.stack()[1][3]

def get_parent():
    return inspect.stack()[2][3]

def list_attrs(obj):
    attrs = vars(obj)
    attr_list  = ["{} : {}".format(*item) for item in attrs.items()]
    print(attr_list)
    
def list_object(theObject,cols = 5):
    print("********")
    print(type(theObject))
    items = dir(theObject)
    while(items):
        for i in range(cols):
            if items:
                print("{:<30}".format(items.pop(0)),end='')
        print()