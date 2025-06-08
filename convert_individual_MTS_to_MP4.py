"""Convert batch of MTS files into MP4 files

Reason:
Camcorders often produce a collection of files known as MTS files.

This script will convert all MTS files in the current directory into MP4 files with the same basename.

Usage:
   python convert_individual_MTS_to_MP4.py

This will convert all MTS file in the current directory into <basename>.mp4.


This works on Ubuntu20.10, python3.8

Ole Nielsen - 12 May 2021

"""

import sys, os


# Find input files

MTSlist = []
for filename in os.listdir('.'):
    if filename.endswith('.MTS'):
        MTSlist.append(filename.replace(' ', '\\ '))
MTSlist.sort()

for MTS_filename in MTSlist:
    if MTS_filename.endswith('.MTS'):
        basename = MTS_filename[0:-4]
        MP4_filename = basename + '.mp4'

        print('Converting %s to %s' % (MTS_filename, MP4_filename))

        # Now convert to mp4

        # From https://blog.tahvok.com/2013/10/deinterlacing-and-converting-mts-video.html: Deinterlacing
        #conversion_command = 'ffmpeg -i %s -vf yadif=1 -c:a mp3 -ab 192k -vcodec mpeg4 -f mp4 -y -qscale 0 %s' % (MTS_filename, MP4_filename)
        # From ffmpeg manual: https://ffmpeg.org/ffmpeg-filters.html
        conversion_command = 'ffmpeg -i %s -vf yadif=1 -c:v h264 -c:a mp3 %s' % (MTS_filename, MP4_filename)  # Good quality, progressive, small


        print(conversion_command)
        os.system(conversion_command)
        print()


