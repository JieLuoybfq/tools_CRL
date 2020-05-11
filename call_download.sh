#!/bin/bash

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

tiles="h00v14 h00v15 h00v16 h00v17 h00v18 h00v19 h00v20 h00v21 h01v11 h01v12 h01v13 h01v14 h01v15 h01v16 h01v17 h01v18 h01v19 h01v20 h01v21 h01v22 h01v23 h01v24 h02v09 h02v10 h02v11 h02v12 h02v13 h02v14 h02v15 h02v16 h02v17 h02v18 h02v19 h02v20 h02v21 h02v22 h02v23 h02v24 h02v25 h02v26 h03v06 h03v07 h03v08 h03v09 h03v10 h03v11 h03v12 h03v13 h03v14 h03v15 h03v16 h03v17 h03v18 h03v19 h03v20 h03v21 h03v22 h03v23 h03v24 h03v25 h03v26 h03v27 h03v28 h03v29 h04v04 h04v05 h04v06 h04v07 h04v08 h04v09 h04v10 h04v11 h04v12 h04v13 h04v14 h04v15 h04v16 h04v17 h04v18 h04v19 h04v20 h04v21 h04v22 h04v23 h04v24 h04v25 h04v26 h04v27 h04v28 h04v29 h04v30 h04v31 h05v02 h05v03 h05v04 h05v05 h05v06 h05v07 h05v08 h05v09 h05v10 h05v11 h05v12 h05v13 h05v14 h05v15 h05v16 h05v17 h05v18 h05v19 h05v20 h05v21 h05v22 h05v23 h05v24 h05v25 h05v26 h05v27 h05v28 h05v29 h05v30 h05v31 h05v32 h05v33"
echo "Running for tiles h00v14 - h05v33, filled only"

# Loop through all tiles in list, submit to function

for val in $tiles; do
	echo "Beginning tile: " $val
	echo "Calling download function"
	./download_viirs_modis_climoOpt.sh -s ${start_date} -e ${end_date} -n ${short_name} -t $val -d ${dl_dir}
	echo "Tile " $val "complete."
done

