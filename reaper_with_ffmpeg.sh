#!/usr/bin/env sh
	
# Starting Reaper with a custom load library (addressing 2022 bug where Reaper can’t render using native video libraries). See https://forums.cockos.com/showthread.php?p=2617432

LD_LIBRARY_PATH=~/ffmpeg/lib ~/opt/REAPER/reaper

