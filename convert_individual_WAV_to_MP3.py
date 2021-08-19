"""Convert batch of WAV files into MP3 files


This script will convert all WAV files in the current directory into MP3 files with the same basename.

Usage:
   python convert_individual_WAV_to_MP3.py

This will convert all WAV file in the current directory into <basename>.mp3


This works on Ubuntu20.10, python3.8

Ole Nielsen - 19 August 2021

"""

import sys, os


# Find input files

WAVlist = []
for filename in os.listdir('.'):
    if filename.endswith('.WAV') or filename.endswith('.wav'):
        WAVlist.append(filename.replace(' ', '\ '))
WAVlist.sort()

for WAV_filename in WAVlist:
    if WAV_filename.endswith('.WAV') or WAV_filename.endswith('.wav'):
        basename = WAV_filename[0:-4]
        MP3_filename = basename + '.mp3'

        print('Converting %s to %s' % (WAV_filename, MP3_filename))

        conversion_command = 'ffmpeg -i %s -acodec mp3 %s' % (WAV_filename, MP3_filename)


        print(conversion_command)
        os.system(conversion_command)
        print()


