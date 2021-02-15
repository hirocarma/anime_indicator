#!/bin/sh

FFMPEG="/usr/bin/ffmpeg"
PYTHON="/usr/bin/python"

INPUT="$1"

START="00:00:00"
END="00:24:40"

NAME=`basename "$INPUT" | sed 's/\.[^\.]*$//' `
CUT=1
FFMPEG_SKIP=0

WKDIR=$HOME/anime_indicator
IMG_DIR=$WKDIR/img
IMG_OUT_DIR=$WKDIR/img_out
RESULT_DIR=$WKDIR/result

IMGSIZE="480x270"

if [ -d "$IMG_OUT_DIR" ]; then
	rm -rf "$IMG_OUT_DIR"
fi
mkdir -p "$IMG_OUT_DIR"

if [ ! -d "$RESULT_DIR" ]; then
	mkdir "$RESULT_DIR"
fi

# frame
if [ $FFMPEG_SKIP = 0 ]; then

	if [ -d "$IMG_DIR" ]; then
		rm -rf "$IMG_DIR"
	fi
	mkdir -p "$IMG_DIR"

	if [ $CUT = 1 ]; then
		PARM="-ss $START -to $END"
	else
		PARM=" "
	fi

	$FFMPEG $OVERWRITE $PARM -i "$INPUT"  \
			-vf framestep=1 -vsync 0 -q:v 5 -s $IMGSIZE \
			"$IMG_DIR"image_%05d.jpg
fi

$PYTHON $WKDIR/main.py "$IMG_DIR"/ "$IMG_OUT_DIR"/ \
	| tee $RESULT_DIR/ret_"$NAME"_"$START"-"$END"_`date +%m%d%H%M%S`.txt

exit
