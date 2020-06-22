#/bin/env python

import os

print('starting')

basedir = os.path.expanduser('~/Music/SelfMade')
print('Removing wav files already converted to mp3 from %s' % basedir)

for dirname, subdirlist, filelist in os.walk(basedir):
    #print('Searching directory: %s' % dirname)
    for filename in filelist:
        if filename.endswith('.WAV') or filename.endswith('wav'):
            basename, ext = os.path.splitext(filename)
            candidate = os.path.join(basedir, dirname, basename + '.mp3')
            #print('Looking for ' + candidate)
            if os.path.isfile(candidate):
                print('Found', candidate, filename)
                


