##from ecmwfapi import ECMWFDataServer
##import xarray as xr
##import pandas as pd
##from datetime import datetime, timedelta
##
##def fetch_era5_data(start_date, end_date, output_file):
##    # Initialize the server
##    server = ECMWFDataServer()
##    
##    # Define the parameters for the data request
##    params = {
##        'class': 'ea',  # Atmospheric data class
##        'dataset': 'era5',
##        'date': f'{2014-10-22}/to/{2024-10-22}',
##        'expver': '1',
##        'levtype': 'sfc',  # Surface level
##        'param': ','.join([
##        '165.128', '130.128', '228.128', '165.128', '166.128', 
##        '134.128', '151.128', '196.128', '129.128', '228.128',
##        '227.128', '236.128', '167.128', '198.128', '165.128', 
##        '130.128', '131.128', '132.128', '157.128', '133.128', 
##        '128.128', '130.128', '136.128', '165.128', '198.128',
##        '199.128', '200.128', '233.128', '168.128', '133.128', 
##        '163.128', '240.128', '165.128', '166.128', '223.128',
##        '224.128', '225.128', '226.128', '130.128', '229.128',
##        '230.128', '231.128', '228.128', '237.128', '238.128',
##        '165.128', '129.128', '239.128', '244.128', '245.128',
##        '246.128'
##        ]),
##        'step': '0',
##        'stream': 'oper',
##        'time': '00:00:00',  # Specific time
##        'format': 'netcdf',
##        'target': 'output.nc'
##    }
##
##    # Fetch the data
##    server.retrieve(params)
##
##    # Load the data
##    data = xr.open_dataset('output.nc')
##
##    # Convert to pandas DataFrame
##    df = data.to_dataframe().reset_index()
##
##    # Save to CSV
##    df.to_csv(output_file, index=False)
##
##if __name__ == "__main__":
##    # Define the date range for the last week
##    end_date = datetime.utcnow()
##    start_date = end_date - timedelta(days=7)
##
##    # Format dates as strings
##    start_date_str = start_date.strftime('%Y-%m-%d')
##    end_date_str = end_date.strftime('%Y-%m-%d')
##
##    # Specify output CSV file
##    output_file = f'era5_data_{start_date_str}_to_{end_date_str}.csv'
##
##    # Fetch and save the data
##    fetch_era5_data(start_date_str, end_date_str, output_file)
##    print(f'Data saved to {output_file}')

from ecmwfapi import ECMWFDataServer

server = ECMWFDataServer()

try:
    server.retrieve({
        'class': 'ea',
        'dataset': 'era5',
        'date': '2024-01-01/to/2024-01-02',
        'param': '165.128',  # Change this if necessary
        'target': 'test.nc'
    })
    print("Data fetched successfully!")
except Exception as e:
    print(f"Error: {e}")
