"""Merge MTS files into one

Reason:
Camcorders often produce a collection of files for each recording. They are known as MTS files and typically only cover 10 minutes each. For longer recordings one therefore has to merge them into one file before it is possible to convert or edit into something useful that can be shared.

This script will merge all MTS files in the current directory into one output MTS file.

Usage:
   python merge_MTS.py <output_name>

This will merge all MTS file in the current directory into one name <output_name>.

The order will follow the default numerical enumeration of MTS files i.e.
00000.MTS, 00001.MTS, ... 

If no output name is specified the result will be stored in the default name: combined.MTS and combined.mp4

This works on Ubuntu20.10, python3.8

Ole Nielsen - 7 April 2019, 1 July 2020

"""

import sys, os

# Get output filename
default_output_rootfilename = 'combined'
args = sys.argv


assert len(args) <= 2, 'You must specify max one argument - the output filename. You specified %s' %str(args)

if len(args) == 2:
    output = args[1]
else:
    output = default_output_rootfilename    

# Sanitize
root, ext = os.path.splitext(output)
if ext == 'mp4':
    pass
if ext == '':
    output_filename = root + '.mp4'
else:
    msg = 'Given output filename (%s) must have extension .mp4 or no extension' % output
    raise Exception(msg)


MTS_filename = root + '.MTS'
MP4_filename = root + '.mp4'

print(MTS_filename, MP4_filename)


# Find input files

MTSlist = []
for filename in os.listdir('.'):
    if filename.endswith('.MTS'):
        MTSlist.append(filename)
MTSlist.sort()

# Generate merge command
# See https://stackoverflow.com/questions/44798419/ffmpeg-conversion-from-h264-to-mp4-playing-too-fast/44799078#44799078 re frame rate
# Example could be 'ffmpeg -r 30 -i "concat:00007.MTS|00008.MTS|00009.MTS|00010.MTS" -c copy AKRG10.MTS'
# This works but it is weird because ffprobe <MTS file> reveals that the framerate is 25 fps.

merge_command = 'ffmpeg -r 30 -i "concat:'

for filename in MTSlist:
    merge_command += filename + '|'

merge_command = merge_command[:-1]  # Strip off trailing '|' character
merge_command += '" -c copy %s' % MTS_filename    
print(merge_command)

# Execute the command
os.system(merge_command)

print('Done merging %s into %s' % (MTSlist, MTS_filename))
print('Converting to %s' % MP4_filename)

# Now convert to mp4
# Source: https://stackoverflow.com/questions/24720063/how-can-i-convert-mts-file-avchd-to-mp4-by-ffmpeg-without-re-encoding-h264-v
# ffmpeg -i input.m2ts -c:v copy -c:a aac -strict experimental -b:a 128k output.mp4

# Both seem to work
#conversion_command = 'ffmpeg -i %s -c:v copy -c:a copy -strict experimental -b:a 128k %s' % (MTS_filename, MP4_filename)
#conversion_command = 'ffmpeg -i %s -c:v copy -c:a mp3 -strict experimental -b:a 128k %s' % (MTS_filename, MP4_filename)

# From https://blog.tahvok.com/2013/10/deinterlacing-and-converting-mts-video.html: Deinterlacing
#conversion_command = 'ffmpeg -i %s -vf yadif=1 -acodec mp3 -ab 192k -vcodec mpeg4 -f mp4 -y -qscale 0 %s' % (MTS_filename, MP4_filename)
conversion_command = 'ffmpeg -i %s -vf yadif=1 -c:a mp3 -ab 192k -vcodec mpeg4 -f mp4 -y -qscale 0 %s' % (MTS_filename, MP4_filename)

print(conversion_command)
os.system(conversion_command)

# Good instructions about detecting interlaced videos
# http://www.aktau.be/2013/09/22/detecting-interlaced-video-with-ffmpeg/
#
# ffmpeg -filter:v idet -frames:v 1000 -an -f rawvideo -y /dev/null -i combined.mp4
