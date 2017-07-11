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

def print_table(table, width=None):
    
    s = [[str(e) for e in row] for row in table]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:<{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))
    

def print_table_x(table, width=None):
    
    data_table = [[str(e) for e in row] for row in table]

    lengths = [max(map(len, col)) for col in zip(*data_table)]
    numbering = [num for num in range(len(lengths))]
    numbered_lengths = list(zip(numbering,lengths))
    
    #print(numbering)
    #print(numbered_lengths)
    
    format_string = '\t'.join('{{{}:<{}}}'.format(*x) for x in numbered_lengths)
    #print(lengths)
    
    #for row in data_table:
    #    print(row)
    #    print(format_string)
    #    print(format_string.format(*row))
    #    raise
    #raise
    print(format_string)
    table = [format_string.format(*row) for row in data_table]
    print('\n'.join(table))