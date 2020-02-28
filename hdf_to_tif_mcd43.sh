#!/bin/bash

in_dir=$1 
out_dir=$2

if [ ! -d ${out_dir} ]; then
    mkdir ${out_dir}
fi

#if [ ! -d ${out_dir}/qa/ ]; then
#    mkdir ${out_dir}/qa/
#fi

#if [ ! -d ${out_dir}/wsa/ ]; then
#    mkdir ${out_dir}/wsa/
#fi

#if [ ! -d ${out_dir}/bsa/ ]; then
#    mkdir ${out_dir}/bsa/
#fi

for hdf in $in_dir/*.hdf
do
    echo $hdf
    filename=$(basename -- $hdf)
    extension="${filename##*.}"
    filename_bare="${filename%.*}"
    gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MODIS_Grid_500m_2D:sur_refl_b01_1 ${out_dir}/${filename_bare}_sr_b1.tif
    gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MODIS_Grid_500m_2D:sur_refl_b02_1 ${out_dir}/${filename_bare}_sr_b2.tif
    gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MODIS_Grid_500m_2D:sur_refl_b03_1 ${out_dir}/${filename_bare}_sr_b3.tif
    gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MODIS_Grid_500m_2D:sur_refl_b04_1 ${out_dir}/${filename_bare}_sr_b4.tif
    gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MODIS_Grid_500m_2D:sur_refl_b05_1 ${out_dir}/${filename_bare}_sr_b5.tif
    gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MODIS_Grid_500m_2D:sur_refl_b06_1 ${out_dir}/${filename_bare}_sr_b6.tif
    gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MODIS_Grid_500m_2D:sur_refl_b07_1 ${out_dir}/${filename_bare}_sr_b7.tif

    #gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:Albedo_WSA_Band1 ${out_dir}/${filename_bare}_wsa_b1.tif
    #gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:Albedo_WSA_Band2 ${out_dir}/${filename_bare}_wsa_b2.tif
    #gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:Albedo_WSA_Band3 ${out_dir}/${filename_bare}_wsa_b3.tif
    #gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:Albedo_WSA_Band4 ${out_dir}/${filename_bare}_wsa_b4.tif
    #gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:Albedo_WSA_Band5 ${out_dir}/${filename_bare}_wsa_b5.tif
    #gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:Albedo_WSA_Band6 ${out_dir}/${filename_bare}_wsa_b6.tif
    #gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:Albedo_WSA_Band7 ${out_dir}/${filename_bare}_wsa_b7.tif
    #gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:Albedo_WSA_shortwave ${out_dir}/wsa/${filename_bare}_wsa_shortwave.tif
    #gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:Albedo_BSA_shortwave ${out_dir}/bsa/${filename_bare}_bsa_shortwave.tif
    #gdal_translate -of GTiff HDF4_EOS:EOS_GRID:'"'${in_dir}/${filename}'"':MOD_Grid_BRDF:BRDF_Albedo_Band_Mandatory_Quality_shortwave ${out_dir}/qa/${filename_bare}_qa_shortwave.tif
done
