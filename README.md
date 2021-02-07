# anime_indecator

An attempt to quantify the amount of work that goes into creating a picture in an animation.


## Features

Calculate the rate of change of the video from the histogram and the rate of change of the feature points.
The rate of change between a frame and the next frame is accumulated and divided by the number of frames to obtain a constant.

## required
python ffmpeg 

## Usage

./anime_indicator.sh mov_file

If you want to cut the input file by time, please modify the script.

``` shell
CUT=1
START="00:00:00.000"
END="00:23:06.000"
```

## Thanks
https://qiita.com/best_not_best/items/c9497ffb5240622ede01

