
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import os
import sys


mosaic_path=sys.argv[1]


os.listdir(mosaic_path)

dmask=nc.Dataset(mosaic_path+'/ocean_mask.nc')
ny,nx=dmask.variables['mask'].shape

# tile1 === atmos cell
# tile2 === ocean cell
oxarea=np.zeros((ny,nx))

#f_list=[]
#for tile in np.arange(1,7):
#    f_list.append('c192/tmp/C192_mosaic_tile'+str(tile)+'Xocean_mosaic_tile1.nc')
f_list=[mosaic_path+'/atmos_mosaic_tile1Xocean_mosaic_tile1.nc']

for file in f_list:
    f=nc.Dataset(file)
    tile1_cell= f.variables['tile1_cell'][:]
    tile2_cell= f.variables['tile2_cell'][:]
    xgrid_area= f.variables['xgrid_area'][:]

    i2=tile2_cell[:,0]-1
    j2=tile2_cell[:,1]-1
    for i,j,x in zip(i2,j2,xgrid_area):
        oxarea[j,i]=oxarea[j,i]+x

    f.close()


mask=dmask.variables['mask'][:]
bad = np.zeros(mask.shape)
bad[np.logical_and(mask>0,oxarea<=0.0)]=1
bad[np.logical_and(mask==0,oxarea>0.0)]=-1


if bad.min()<0:
    print('There are ',bad[bad<0].sum(),' ocean cells with negative or zero remapping weights')
else:
    print('Ocean Cells OK')
if bad.max()>0:
    print('There are ',bad[bad>0].sum(),' land cells with positive remapping weights')
else:
    print('Land Cells OK')
