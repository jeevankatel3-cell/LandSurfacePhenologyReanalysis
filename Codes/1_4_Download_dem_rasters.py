#download gmted dem to work with modis lsp
#using native ee reproject to epsg:4326
import ee
import geemap
import os

cloud_project = 'ee-jeevankatel3'
try: 
    ee.Initialize()
except Exception as e:
    ee.Authenticate(project = cloud_project)
    ee.Initialize()

gmted = ee.Image("USGS/GMTED2010_FULL")
roi = ee.FeatureCollection('projects/ee-jeevankatel3/assets/nepRect')
roi_geometry = roi.geometry()
scale = 250
outpath_base = r"C:\Users\A S U S\Documents\Study\Land Surface Phenology\LSP_WS\Data\DEM_Rasters"
os.makedirs(outpath_base, exist_ok= True)

#process dem to get following rasters: elevation, aspect, slope
gmted_roi = gmted.clip(roi)
elevation = gmted_roi.select('mea').rename('elevation')
aspect = ee.Terrain.aspect(gmted_roi.select('mea')).rename('aspect')
slope = ee.Terrain.slope(gmted_roi.select('mea')).rename('slope')
image_list = [elevation, aspect, slope]

for img in image_list:
    filename = f"{img.bandNames().getInfo()[0]}.tif"
    outpath_full = os.path.join(outpath_base, filename)
    geemap.ee_export_image(img, filename=outpath_full, region=roi_geometry, crs="EPSG:4326", scale=scale, file_per_band=False)