print("""
Created on Wed Sep 19 10:04:10 2018
@author: aelmes

Edited on Tues Feb 11 11:25 2020
@author: clevy

Edits: generate data series for LANCE outputs

""")
#Import needed packages#########################################################################
import os, glob, sys, rasterio, pyproj, csv, statistics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Manually declare the time range, product, and base directory. Tile variable is defunct.########
#years = [ "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019" ]
years = ["2019"]
tile = "h12v04"
prdct = "MOD09GA" #MCD43A3
base_dir = '/muddy/data04/charlotte.levy/outputs/LANCE/2019/h12v04/SR'

sites_dict = {
"HarvardForest" : [(42.53691, -72.17265), tile],
"Fitchburg" : [(42.5834, -71.8023), tile],
"GreylockMtn" : [(42.6376, -73.1662), tile]}
#"Desert" : [(45.354367, 87.727491), "h24v04"]}
#"Mountain" : [(47.240874, 90.019461), "h24v04"],
#"Foothills" : [(47.069119, 98.768448), "h24v04"]}

def convert_ll(lat, lon, tile, in_dir):
    # Convert the lat/long point of interest to a row/col location
    template_tif_list = glob.glob(os.path.join(in_dir, '{prdct}.A*{tile}*sr*.tif'.format(prdct=prdct, tile=tile)))
    template_tif = template_tif_list[0]
    template_raster = rasterio.open(template_tif)
    in_proj = pyproj.Proj(init='epsg:4326')
    out_proj = pyproj.Proj(template_raster.crs)
    print("longitude: " + str(lon) + " latitude:" + str(lat))
    x, y = pyproj.transform(in_proj, out_proj, lon, lat)
    smp_rc = template_raster.index(x, y)
    print('Querying pixel:' + str(smp_rc))
    return smp_rc

def draw_plot():
    plt.ion()
    # fig = plt.figure()
    # fig.suptitle('ABoVE Domain Albedo Time Series')
    # ax = fig.add_subplot(111)
    # fig.subplots_adjust(top=0.85)
    # ax.set_title(series_name)
    # ax.set_xlabel('DOY')
    # ax.set_ylabel('White Sky Albedo')
    # plt.xlim(0, 365)
    # plt.ylim(0.0, 1.0)
    # ax.plot(doys, wsa_swir_mean)
    # plt_name = str(year + '_' + series_name.replace(" ", ""))
    # print('Saving plot to: ' + '{plt_name}.png'.format(plt_name=plt_name))
    # plt.savefig('{plt_name}.png'.format(plt_name=plt_name))


def main():
    # Create empty arrays for mean, sd. also added year through doy
    #TODO curently these aren't really needed. Probably better way for year through
    yearL = []
    siteL = []
    tileL = []
    doyL = []

                
    # Create empty arrays for mean, sd. also added year through doy
    #TODO curently these aren't really needed. Probably better way for year through doy
    b1_swir_mean = []
    b1_swir_sd = []
    b2_swir_mean = []
    b2_swir_sd = []
    b3_swir_mean = []
    b3_swir_sd = []
    b4_swir_mean = []
    b4_swir_sd = []
    b5_swir_mean = []
    b5_swir_sd = []
    b6_swir_mean = []
    b6_swir_sd = []
    b7_swir_mean = []
    b7_swir_sd = []
 
    for year in years:
        for site in sites_dict.items():
            print("Processing " + str(year) + " at site: " + site[0])
            in_dir = os.path.join(base_dir)
            fig_dir = os.path.join(base_dir, 'figs')
            os.chdir(in_dir)

            # Set up graph days and time axis
            doys = range(1, 366)

            # Set up the pixel location manually FOR NOW
            location = str(site[0])
            print(site)
            lat_long = (site[1][0][0], site[1][0][1])
            print(lat_long)

            
            for day in doys:
                # Open each raw reflectance band band.
                # The list approach is because of the processing date part of the file
                # name, which necessitates the wildcard -- this was just the easiest way.
                b1_tif_list = glob.glob(os.path.join(in_dir,
                                                      #'b1'
                                                      '{prdct}.A{year}{day:03d}*sr_b1.tif'.format(prdct=prdct,
                                                                                                          day=day, year=year)))
                b2_tif_list = glob.glob(os.path.join(in_dir,
                                                      #'b2',
                                                      '{prdct}.A{year}{day:03d}*sr_b2.tif'.format(prdct=prdct,
                                                                                                          day=day, year=year)))
                b3_tif_list = glob.glob(os.path.join(in_dir,
                                                     #'b3',
                                                     '{prdct}.A{year}{day:03d}*sr_b3.tif'.format(prdct=prdct,
                                                                                                        day=day, year=year)))
                b4_tif_list = glob.glob(os.path.join(in_dir,
                                                      #'b4',
                                                      '{prdct}.A{year}{day:03d}*sr_b4.tif'.format(prdct=prdct,
                                                                                                          day=day, year=year)))
                b5_tif_list = glob.glob(os.path.join(in_dir,
                                                      #'b5',
                                                      '{prdct}.A{year}{day:03d}*sr_b5.tif'.format(prdct=prdct,
                                                                                                          day=day, year=year)))
                b6_tif_list = glob.glob(os.path.join(in_dir,
                                                     #'b6',
                                                     '{prdct}.A{year}{day:03d}*sr_b6.tif'.format(prdct=prdct,
                                                                                                        day=day, year=year)))
                b7_tif_list = glob.glob(os.path.join(in_dir,
                                                     #'b7',
                                                     '{prdct}.A{year}{day:03d}*sr_b7.tif'.format(prdct=prdct,
                                                                                                        day=day, year=year)))

                # See if there is a raster for the date, if not use a fill value for the graph
                if len(b1_tif_list) == 0 or len(b2_tif_list) == 0 or len(b3_tif_list) == 0 or len(b4_tif_list) == 0 or len(b5_tif_list) == 0 or len(b6_tif_list) == 0 or len(b7_tif_list) == 0:
                    print('File not found: {prdct}.A{year}{day:03d}*sr_bX.tif'.format(prdct=prdct, day=day, year=year))
                    b1_swir_subset_flt = float('nan')
                    b2_swir_subset_flt = float('nan')
                    b3_swir_subset_flt = float('nan')
                    b4_swir_subset_flt = float('nan')
                    b5_swir_subset_flt = float('nan')
                    b6_swir_subset_flt = float('nan')
                    b7_swir_subset_flt = float('nan')

                elif len(b1_tif_list) > 1 or len(b2_tif_list) > 1 or len(b3_tif_list) > 1 or len(b4_tif_list) > 1 or len(b5_tif_list) > 1 or len(b6_tif_list) > 1 or len(b7_tif_list) > 1:
                    print('Multiple matching files found for same date!')
                    sys.exit()
                else:
                    print('Found file: {prdct}.A{year}{day:03d}*sr_bX.tif'.format(prdct=prdct, day=day, year=year))
                    b1_tif = b1_tif_list[0]
                    b2_tif = b2_tif_list[0]
                    b3_tif = b3_tif_list[0]
                    b4_tif = b4_tif_list[0]
                    b5_tif = b5_tif_list[0]
                    b6_tif = b6_tif_list[0]
                    b7_tif = b7_tif_list[0]

                    # Open tifs as gdal ds but using rasterio for simplicity
                    b1_raster = rasterio.open(b1_tif)
                    b2_raster = rasterio.open(b2_tif)
                    b3_raster = rasterio.open(b3_tif)
                    b4_raster = rasterio.open(b4_tif)
                    b5_raster = rasterio.open(b5_tif)
                    b6_raster = rasterio.open(b6_tif)
                    b7_raster = rasterio.open(b7_tif)
                    b1_band = b1_raster.read(1)
                    b2_band = b2_raster.read(1)
                    b3_band = b3_raster.read(1)
                    b4_band = b4_raster.read(1)
                    b5_band = b5_raster.read(1)
                    b6_band = b6_raster.read(1)
                    b7_band = b7_raster.read(1)

                    # Mask out nodata values
                    #wsa_swir_masked = np.ma.masked_array(wsa_band, wsa_band == 32767)
                    #wsa_swir_masked_qa = np.ma.masked_array(wsa_swir_masked, qa_band > 1)
                    #bsa_swir_masked = np.ma.masked_array(bsa_band, bsa_band == 32767)
                    #bsa_swir_masked_qa = np.ma.masked_array(bsa_swir_masked, qa_band > 1)

                    # Spatial subset based on coordinates of interest.
                    b1_smpl_results = []
                    b2_smpl_results = []
                    b3_smpl_results = []
                    b4_smpl_results = []
                    b5_smpl_results = []
                    b6_smpl_results = []
                    b7_smpl_results = []
                    
                    #TODO this used to be an additional loop that would average the values over
                    #several locations to get one mean value, rather than get the value of a given
                    #tower's pixel. Maybe modifiy to average within a bounding box or something?
                    #for smpl in sites_dict.values():
                    smp_rc = convert_ll(site[1][0][0], site[1][0][1], site[1][1], os.path.join(in_dir))
                    print("Sample row/col: " + str(smp_rc))
                    print("Directory: " + os.path.join(in_dir))
                    b1_swir_subset = b1_band[smp_rc]
                    b2_swir_subset = b2_band[smp_rc]
                    b3_swir_subset = b3_band[smp_rc]
                    b4_swir_subset = b4_band[smp_rc]
                    b5_swir_subset = b5_band[smp_rc]
                    b6_swir_subset = b6_band[smp_rc]
                    b7_swir_subset = b7_band[smp_rc]
                    b1_swir_subset_flt = np.multiply(b1_band, 1)
                    b2_swir_subset_flt = np.multiply(b2_band, 1)
                    b3_swir_subset_flt = np.multiply(b3_band, 1)
                    b4_swir_subset_flt = np.multiply(b4_band, 1)
                    b5_swir_subset_flt = np.multiply(b5_band, 1)
                    b6_swir_subset_flt = np.multiply(b6_band, 1)
                    b7_swir_subset_flt = np.multiply(b7_band, 1)
                       
                    # Add each point to the temporary list
                    b1_smpl_results.append(b1_swir_subset_flt)
                    b2_smpl_results.append(b2_swir_subset_flt)
                    b3_smpl_results.append(b3_swir_subset_flt)
                    b4_smpl_results.append(b4_swir_subset_flt)
                    b5_smpl_results.append(b5_swir_subset_flt)
                    b6_smpl_results.append(b6_swir_subset_flt)
                    b7_smpl_results.append(b7_swir_subset_flt)

                    #TODO this try is not really needed, but it doesn't hurt to leave it in case
                    #I want to incorporate the multiple-points-per-sample idea
                    try:
                        b1_tmp_mean = statistics.mean(b1_smpl_results)
                        b1_swir_mean.append(b1_swir_subset_flt)
                        b2_tmp_mean = statistics.mean(b2_smpl_results)
                        b2_swir_mean.append(b2_swir_subset_flt)
                        b3_tmp_mean = statistics.mean(b3_smpl_results)
                        b3_swir_mean.append(b3_swir_subset_flt)
                        b4_tmp_mean = statistics.mean(b4_smpl_results)
                        b4_swir_mean.append(b4_swir_subset_flt)
                        b5_tmp_mean = statistics.mean(b5_smpl_results)
                        b5_swir_mean.append(b5_swir_subset_flt)
                        b6_tmp_mean = statistics.mean(b6_smpl_results)
                        b6_swir_mean.append(b6_swir_subset_flt)
                        b7_tmp_mean = statistics.mean(b7_smpl_results)
                        b7_swir_mean.append(b7_swir_subset_flt)
                    except:
                        b1_swir_mean.append(0.0) 
                        b2_swir_mean.append(0.0) 
                        b3_swir_mean.append(0.0) 
                        b4_swir_mean.append(0.0) 
                        b5_swir_mean.append(0.0) 
                        b6_swir_mean.append(0.0) 
                        b7_swir_mean.append(0.0) 
                     
                    #Added the year, site, tile, and doy
                    yearL.append(str(year))
                    siteL.append(location)
                    tileL.append(tile)
                    doyL.append(str(day))

            b1_smpl_results_df = pd.DataFrame(b1_swir_mean)
            b2_smpl_results_df = pd.DataFrame(b2_swir_mean)
            b3_smpl_results_df = pd.DataFrame(b3_swir_mean)
            b4_smpl_results_df = pd.DataFrame(b4_swir_mean)
            b5_smpl_results_df = pd.DataFrame(b5_swir_mean)
            b6_smpl_results_df = pd.DataFrame(b6_swir_mean)
            b7_smpl_results_df = pd.DataFrame(b7_swir_mean)
            year_df = pd.DataFrame(yearL)
            site_df = pd.DataFrame(siteL)
            tile_df = pd.DataFrame(tileL)
            doy_df = pd.DataFrame(doyL)
            cmb_smpl_results_df = pd.concat([doy_df, tile_df, site_df, year_df, b1_smpl_results_df, b2_smpl_results_df, b3_smpl_results_df, b4_smpl_results_df, b5_smpl_results_df, b6_smpl_results_df, b7_smpl_results_df], axis=1, ignore_index=True)
            print("Combined DF below")
            cmb_smpl_results_df.set_axis(['doy', 'tile', 'site', 'year', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7'], axis=1, inplace=True)
            print(cmb_smpl_results_df.to_string())
            # Do plotting and save output
            series_name = "ResultsbyLatLon" + "_" + str(year)
            os.chdir(fig_dir)
            csv_name = str(series_name + "_" + prdct + ".csv")
            print("writing csv: " + csv_name)
            # export data to csv
            cmb_smpl_results_df.to_csv(csv_name, index=False)
            # with open(csv_name, "w") as export_file:
            #     wr = csv.writer(export_file, dialect='excel', lineterminator='\n')
            #     for index, row in cmb_smpl_results_df.iterrows():
            #         row_data = str(row['wsa'] + "," + row['bsa'])
            #         wr.writerow(row_data)


if __name__ == "__main__":
    main()
