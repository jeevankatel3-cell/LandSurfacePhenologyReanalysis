import ee
import geemap
import os

cloud_project = 'ee-jeevankatel3'
try: 
    ee.Initialize()
except Exception as e:
    ee.Authenticate(project = cloud_project)
    ee.Initialize()


start_year = 2001
end_year = 2024
output_base_dir = r'C:/Users/A S U S/Documents/Study/Land Surface Phenology/LSP_WS/Data/Unscaled_LSP_Rasters'
roi = ee.FeatureCollection('projects/ee-jeevankatel3/assets/nepRect')
roi_geometry = roi.geometry()
scale = 250



sos_asset_base_path = 'projects/ee-jeevankatel3/assets/n_me_sos'
eos_asset_base_path = 'projects/ee-jeevankatel3/assets/n_me_eos'
los_asset_base_path = 'projects/ee-jeevankatel3/assets/n_me_los'
pos_asset_base_path = 'projects/ee-jeevankatel3/assets/n_me_pos'

sos_asset_list = [f"{sos_asset_base_path}{str(year)[-2:]}_season1" for year in range(start_year, end_year + 1)]
eos_asset_list = [f"{eos_asset_base_path}{str(year)[-2:]}_season1" for year in range(start_year, end_year + 1)]
los_asset_list = [f"{los_asset_base_path}{str(year)[-2:]}_season1" for year in range(start_year, end_year + 1)]
pos_asset_list = [f"{pos_asset_base_path}{str(year)[-2:]}_season1" for year in range(start_year, end_year + 1)]


#download function using geemap
def download_single_image(asset_id, outpath_full):
    image = ee.Image(asset_id)    
    geemap.ee_export_image(image, filename=outpath_full, region=roi_geometry, crs="EPSG:4326", scale=scale, file_per_band=False)


metrics = {
    'sos': sos_asset_list,
    'eos': eos_asset_list,
    'los': los_asset_list,
    'pos': pos_asset_list
}

for metric, asset_list in metrics.items():
    metric_dir = os.path.join(output_base_dir, metric)
    os.makedirs(metric_dir, exist_ok=True)
    
    for asset_id in asset_list:
        
        parts = asset_id.split('_')
        filename = f"{parts[2]}.tif"
        outpath_full = os.path.join(metric_dir, filename)
        
        if not os.path.exists(outpath_full):
            print(f"Downloading {asset_id} to {outpath_full}...")
            download_single_image(asset_id, outpath_full)
        else:
            print(f"Skipping {filename}, already exists.")
