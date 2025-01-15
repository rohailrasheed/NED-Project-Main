#!/usr/bin/env python
import cdsapi
import xarray as xr
import pandas as pd

# Create a CDS API client
c = cdsapi.Client()

# Define the parameters you want to retrieve
parameters = [
    '130',   # 2m temperature
    '157',   # Apparent temperature
    '134',   # Specific humidity
    '132',   # Relative humidity
    '151',   # Surface pressure
    '165',   # Geopotential height
    '228',   # Total precipitation
    '229',   # Snowfall
    '210',   # 10m U wind component
    '211',   # 10m V wind component
    '201',   # Wind speed
    '202',   # Wind direction
    '233',   # Low cloud cover
    '234',   # Medium cloud cover
    '235',   # High cloud cover
    '237',   # Total cloud cover
    '250',   # Surface solar radiation
    '251',   # Surface net solar radiation
    '260',   # Total column water vapor
    '261',   # Total column cloud water
    '262',   # Total column cloud ice
    '227',   # Surface temperature
    '136',   # Snow depth
    '138',   # Soil temperature
    '143',   # Soil moisture
    '167',   # Sea surface temperature
    '168',   # Sea surface salinity
    '173',   # Ice concentration
    '174',   # Ice thickness
    '176',   # Sea ice extent
    '186',   # 500 hPa temperature
    '188',   # 850 hPa temperature
    '192',   # 1000 hPa temperature
    '200',   # 2m dew point temperature
    '104',   # Precipitation rate
    '159',   # Total precipitation (hourly)
    '135',   # Total cloud cover (daily)
    '144',   # Soil temperature (0-7cm)
    '145',   # Soil moisture (0-7cm)
    '208',   # 10m wind speed
    '223',   # Pressure at sea level
    '242',   # Total column water
    '225',   # Surface pressure (hourly)
    '112',   # Air density
    '163',   # CAPE
    '180',   # Cloud base height
    '205',   # Visibility
    '213',   # Evapotranspiration
    '222',   # Mean sea level pressure
    '116',   # Ground temperature
    '127',   # Maximum temperature
    '126',   # Minimum temperature
    '252',   # Surface net solar radiation (hourly)
    '240',   # Total column cloud liquid water
    '243',   # Total column cloud ice water
    '257',   # Weather codes
    '139',   # Soil moisture (0-40cm)
    '154',   # Total cloud cover (hourly)
    '153',   # Low cloud cover (hourly)
    '152',   # Medium cloud cover (hourly)
    '203',   # Wind direction (hourly)
    '204',   # Wind gust speed
    '211',   # Surface temperature (hourly)
    '212',   # Sea surface salinity (hourly)
    '214',   # Ice thickness (hourly)
    '215',   # Sea ice extent (hourly)
    '216',   # Boundary layer height
    '217',   # Atmospheric pressure at sea level
    '218',   # Cloud fraction
    '219',   # Precipitation amount
    '220'    # Cumulative precipitation
]


# Create a string of parameters separated by commas
param_str = ','.join(parameters)

# Retrieve ERA5 data
c.retrieve('reanalysis-era5-complete', {
    'date': f'{year}-01-01/to/{year}-12-31',   #'2013-01-01',            # Specify the date
    'levelist': '1/10/100/137',      # Model levels
    'levtype': 'ml',                 # Level type
    'param': parameters,              # Multiple parameters
    'stream': 'oper',                # Data stream
    'time': '00/to/23/by/6',         # Time intervals
    'type': 'an',                    # Analysis type
    'area': '80/-50/-25/0',          # Geographic area (North, West, South, East)
    'grid': '1.0/1.0',               # Grid resolution
    'format': 'netcdf',              # Output format
}, 'ERA5-ml-temperature-subarea.nc')   # Output filename

# Load the NetCDF data
data = xr.open_dataset('ERA5-ml-temperature-subarea.nc')

# Convert to pandas DataFrame
df = data.to_dataframe().reset_index()

# Specify output CSV file
output_csv_file = 'ERA5-ml-temperature-subarea.csv'

# Save to CSV
df.to_csv(output_csv_file, index=False)

print(f'Data saved to {output_csv_file}')
