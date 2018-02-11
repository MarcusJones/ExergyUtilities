# Add utility dir

import sys
print(sys.version)

mod_path = r"C:\LOCAL_REPO\py_ExergyUtilities"
if mod_path not in sys.path:
	sys.path.append(mod_path)

import RevitUtilities.utility_NEW_LCA as ul
import RevitUtilities.utility_parameters as up
import RevitUtilities.utility_get_elements as uels

reload(up)
reload(ul)
reload(uels)

el_dict = ul.get_sort_all_FamilyInstance(doc)

for k in el_dict:
	print(k,len(el_dict[k]))

cats = [
'Roofs',
'Walls',
'Columns',
'Structural Framing', 
'Doors', 
'Floors', 
'Site', 
'Curtain Systems', 
'Generic Models',
]


for cat in cats:
	print("*** Category".format(cat))
	fname = r"C:\Users\jon\Desktop\temp_BOQ\{}.csv".format(cat)
	this_dict = ul.dict_parameters(el_dict[cat])
	ul.write_dictoflists(fname,this_dict)


#fnam
#fname = r"C:\Users\jon\Desktop\temp_BOQ\temp.csv"
#ul.write_dictoflists(fname,this_dict)




if 0: 
	for k in els:
		print(k,len(els[k]))


	this_el = els['Walls'][0]
	up.table_parameters(this_el)

# for k in els:
	# print("In category:", k)
	# print(this_el)
	#print(this_el)
	# this_el = els[k][0]
	
	# break
# Current namespace
# for i in dir():
	# print(i)

"""
import os
#dirs = os.environ['PATH'].split(os.pathsep)
for d in os.environ['PATH'].split(os.pathsep):
	print(d)


print(sys.path)


#dirs = os.environ['PATH'].split(os.pathsep)
for d in os.environ['PYTHONPATH'].split(os.pathsep):
	print(d)


os.environ['PYTHONPATH'].split(os.pathsep)
"""