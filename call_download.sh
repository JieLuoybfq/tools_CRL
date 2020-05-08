#!/usr/bin/bash

# Script to specify tiles for download
# Charlotte Levy
# Created 2020-05-07

usage="Usage: ./call_download.sh [-s start date (YYYY-MM-DD)] [-e end date (YYYY-MM-DD)] [-n product short name e.g.MCD43A3] [-d download dir]"
while getopts ":s:e:n:d:" arg; do
	case $arg in
		s) start_date=$OPTARG;;
		e) end_date=$OPTARG;;
		n) short_name=$OPTARG;;
		d) dl_dir=$OPTARG;;
		\?) echo $usage
	esac
done

tiles="h14v00 h15v00 h16v00 h17v00 h18v00 h19v00 h20v00 h21v00 h11v01 h12v01 h13v01h14v01 h15v01 h16v01 h17v01 h18v01 h19v01 h20v01 h21v01 h22v01 h23v01 h24v01 h09v02 h10v02 h11v02 h12v02 h13v02 h14v02 h15v02 h16v02 h17v02 h18v02 h19v02 h20v02 h21v02 h22v02 h23v02 h24v02 h25v02 h26v02 h06v03 h07v03 h08v03 h09v03 h10v03 h11v03 h12v03 h13v03 h14v03 h15v03 h16v03 h17v03 h18v03 h19v03 h20v03 h21v03 h22v03 h23v03 h24v03 h25v03 h26v03 h27v03 h28v03 h29v03 h04v04 h05v04 h06v04 h07v04 h08v04 h09v04 h10v04 h11v04 h12v04 h13v04 h14v04 h15v04 h16v04 h17v04 h18v04 h19v04 h20v04 h21v04 h22v04 h23v04 h24v04 h25v04 h26v04 h27v04 h28v04 h29v04 h30v04 h31v04 h02v05 h03v05 h04v05 h05v05 h06v05 h07v05 h08v05 h09v05 h10v05 h11v05 h12v05 h13v05 h14v05 h15v05 h16v05 h17v05 h18v05 h19v05 h20v05 h21v05 h22v05 h23v05 h24v05 h25v05 h26v05 h27v05 h28v05 h29v05 h30v05 h31v05 h32v05 h33v05"

echo "Running for tiles h14v00 - h33v05, filled only"

# Loop through all tiles in list, submit to function

for val in $tiles; do
	echo "Beginning tile: " $val
	echo "Calling download function"
	./download_viirs_modis_climoOpt.sh -s ${start_date} -e ${end_date} -n ${short_name} -t $val -d ${dl_dir}
	echo "Tile " $val "complete."
done

