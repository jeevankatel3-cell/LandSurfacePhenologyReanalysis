#download TerraClimate monthly rasters 
#for variables - temp(tmin and tmax average), prec, solar radiation, and soil moisture 
#atmospheric co2 is downloaded from ee assets

import ee
import geemap
import os
import calendar

cloud_project = "ee-jeevankatel3"
try: 
    ee.Initialize(project=cloud_project)
except Exception as e:
    ee.Authenticate()
    ee.Initialize(project=cloud_project)

start_date = '2000-01-01'   #images are downloaded starting a year earlier to consider preseason window
end_date = '2024-12-31'
start_year = 2000
end_year = 2024

scale = 250
base_outdir = r"Data/Environmental_Drivers/"
os.makedirs(base_outdir, exist_ok=True)
roi = ee.FeatureCollection('projects/ee-jeevankatel3/assets/nepRect')
roi_geometry = roi.geometry()
terraClim = ee.ImageCollection("IDAHO_EPSCOR/TERRACLIMATE")

#atmospheric co2 assets download - has semiannual rasters
for year in range(2000, 2021, 1):   #atm co2 rasters are available from 2000 to 2020
    outpath_full = os.path.join(base_outdir, f"AveragedCO2")
    os.makedirs(outpath_full, exist_ok=True)
    #download image A for the year #projects/ee-jeevankatel3/assets/AveragedCO2-2000A
    outpath_a = os.path.join(outpath_full, f"AveragedCO2_{year}A.tif")
    image_a = ee.Image("projects/" + cloud_project + "/assets/" + "AveragedCO2-" + str(year) + "A")
    geemap.ee_export_image(image_a, filename=outpath_a, region=roi_geometry, crs="EPSG:4326", scale=scale, file_per_band=False)
    #download image B for the year
    outpath_b = os.path.join(outpath_full, f"AveragedCO2_{year}B.tif")
    image_b = ee.Image("projects/" + cloud_project + "/assets/" + "AveragedCO2-" + str(year) + "B")
    geemap.ee_export_image(image_b, filename=outpath_b, region=roi_geometry, crs="EPSG:4326", scale=scale, file_per_band=False)


#download TerraClimate monthly rasters
def process_temperature(image):
    tmmn = image.select('tmmn').multiply(0.1).rename('tmmn')
    tmmx = image.select('tmmx').multiply(0.1).rename('tmmx')
    tmean = tmmn.add(tmmx).divide(2).rename('tmean')
    return tmean

def process_prec(image):
    prec = image.select('pr').rename('prec')
    return prec

def process_srad(image):
    srad = image.select('srad').multiply(0.1).rename('srad')
    return srad

def process_soilmoist(image):
    soilmoist = image.select('soil').multiply(0.1).rename('soilmoist')
    return soilmoist

# Variable configuration: (Name, Process Function, Folder Name)
variables_to_download = [
    ("Temperature", process_temperature, "Temperature"),
    ("Precipitation", process_prec, "Precipitation"),
    ("SolarRadiation", process_srad, "SolarRadiation"),
    ("SoilMoisture", process_soilmoist, "SoilMoisture")
]

# for var_name, process_func, folder_name in variables_to_download:
#     var_outdir = os.path.join(base_outdir, folder_name)
#     os.makedirs(var_outdir, exist_ok=True)
#     print(f"Starting downloads for {var_name}...")

#     for year in range(start_year, end_year + 1):
#         for month in range(1, 13):
#             # Calculate the last day of the month
#             _, last_day = calendar.monthrange(year, month)
            
#             # Construct date strings
#             # Note: TerraClimate is monthly, usually indexed on the 1st of the month
#             start_date_str = f"{year}-{month:02d}-01"
#             # We use the end of the month to be safe with the filter
#             end_date_str = f"{year}-{month:02d}-{last_day}" 
            
#             outpath = os.path.join(var_outdir, f"{folder_name}_{year}_{month}.tif")
            
#             if os.path.exists(outpath):
#                 # print(f"Skipping {outpath}, already exists.")
#                 continue
            
#             #filter image collection
#             # To get the specific month's image
#             ic_filtered = terraClim.filterDate(start_date_str, end_date_str).filterBounds(roi)
            
#             if ic_filtered.size().getInfo() == 0:
#                 print(f"No data for {var_name} in {year}-{month:02d}")
#                 continue
                
#             #process and download
#             ic_processed = ic_filtered.map(process_func)
#             image_to_save = ic_processed.first()
            
#             try:
#                 print(f"Downloading {folder_name}_{year}_{month}...")
                
#                 geemap.download_ee_image(
#                     image_to_save, 
#                     filename=outpath, 
#                     region=roi_geometry, 
#                     crs="EPSG:4326", 
#                     scale=scale,
#                     dtype='float32' 
#                 )
#             except Exception as e:
#                 print(f"Failed to download {folder_name}_{year}_{month}: {e}")