import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
plt.rcParams['font.weight'] = 'bold'

import numpy as np 
import numpy.ma as ma

import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.feature as cfeature

import cartopy.io.shapereader as shapereader

from matplotlib.collections import QuadMesh
from typing import Optional, Union, Tuple



def plot(lons: np.ndarray, lats: np.ndarray, variable: np.ndarray = None, 
         variable_vector: Tuple[np.ndarray, np.ndarray] = None, 
         units: str = "None", img_name: str = "map.png", 
         save: bool = False, plot: bool = False, 
         title: str = "",
         zlims: Optional[tuple] = None,
         use_log_scale: bool = False) -> Union[QuadMesh, None]:

    # plotting preferences
    plt.rcParams.update({"font.size": 10})
    cmap = plt.get_cmap('viridis')

    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # NOTE that PlateCarree expects longitudes on interval -180, 180
    lons[lons > 180] = lons[lons > 180] - 360

    cont = None 
    
    # by default we plot this, can be switched off by passing None
    # and passing not None for vector field
    if variable is not None: 
        variable = np.ma.masked_array(variable, np.isnan(variable))

        zmin = variable.min() 
        if zlims is not None : zmin=zlims[0]

        zmax = variable.max() 
        if zlims is not None : zmax=zlims[1]

        if use_log_scale: 
            cont = ax.pcolormesh(lons, lats, variable,
                cmap=cmap, 
                norm=LogNorm(vmin=zmax*0.01, vmax=zmax),
                alpha=0.75, 
                shading='gouraud')
        else: 
            cont = ax.pcolormesh(lons, lats, variable,
                cmap=cmap, 
                vmin=zmin, 
                vmax=zmax, 
                alpha=0.75, 
                shading='gouraud')

        cont.set_edgecolor('none')

        cbar = fig.colorbar(cont, orientation="vertical",
                            fraction=0.046, pad=0.04)
        cbar.set_label(units, fontweight='bold')

        if not use_log_scale: 
            cbar.set_ticks(np.linspace(zmin, zmax, 10))

    # can overlay this 
    if variable_vector is not None: 
        variable_vector = np.ma.masked_array(
            variable_vector, np.isnan(variable_vector)
        )
        dx = variable_vector[0]
        dy = variable_vector[1]
        ax.quiver(lons, lats, dx, dy)

    xmin = lons.min()
    xmax = lons.max()

    xticks = np.linspace(xmin, xmax, 5)
    ax.set_xlim(xmin, xmax)
    ax.set_xticks(xticks, crs=ccrs.PlateCarree())

    ymin = lats.min()
    ymax = lats.max()
    yticks = np.linspace(ymin, ymax, 5)
    ax.set_ylim(ymin, ymax)
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    # ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    ax.xaxis.set_major_formatter(LONGITUDE_FORMATTER)
    ax.yaxis.set_major_formatter(LATITUDE_FORMATTER)

    # draw land features
    # ax.add_feature(cfeature.COASTLINE, linewidth=0.25)
    ax.add_feature(cfeature.LAND, edgecolor='black')

    ax.set_title(title, pad=20, fontweight='bold')

    if plot : plt.show()
    if save : fig.savefig(img_name)

    return cont

