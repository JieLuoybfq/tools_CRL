"""
Created on Wed Sep 19 10:04:10 2018
@author: aelmes

Taiga,AK,Delta Junction - DEJU,63.88112,-145.75136,Relocatable Terrestrial,Bureau of Land Management,Complete,Partially Available,h11v02
Taiga,AK,Caribou-Poker Creeks Research Watershed - BONA,65.15401,-147.50258,Core Terrestrial,University of Alaska,Complete,Partially Available,h11v02
Tundra,AK,Barrow Environmental Observatory - BARR,71.28241,-156.61936,Relocatable Terrestrial,Barrow Environmental Observatory,Complete,Partially Available,h12v01
Tundra,AK,Toolik - TOOL,68.66109,-149.37047,Core Terrestrial,Bureau of Land Management,Complete,Partially Available,h12v02
Taiga,AK,Healy - HEAL,63.87569,-149.21334,Relocatable Terrestrial,Alaska Department of Natural Resources,h11v02

Anaktuvuk River Fire: year 2007, 
smple1: 69.120186, -150.60678

Rock Fire: year 2015, 
orig_smpl: 66.012754 -154.162100

smpl1:  66.020665, -154.133065 
smpl2:  66.187050, -153.932029
smpl3:  65.979228, -154.049494  
smpl4:  65.920039, -154.040912 

"""
import os, glob, sys, rasterio, pyproj, csv, statistics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#years = [ "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019" ]
years = [ "2018", "2019" ]
#tile = "h12v04"
prdct = "MCD43A3"
base_dir = '/penobscot/data06/arthur.elmes/'

sites_dict = {
    #"HF" : [(42.53691, -72.17265), "h12v04"]
    "Summit" : [(72.57972, -38.50454), "h16v01"],
    #"NASA-U" : [(73.84189, -49.49831), "h16v01"],
    #"GITS":  [(77.13781, -61.04113), "h16v01"],
    #"Humboldt" : [(78.5266, -56.8305), "h16v01"],
    #"CP2" : [(69.87968, -46.98692), "h16v01"],
    #"South_Dome" : [(63.14889, -44.81717), "h16v02"],
    #"DYE-2" : [(66.48001, -46.27889), "h16v02"],
    #"Saddle" : [(65.99947, -44.50016), "h16v02"],
    #"NASA-SE" : [(66.4797, -42.5002), "h16v02"],
    #"Swiss_Camp" : [(69.56833, -49.31582), "h16v02"],
    #"JAR" : [(69.498358, -49.68156), "h16v02"],
    #"JAR_2" : [(69.42, -50.0575), "h16v02"],
    #"KAR" : [(69.69942, -33.00058), "h16v02"],
    #"NASA-E" : [(75, -29.99972), "h17v01"],
    #"NGRIP" : [(75.09975, -42.3325), "h17v01"],
    #"TUNU-N" : [(78.01677, -33.99387), "h17v01"]
}

#"Crawford_Pt" : [(69.87975, -46.98667), "h16v01"],
    
# sites_dict = {
#         "DEJU" : [(63.88112, -145.75136), "h11v02"],
#         "BONA" : [(65.15401,-147.50258), "h11v02"],
#         "BARR" : [(71.28241,-156.61936), "h12v01"],
#         "TOOL" : [(68.66109,-149.37047), "h12v02"],
#         "HEAL" : [(63.87569,-149.21334), "h11v02"],
#         "CARI" : [(65.15306, -147.502), "h11v02"]
#         }

def convert_ll(lat, lon, tile, in_dir):
    # Convert the lat/long point of interest to a row/col location
    template_tif_list = glob.glob(os.path.join(in_dir, '{prdct}.A*{tile}*wsa_shortwave.tif'.format(prdct=prdct, tile=tile)))
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
    for year in years:
        for site in sites_dict.items():
            print("Processing " + str(year) + " at site: " + site[0])
            in_dir = os.path.join(base_dir, prdct, 'tif', year, site[1][1])
            fig_dir = os.path.join(base_dir, 'figs')
            os.chdir(in_dir)

            # Set up graph days and time axis
            doys = range(1, 366)

            # Set up the pixel location manually FOR NOW
            location = str(site[0])
            print(site)
            lat_long = (site[1][0][0], site[1][0][1])
            print(lat_long)
            
            # Create empty arrays for mean, sd
            #TODO curently these aren't really needed
            wsa_swir_mean = []
            wsa_swir_sd = []
            bsa_swir_mean = []
            bsa_swir_sd = []
            
            for day in doys:
                # Open the shortwave white sky albedo band.
                # The list approach is because of the processing date part of the file
                # name, which necessitates the wildcard -- this was just the easiest way.
                wsa_tif_list = glob.glob(os.path.join(in_dir,
                                                      'wsa',
                                                      '{prdct}.A{year}{day:03d}*wsa_shortwave.tif'.format(prdct=prdct,
                                                                                                          day=day, year=year)))
                bsa_tif_list = glob.glob(os.path.join(in_dir,
                                                      'bsa',
                                                      '{prdct}.A{year}{day:03d}*bsa_shortwave.tif'.format(prdct=prdct,
                                                                                                          day=day, year=year)))
                qa_tif_list = glob.glob(os.path.join(in_dir,
                                                     'qa',
                                                     '{prdct}.A{year}{day:03d}*qa_shortwave.tif'.format(prdct=prdct,
                                                                                                        day=day, year=year)))
                # See if there is a raster for the date, if not use a fill value for the graph
                if len(wsa_tif_list) == 0 or len(bsa_tif_list) == 0 or len(qa_tif_list) == 0:
                    #print('File not found: MCD43A3.A{year}{day:03d}*wsa_shortwave.tif'.format(day=day, year=year))
                    wsa_swir_subset_flt = float('nan')
                    bsa_swir_subset_flt = float('nan')
                elif len(wsa_tif_list) > 1:
                    print('Multiple matching files found for same date!')
                    sys.exit()
                else:
                    print('Found file: ' + ' {prdct}.A{year}{day:03d}*wsa_shortwave.tif'.format(prdct=prdct, day=day, year=year))
                    wsa_tif = wsa_tif_list[0]
                    bsa_tif = bsa_tif_list[0]
                    qa_tif = qa_tif_list[0]

                    # Open tifs as gdal ds but using rasterio for simplicity
                    wsa_raster = rasterio.open(wsa_tif)
                    bsa_raster = rasterio.open(bsa_tif)
                    qa_raster = rasterio.open(qa_tif)
                    wsa_band = wsa_raster.read(1)
                    bsa_band = bsa_raster.read(1)
                    qa_band = qa_raster.read(1)

                    # Mask out nodata values
                    wsa_swir_masked = np.ma.masked_array(wsa_band, wsa_band == 32767)
                    wsa_swir_masked_qa = np.ma.masked_array(wsa_swir_masked, qa_band > 1)
                    bsa_swir_masked = np.ma.masked_array(bsa_band, bsa_band == 32767)
                    bsa_swir_masked_qa = np.ma.masked_array(bsa_swir_masked, qa_band > 1)

                    # Spatial subset based on coordinates of interest.
                    wsa_smpl_results = []
                    bsa_smpl_results = []
                    
                    #TODO this used to be an additional loop that would average the values over
                    #several locations to get one mean value, rather than get the value of a given
                    #tower's pixel. Maybe modifiy to average within a bounding box or something?
                    #for smpl in sites_dict.values():
                    smp_rc = convert_ll(site[1][0][0], site[1][0][1], site[1][1], os.path.join(in_dir, 'wsa'))
                    print("Sample row/col: " + str(smp_rc))
                    print("Directory: " + os.path.join(in_dir, 'wsa'))
                    wsa_swir_subset = wsa_swir_masked_qa[smp_rc]
                    wsa_swir_subset_flt = np.multiply(wsa_swir_subset, 0.001)
                    bsa_swir_subset = bsa_swir_masked_qa[smp_rc]
                    bsa_swir_subset_flt = np.multiply(bsa_swir_subset, 0.001)
                       
                    # Add each point to the temporary list
                    wsa_smpl_results.append(wsa_swir_subset_flt)
                    bsa_smpl_results.append(bsa_swir_subset_flt)
                    #TODO this try is not really needed, but it doesn't hurt to leave it in case
                    #I want to incorporate the multiple-points-per-sample idea
                    try:
                        wsa_tmp_mean = statistics.mean(wsa_smpl_results)
                        bsa_tmp_mean = statistics.mean(bsa_smpl_results)
                        wsa_swir_mean.append(wsa_tmp_mean)
                        bsa_swir_mean.append(bsa_tmp_mean)
                    except:
                        wsa_swir_mean.append(0.0)
                        bsa_swir_mean.append(0.0)

        wsa_smpl_results_df = pd.DataFrame(wsa_swir_mean)
        bsa_smpl_results_df = pd.DataFrame(bsa_swir_mean)
        cmb_smpl_results_df = pd.concat([wsa_smpl_results_df, bsa_smpl_results_df], axis=1, ignore_index=True)
        print("Combined DF below")
        cmb_smpl_results_df.set_axis(['wsa', 'bsa'], axis=1, inplace=True)
        print(cmb_smpl_results_df.to_string())
        # Do plotting and save output
        #print(*doys)
        #print(*wsa_swir_mean)
        series_name = location + "_" + str(year)
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
