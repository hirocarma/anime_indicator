#!/bin/sh

FFMPEG="/usr/bin/ffmpeg"
PYTHON="/usr/bin/python"

INPUT="$1"
NAME=`basename "$INPUT" | sed 's/\.[^\.]*$//' `
CUT=1
START="hh:mm:ss"
END="hh:mm:ss"

WKDIR=$HOME/anime_indicator
IMG_DIR=$WKDIR/img
IMGSIZE="480x270"

if [ $CUT = 1 ]; then
	$FFMPEG -y -ss $START -to $END -i "$INPUT" -vcodec copy -an $WKDIR/tmp.mp4
	INPUT=$WKDIR/tmp.mp4
fi

if [ -d "$IMG_DIR" ]; then
	rm -rf "$IMG_DIR"
fi
mkdir -p "$IMG_DIR"

# frame
$FFMPEG $OVERWRITE -i "$INPUT" \
		-vf framestep=1 -vsync 0 -q:v 5 -s $IMGSIZE \
		"$IMG_DIR"/image_%05d.jpg

# frame count
cd "$IMG_DIR"
COUNT=`ls -U1 | wc -l`

$PYTHON $WKDIR/hist_feature.py "$IMG_DIR"/ $COUNT > ret_"$NAME".txt
cat ret_"$NAME".txt

exit

