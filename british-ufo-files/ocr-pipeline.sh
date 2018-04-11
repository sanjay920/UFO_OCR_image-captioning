#!/bin/bash

export FILENAME=$1
echo $FILENAME
filename_no_path=$(basename "$FILENAME")
extension="${filename_no_path##*.}"
filename_no_extension="${filename_no_path%.*}"
echo "Processing $FILENAME: extension $extension: filename no extension: $filename_no_extension"

mkdir -p $filename_no_extension
mkdir -p $filename_no_extension/tiff
mkdir -p $filename_no_extension/outtxt
mkdir -p $filename_no_extension/temp

pdfseparate "$FILENAME" "$filename_no_extension"/%d.pdf


for f in $( ls $filename_no_extension ); do
    the_file=$(basename $f)
    the_file_ext="${the_file##*.}"
    the_file_noext="${the_file%.*}"
    # convert -density 300 $filename_no_extension/$the_file -depth 8 -background white -flatten +matte $filename_no_extension/tiff/$the_file_noext.tif
    # tesseract $filename_no_extension/tiff/$the_file_noext.tif $filename_no_extension/outtxt/$the_file_noext
    gs -q -dNOPAUSE -sDEVICE=jpeg -dJPEGQ=0 -r300.0 -sOutputFile=$filename_no_extension/temp/$the_file_noext.jpg $filename_no_extension/$the_file -c quit
    convert -density 300 $filename_no_extension/temp/$the_file_noext.jpg -depth 8 -median 3 $filename_no_extension/tiff/$the_file_noext.tif
    tesseract $filename_no_extension/tiff/$the_file_noext.tif $filename_no_extension/outtxt/$the_file_noext -psm 1 -c hocr_font_info=1 -l eng
done
