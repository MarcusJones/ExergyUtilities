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


def print_table(table, head = False, width=None):
    
    s = [[str(e) for e in row] for row in table]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:<{}}}'.format(x) for x in lens)

    if head:
        head_break = ['*' * len for len in lens] 
        s.insert(1,head_break)
    
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))

def print_table_dicts(data_dict):
    keys=list(data_dict[0].keys())
    table_rows = keys
    this_table = list()
    this_table.append(keys)
    for item in data_dict:
        #print(keys)
        #print(item)
        for key in keys:
            pass
            #print(item[key],type(item[key]))
            
            
        
        
        
        this_row = [item[key] for key in keys]
        #print(this_row) 
        this_table.append(this_row)
        #table_rows.append(this_row)
    
    print_table(this_table,True)

#----- Following is from 
#https://www.calazan.com/python-function-for-displaying-a-list-of-dictionaries-in-table-format/

from operator import itemgetter

def OLD_print_table_dicts(data,
                    keys=None,
                    header=None,
                    sort_by_key=None,
                    sort_order_reverse=False):
    """Takes a list of dictionaries, formats the data, and returns
    the formatted data as a text table.

    Required Parameters:
        data - Data to process (list of dictionaries). (Type: List)
        keys - List of keys in the dictionary. (Type: List)

    Optional Parameters:
        header - The table header. (Type: List)
        sort_by_key - The key to sort by. (Type: String)
        sort_order_reverse - Default sort order is ascending, if
            True sort order will change to descending. (Type: Boolean)
    """
    if not keys:
        keys=list(data[0].keys())
    
    # Sort the data if a sort key is specified (default sort order
    # is ascending)
    if sort_by_key:
        data = sorted(data,
                      key=itemgetter(sort_by_key),
                      reverse=sort_order_reverse)

    # If header is not empty, add header to data
    if header:
        # Get the length of each header and create a divider based
        # on that length
        header_divider = []
        for name in header:
            header_divider.append('-' * len(name))

        # Create a list of dictionary from the keys and the header and
        # insert it at the beginning of the list. Do the same for the
        # divider and insert below the header.
        header_divider = dict(zip(keys, header_divider))
        data.insert(0, header_divider)
        header = dict(zip(keys, header))
        data.insert(0, header)

    column_widths = []
    for key in keys:
        column_widths.append(max(len(str(column[key])) for column in data))

    # Create a tuple pair of key and the associated column width for it
    key_width_pair = zip(keys, column_widths)

#     format = ('%-*s ' * len(keys)).strip() + '\n'
#     formatted_data = ''
#     for element in data:
#         data_to_format = []
#         # Create a tuple that will be used for the formatting in
#         # width, value format
#         for pair in key_width_pair:
#             data_to_format.append(pair[1])
#             data_to_format.append(element[pair[0]])
#         formatted_data += format % tuple(data_to_format)
#     return formatted_data
    print_table(data)
# 
# # Test
# if __name__ == '__main__':
#     header = ['Name', 'Age', 'Sex']
#     keys = ['name', 'age', 'sex']
#     sort_by_key = 'age'
#     sort_order_reverse = True
#     data = [{'name': 'John Doe', 'age': 37, 'sex': 'M'},
#             {'name': 'Lisa Simpson', 'age': 17, 'sex': 'F'},
#             {'name': 'Bill Clinton', 'age': 57, 'sex': 'M'}]
# 
#     print format_as_table(data,
#                           keys,
#                           header,
#                           sort_by_key,
#                           sort_order_reverse)


