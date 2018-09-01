#!/bin/sh

ffmpeg -i '%d.png' -s 600x550 -c:v mpeg4 -b:v 1000K out.mp4
