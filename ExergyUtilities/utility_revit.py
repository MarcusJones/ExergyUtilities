# ExergyUtilities
# Copyright (c) 2010, B. Marcus Jones <>
# All rights reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""The :mod:`xx` module 
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:



from config import *

import logging.config
import unittest
from win32com.client import Dispatch
import clr
#from Autodesk.Revit.DB import *
from exergy_frame.tests.utility_inspect import get_self, get_parent, listObject
import sys

sys.path.append(r'D:\Apps\Autocad Plant 3D\Revit 2015')

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUIMacros')
import Autodesk.Revit.DB as rdg
#from Autodesk.Revit.DB.Architecture import *
#from Autodesk.Revit.DB.Analysis import *

print(rdg)
print(dir(rdg))
print(rdg.__doc__)
print(rdg.__name__)
print(rdg.__file__)

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
selection = list(__revit__.ActiveUIDocument.Selection.Elements)

#===============================================================================
# Code
#===============================================================================
class MyClass(object):
    """This class does something for someone.
    """
    def __init__(self, aVariable):
        pass

class MySubClass(MyClass):
    """This class does

    """
    def __init__(self, aVariable):
        super(MySubClass,self).__init__(aVariable)
    def a_method(self):
        """Return the something to the something."""
        pass

def some_function():
    """Return the something to the something."""
    pass
