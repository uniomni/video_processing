"""Merge MTS files into one

Reason:
Camcorders often produce a collection of files for each recording. They are known as MTS files and typically only cover 10 minutes each. For longer recordings one therefore has to merge them into one file before it is possible to convert or edit into something useful that can be shared.

This script will merge all MTS files in the current directory into one output MTS file.

Usage:
   python merge_MTS.py <output_name>

This will merge all MTS file in the current directory into one name <output_name>.

The order will follow the default numerical enumeration of MTS files i.e.
00000.MTS, 00001.MTS, ... 

If no output name is specified the result will be stored in the default name: output.MTS

This works on Linux, Ubuntu18.10, python2.7

Ole Nielsen - 7 April 2019
"""

import sys, os

# Get output filename
default_output_filename = 'output'    
args = sys.argv


assert len(args) <= 2, 'You must specify max one argument - the output filename. You specified %s' %str(args)

if len(args) == 2:
    output_filename = args[1]
else:
    output_filename = default_output_filename    

if not output_filename.endswith('.MTS'):
    output_filename = output_filename + '.MTS'
    
print output_filename

# Find input files

MTSlist = []
for filename in os.listdir('.'):
    if filename.endswith('.MTS'):
        MTSlist.append(filename)
MTSlist.sort()

# Generate merge command
# Example could be 'ffmpeg -i "concat:00007.MTS|00008.MTS|00009.MTS|00010.MTS" -c copy AKRG10.MTS'

merge_command = 'ffmpeg -i "concat:'

for filename in MTSlist:
    merge_command += filename + '|'

merge_command = merge_command[:-1]  # Strip off trailing '|' character
merge_command += '" -c copy %s' % output_filename    
print merge_command

# Execute the command
os.system(merge_command)

print 'Done merging %s into %s' % (MTSlist, output_filename)



