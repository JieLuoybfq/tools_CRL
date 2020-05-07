#!/bin/bash
# Script to specify tiles for download 
# Charlotte Levy
# Created 2020-05-07

usage="Usage: ./call_download.sh" [-s start date (YYYY-MM-DD)] [-e end date (YYYY-MM-DD)] [-n product short name e.g. MCD43A3] [-d download dir]"
while getopts ":s:e:n:t:d:" arg; do
    case $arg in
	s) start_date=$OPTARG;;
	e) end_date=$OPTARG;;
	n) short_name=$OPTARG;;
	d) dl_dir=$OPTARG;;
	\?) echo $usage
    esac
done

tiles="h010v04 h09v04"

# Loop through all tiles in list, submit to function
for val in tiles; do
	echo "Beginning tile: " $val
	echo "Calling download function"
	./download_viirs_modis_climoOpt.sh -s ${start_date} -e ${end_date} -n ${short_name} -t $val -d ${dl_dir} 
	echo "Tile " $val "complete."
done