import numpy as np 
import numpy.ma as ma
import netCDF4 as nc
import pathlib

import map_plotter 

# make sure directory changes are relative to file, so can run from top level directory
path = pathlib.Path(__file__).parent

if __name__ == "__main__":

    ds = nc.Dataset(str(path.absolute() / "map.nc"), 'r', format='NETCDF4')

    lons = ds.variables['lon'][:]
    lats = ds.variables['lat'][:]
    lons_g, lats_g = np.meshgrid(lons, lats, indexing="ij")
    
    currents = ds.variables['current'][:, :]

    masked_currents = ma.masked_invalid(currents)

    map_plotter.plot(
        lons_g, lats_g, masked_currents,  
        units="m/s", img_name="ocean_current.png", plot=True, save=False)


