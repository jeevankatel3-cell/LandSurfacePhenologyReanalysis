# Elevation-Dependent Land Surface Phenology Shifts Across Nepal's Ecoregions

This repository contains the data processing, analysis, and visualization code for a study examining 23 years (2001–2024) of Land Surface Phenology (LSP) trends across nine ecoregions of Nepal, and evaluating their topographic and climatic drivers.

## Background

Land Surface Phenology (LSP) — derived from satellite vegetation indices — is a sensitive indicator of ecosystem responses to climate change. Nepal's extreme elevational gradient (<100 m to >8,848 m) and diverse ecoregions spanning tropical grasslands to alpine shrublands make it an exceptional natural laboratory for studying how topography and climate jointly shape phenological change. Using MODIS EVI (~250 m) processed through TIMESAT, we characterize trends in Start of Season (SOS), End of Season (EOS), Length of Season (LOS), and Peak of Season (POS), and identify the dominant topographic (elevation, slope, aspect) and climatic (temperature, precipitation, soil moisture, solar radiation) drivers across ecoregions.

---

## Datasets

| Dataset | Description | Source |
|---|---|---|
| **MOD13Q1.061** | MODIS/Terra EVI, 250 m, 16-day, 2001–2024 | NASA LP DAAC via Google Earth Engine |
| **MCD12Q2.061** | MODIS Land Cover Dynamics (standard LSP product for validation) | NASA LP DAAC |
| **GMTED2010** | Global terrain elevation data; elevation, slope & aspect derived | USGS |
| **TerraClimate** | Monthly temperature, precipitation, soil moisture, solar radiation (~4 km) | Abatzoglou et al., 2018 |

**Processing Tools:** TIMESAT 3.3 (curve fitting & phenometric extraction), Google Earth Engine (data access & pre-processing), Python (trend analysis & visualization).

---

## Repository Structure

```
LSP_WS/
├── Codes/               # All analysis scripts (see below)
├── Data/                # Is Zipped and uploaded to Zenodo, extract from there to your cloned repository
│   ├── DEM_Rasters/             # Elevation, slope, aspect rasters
│   ├── Ecoregion_raster/        # Nepal ecoregion boundary raster
│   ├── Environmental_Drivers/   # TerraClimate climate variable rasters
│   ├── LSP_Rasters/             # Raw TIMESAT-derived LSP rasters
│   ├── Scaled_LSP_Rasters/      # Scaled LSP metric rasters
│   ├── Unscaled_LSP_Rasters/    # Unscaled (raw export) LSP rasters
│   ├── Standard_Modis_LSP/      # MCD12Q2 standard product (validation)
│   ├── Trend_Rasters/           # Mann-Kendall trend & Sen's slope rasters
│   ├── Processed/               # Intermediate processed outputs
│   ├── Final/                   # Final outputs and figures
│   └── roi_nepal/               # Nepal region of interest boundary
└── Documents/           # removed
```

### Scripts (`Codes/`)

| Script | Description |
|---|---|
| `1_1_Download_unscaled_raster.py` | Downloads raw (unscaled) LSP rasters exported from TIMESAT/GEE |
| `1_2_Scale_LSP_raster.ipynb` | Applies scaling factors to raw LSP rasters to produce metric values in DOY/EVI units |
| `1_3_Download_standard_modis_lsp.ipynb` | Downloads the MCD12Q2 standard MODIS LSP product for validation |
| `1_4_Download_dem_rasters.py` | Downloads and processes GMTED2010 DEM rasters (elevation, slope, aspect) |
| `1_5_Download_environmental_driver.py` | Downloads TerraClimate climate variable rasters for driver analysis |
| `2_1_Trend_analysis_pmk.ipynb` | Pixel-level Mann-Kendall trend test and Sen's slope estimation for all LSP metrics |
| `2_2_Validate_evi_to_standard_product.ipynb` | Validates derived EVI-based LSP trends against MCD12Q2 using Spearman's correlation |
| `3_1_Stratified_ecoregion_trends.ipynb` | Topographic stratification into Stratified Units (SUs) and ecoregion-level trend summarization |
| `3_2_Derive_valid_lsp_change_raster.ipynb` | Generates rasters of valid LSP change pixels based on TAR filtering criteria |
| `3_3_Correlation_topographic_drivers.ipynb` | Spearman's/Mann-Whitney U analysis of topographic drivers (elevation, slope, aspect) vs. trend asymmetry index |
| `3_4_1_Correlation_environmental_drivers_sos.ipynb` | Pixel-level climate–SOS Spearman's correlation for pre-season windows |
| `3_4_2_Correlation_environmental_drivers_eos.ipynb` | Pixel-level climate–EOS Spearman's correlation for pre-season windows |
| `3_4_3_Correlation_environmental_drivers_pos.ipynb` | Pixel-level climate–POS Spearman's correlation for pre-season windows |
| `4_1_Heatmap_environmental_driver.ipynb` | Visualization of climatic driver correlation matrices (heatmaps) across ecoregions |

---

## Dependencies

The Python analysis environment requires the following major packages:

| Package | Purpose |
|---|---|
| `numpy` | Array operations and numerical computation |
| `pandas` | Tabular data management |
| `rasterio` | Reading/writing geospatial rasters |
| `geopandas` | Vector spatial data handling |
| `scipy` | Statistical tests |
| `pymannkendall` | Mann-Kendall trend test and Sen's slope |
| `matplotlib` | Plotting and visualization |
| `seaborn` | Heatmap and statistical visualizations |
| `earthengine-api` | Google Earth Engine data access |
| `geemap` | GEE interactive mapping |

> TIMESAT 3.3 (standalone software) is required for EVI time-series smoothing and LSP metric extraction prior to the Python workflow.

## Zenodo Data

The /Data folder (along with detailed analysis results) is available on Zenodo at https://doi.org/10.5281/zenodo.8266666

## Publication
"TITLE" is currently under review at International Journal of Biometeorology

## Contact
jeevankatel3@gmail.com if you have any questions or suggestions

---

*Generated by Antigravity · 2026-02-25*
