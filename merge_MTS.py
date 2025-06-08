"""Merge MTS files into one

Reason:
Camcorders often produce a collection of files for each recording. They are known as MTS files and typically only cover 10 minutes each. For longer recordings one therefore has to merge them into one file before it is possible to convert or edit into something useful that can be shared.

This script will merge all MTS files in the current directory into one output MTS file.

usage: merge_MTS.py [-h] [-v] [-o OUTPUT_NAME] [-q {lossless,veryhigh,high,medium,low,verylow}]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -o OUTPUT_NAME, --output_name OUTPUT_NAME
                        The base filename for the merged and converted files
  -q {lossless,veryhigh,high,medium,low,verylow}, --quality {lossless,veryhigh,high,medium,low,verylow}
                        Set the desired quality of the compressed output file.

This will merge all MTS file in the current directory into one name <output_name>.

The order will follow the default numerical enumeration of MTS files i.e.
00000.MTS, 00001.MTS, ... 

If no output name is specified the result will be stored in the default name: combined.MTS and combined.mp4

Handy command to detect interlaced videos
mediainfo --Inform='Video;%ScanType%,%ScanOrder%,%ScanType_StoreMethod%' combined.mp4


This works on Ubuntu21.04, python3.8

Ole Nielsen - 7 April 2019, 1 July 2020, 29 September 2021

"""

import time, sys, os, argparse

# Defaults
default_output_rootfilename = 'combined'
default_quality = 'high'

quality_map = {
    'lossless': None,                            # Copy the video across   
    'veryhigh': {'crf': 19, 'preset': 'slower'},
    'high': {'crf': 21, 'preset': 'slow'},       
    'medium': {'crf': 23, 'preset': 'medium'},   # ffmpeg default
    'low': {'crf': 25, 'preset': 'fast'},
    'verylow': {'crf': 27, 'preset': 'faster'}}                              

# Options for crf are 0 (lossless) to 51 (worst). 
# The default for mpeg is 23 (https://trac.ffmpeg.org/wiki/Encode/H.264, https://ffmpeg.org/ffmpeg-filters.html) 
# Options for -preset are 
# ultrafast
# superfast
# veryfast
# faster
# fast
# medium – default preset
# slow
# slower
# veryslow

quality_options = quality_map.keys()


# Parse commandline arguments

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
parser.add_argument('-o', '--output_name', type=str, help='The base filename for the merged and converted files')
parser.add_argument('-q', '--quality', type=str, choices=quality_options, help=f'Set the desired quality of the compressed output file.')
args = parser.parse_args()
if args.verbose:
    print('verbosity turned on')

print(args)

if args.output_name is None:
    output_name = default_output_rootfilename 
else:
    output_name = args.output_name

if args.quality is None:
    quality = default_quality
else:
    quality = args.quality
    
print(f'output_name = {output_name}')
print(f'quality = {quality}')

# Sanitize output_filename
root, ext = os.path.splitext(output_name)
print('ext', ext)
if ext == '.mp4':
    pass
elif ext == '':
    output_filename = root + '.mp4'
else:
    msg = f'Given output filename (output_name) must have extension .mp4 or no extension'
    raise Exception(msg)

# Define quality parameters and derived filenames
if quality == 'lossless':
    quality_str = f'quality={quality}'
else:        
    preset = quality_map[quality]['preset']
    crf = quality_map[quality]['crf']
    quality_str = f'quality={quality}_crf={crf}_preset={preset}'
    
MTS_filename = root + f'_{quality_str}' + '.MTS'
MP4_filename = root + f'_{quality_str}' + '.mp4'

print(f'Output files are {MTS_filename} and {MP4_filename}')


# Find input files

MTSlist = []
for filename in os.listdir('.'):
    if filename.endswith('.MTS'):
        MTSlist.append(filename.replace(' ', '\\ '))    

if len(MTSlist) == 0:
    print('No MTS files found')
    work_to_do = False
else:
    work_to_do = True
        
MTSlist.sort()


# Generate merge command
# See https://stackoverflow.com/questions/44798419/ffmpeg-conversion-from-h264-to-mp4-playing-too-fast/44799078#44799078 re frame rate
# Example could be 'ffmpeg -r 30 -i "concat:00007.MTS|00008.MTS|00009.MTS|00010.MTS" -c copy AKRG10.MTS'
# This works but it is weird because ffprobe <MTS file> reveals that the framerate is 25 fps.

if work_to_do:
    merge_command = 'ffmpeg -r 30 -i "concat:'
    for filename in MTSlist:
        merge_command += filename + '|'

    merge_command = merge_command[:-1]  # Strip off trailing '|' character
    merge_command += '" -c copy %s' % MTS_filename    


    # Execute the command
    print(merge_command)
    os.system(merge_command)

    print('Done merging %s into %s' % (MTSlist, MTS_filename))
    print('Converting to %s' % MP4_filename)

    # Convert to mp4 according to specified quality
    if quality == 'lossless':
        conversion_command = f'ffmpeg -i {MTS_filename} -c:v copy -c:a mp3 {MP4_filename}'    
    else:
        conversion_command = f'ffmpeg -i {MTS_filename} -vf yadif=1 -c:v h264 -preset {preset} -crf {crf} -c:a mp3 {MP4_filename}'

    print(conversion_command)
    timestamp = time.time()
    os.system(conversion_command)
    time_elapsed = time.time() - timestamp 

    # Uncomment if time stamp is required
    #filename = f'time_{quality}={time_elapsed:.2f}s'
    #fid = open(filename, 'w')
    #fid.write('Time: %f\n' % time_elapsed)
    #fid.close()    
