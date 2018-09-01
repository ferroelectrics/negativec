import netCDF4
import numpy as np
import os
 
def get_coords(data_dir): 
    files = os.listdir(data_dir)
    files = [f for f in files if f.endswith('.e')]
    files.sort(key = lambda name : float(name.split('_')[7]))
    overall_coordinates = []

    for f in files:
        filename = data_dir + f
        nc = netCDF4.Dataset(filename, 'r')

        X = nc.variables['coordx']
        Y = nc.variables['coordy']
        Z = nc.variables['coordz']

        polar_x = nc.variables['vals_nod_var1'][1,:]
        polar_y = nc.variables['vals_nod_var2'][1,:]
        polar_z = nc.variables['vals_nod_var3'][1,:]
        
        overall_coordinates.append((X[:],Y[:],polar_z[:]))
        nc.close()
    
    return overall_coordinates
    
    
