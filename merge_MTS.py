"""Merge MTS files into one

Reason:
Camcorders often produce a collection of files for each recording. They are known as MTS files and typically only cover 10 minutes each. For longer recordings one therefore has to merge them into one file before it is possible to convert or edit into something useful that can be shared.

This script will merge all MTS files in the current directory into one output MTS file.

Usage:
   python merge_MTS.py <output_name> [quality]

This will merge all MTS file in the current directory into one name <output_name>.

The order will follow the default numerical enumeration of MTS files i.e.
00000.MTS, 00001.MTS, ... 

If no output name is specified the result will be stored in the default name: combined.MTS and combined.mp4

This works on Ubuntu20.10, python3.8

Ole Nielsen - 7 April 2019, 1 July 2020

"""

import sys, os, argparse

# Get output filename
default_output_rootfilename = 'combined'

quality_options = ['lossless', 'high', 'medium', 'low']


#args = sys.argv


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
parser.add_argument('-o', '--output_name', type=str, help='The base filename you want the merged and converted files to be')
parser.add_argument('-q', '--quality', type=str, choices=quality_options, help=f'Set the desired quality of the compressed output file. Allowed values are {quality_options}')
args = parser.parse_args()
if args.verbose:
    print('verbosity turned on')

print(args)

if args.output_name is None:
    output_name = default_output_rootfilename 
else:
    output_name = args.output_name

if args.quality is None:
    quality = 'high'
else:
    quality = args.quality
    
print(f'output_name = {output_name}')
print(f'quality = {quality}')


# Sanitize output_filename
root, ext = os.path.splitext(output_name)
if ext == 'mp4':
    pass
if ext == '':
    output_filename = root + '.mp4'
else:
    msg = 'Given output filename (%s) must have extension .mp4 or no extension' % output
    raise Exception(msg)

MTS_filename = root + '.MTS'
MP4_filename = root + '.mp4'

print(f'Output files are {MTS_filename} and {MP4_filename}')


# Find input files

MTSlist = []
for filename in os.listdir('.'):
    if filename.endswith('.MTS'):
        MTSlist.append(filename)

if len(MTSlist) == 0:
    print('No MTS files found')
    import sys; sys.exit() 
        
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
#conversion_command = 'ffmpeg -i %s -vf yadif=1 -c:a mp3 -ab 192k -vcodec mpeg4 -f mp4 -y -qscale 0 %s' % (MTS_filename, MP4_filename)  # Good quality, but almost as large as MTS.

# From https://stackoverflow.com/questions/24720063/how-can-i-convert-mts-file-avchd-to-mp4-by-ffmpeg-without-re-encoding-h264-v
#conversion_command = 'ffmpeg -i %s -c:v copy -c:a mp3 -strict experimental -b:a 128k %s' % (MTS_filename, MP4_filename)  # Good quality, but may be interlaced

# From ffmpeg manual: https://ffmpeg.org/ffmpeg-filters.html
conversion_command = 'ffmpeg -i %s -vf yadif=1 -c:v h264 -c:a mp3 %s' % (MTS_filename, MP4_filename)  # Good quality, progressive, small
# Try ffmpeg -i input -c:v libx264 -preset slow -crf 22 -c:a copy output.mkv  # -crf 0  is lossless (https://trac.ffmpeg.org/wiki/Encode/H.264), 17 is virtually lossless, 23 is the default, 51 is the worst. 

print(conversion_command)
os.system(conversion_command)

# Good instructions about detecting interlaced videos
# http://www.aktau.be/2013/09/22/detecting-interlaced-video-with-ffmpeg/
#
# ffmpeg -filter:v idet -frames:v 1000 -an -f rawvideo -y /dev/null -i combined.mp4


# This is better
# mediainfo --Inform='Video;%ScanType%,%ScanOrder%,%ScanType_StoreMethod%' combined.mp4
