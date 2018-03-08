# TEST MODULE
#===============================================================================
#--- SETUP Config
#===============================================================================
from config.config import *
import unittest

#===============================================================================
#--- SETUP Logging
#===============================================================================
import logging.config
print(ABSOLUTE_LOGGING_PATH)
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
my_logger = logging.getLogger()
my_logger.setLevel("DEBUG")


#===============================================================================
#--- SETUP Add parent module
#===============================================================================
#from os import sys, path
import os
# Add parent to path
if __name__ == '__main__' and __package__ is None:
    this_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.append(this_path)
    logging.debug("ADDED TO PATH: ".format(this_path))


#===============================================================================
#--- SETUP Standard modules
#===============================================================================
from ExergyUtilities.utility_inspect import get_self

#===============================================================================
#--- SETUP Custom modules
#===============================================================================
from ExergyUtilities.utility_inspect import get_self
from jinja2 import Template

#app.jinja_env.trim_blocks = True
#app.jinja_env.lstrip_blocks = True
#===============================================================================
#--- Directories and files
#===============================================================================
#curr_dir = path.dirname(path.abspath(__file__))
#DIR_SAMPLE_IDF = path.abspath(curr_dir + "\..\.." + "\SampleIDFs")
#print(DIR_SAMPLE_IDF)

"""
<table style="width:100%">
  <!-- table header -->
  {% if history_list %}
  <tr>
     {% for key in history_list[0] %}
     <th> {{ key }} </th>
     {% endfor %}
  </tr>
  {% endif %}

  <!-- table rows -->
  {% for dict_item in history_list %}
  <tr>
     {% for value in dict_item.values() %}
     <td> {{ value }} </td>
     {% endfor %}
  </tr>
  {% endfor %}
"""        

tmplt_title = Template(
"""
<b>{{_title}}</b><br><br>
<!-- FullName:{{_full_name}}-->
""")


tmplt_row = Template(
"""
<table border="1" cellpadding="4" cellspacing="0">
  <tr>{%- for item in data -%}{%- if loop.first -%}<td></td>{% endif %} 
    <td align="right">{{item}}</td>{% endfor %}
  </tr>""")



tmplt_table = Template(
"""
<table border="1" cellpadding="4" cellspacing="0">
       {% for row in rows %}
  <tr>{%- if loop.first -%}<td></td>{% endif %} 
                {%- for item in row %}
    <td align="right">{{item}}</td>
                {%- endfor %}
  </tr>
       {%- endfor %}
</table>
""")

 


#===============================================================================
#--- Unit testing
#===============================================================================
print("Test")
class BasicTest(unittest.TestCase):
    def setUp(self):
        #print "**** TEST {} ****".format(get_self())
        my_logger.setLevel("CRITICAL")
        print("Setup")
         
        curr_path = os.path.dirname(os.path.realpath(__file__))
        curr_path = os.path.abspath(curr_path + "\..\..\ExcelTemplates\Table test.xlsx")
         
        my_logger.setLevel("DEBUG")
         
         
    def test010_SimpleCreation(self):
        print("**** TEST {} ****".format(get_self()))
        template = Template('Hello {{ name }}!')
        result = template.render(name='John Doe')
        print(result)
        


#--- This line makes is more clear how to run in Eclipse
#--- Check to make sure this runs first (Run as -> python)
if __name__ == '__main__': 
    unittest.main()

