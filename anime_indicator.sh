#!/bin/sh

FFMPEG="/usr/bin/ffmpeg"
PYTHON="/usr/bin/python"

INPUT="$1"

START="00:00:00"
END="00:24:40"

NAME=`basename "$INPUT" | sed 's/\.[^\.]*$//' `
CUT=1

WKDIR=$HOME/anime_indicator
IMG_DIR=$WKDIR/img
IMGSIZE="480x270"

if [ $CUT = 1 ]; then
	PARM="-ss $START -to $END"
else
	PARM=" "
fi

if [ -d "$IMG_DIR" ]; then
	rm -rf "$IMG_DIR"
fi
mkdir -p "$IMG_DIR"

# frame
$FFMPEG $OVERWRITE $PARM -i "$INPUT"  \
		-vf framestep=1 -vsync 0 -q:v 5 -s $IMGSIZE \
		"$IMG_DIR"/image_%05d.jpg

# frame count
cd "$IMG_DIR"
COUNT=`ls -U1 | wc -l`
echo "frame count: $COUNT"

$PYTHON $WKDIR/hist_feature.py "$IMG_DIR"/ $COUNT | tee $WKDIR/result/ret_"$NAME".txt

exit
