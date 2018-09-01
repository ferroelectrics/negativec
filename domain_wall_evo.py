from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cbook as cbook
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from os import listdir
from sys import exit
import csv
from collections import defaultdict, namedtuple
import sqlite3
from functools import partial
import extractor_str
import matplotlib.tri as tri
import matplotlib.gridspec as gridspec
import os
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy import interpolate

def plotzero():
    handles = []

    plt.rcParams["font.family"] = "Times New Roman"
     
    with sqlite3.connect('negativec_zero_cols_2.db') as conn:
        c = conn.cursor()
        
        query = '''select distinct primary_parameters.pnum from primary_parameters order by pnum;'''
        c.execute(query)
        query_result = c.fetchall()
        sigma = list(query_result)

        query = '''select primary_parameters.pnum, secondary_parameters.Ftotal
                from primary_parameters inner join secondary_parameters on primary_parameters.secondary_id=secondary_parameters.id;'''
        c.execute(query)
        query_result = c.fetchall()
        
        with open('box20x20.msh') as msh:
            get_line = lambda msh=msh: msh.readline().strip()
            
            while get_line() != '$Nodes': pass

            num_of_nodes = int(get_line())
            nodes = [get_line().split(' ') for i in range(num_of_nodes)]
            node_coords = {n[0].strip() : n[1:] for n in nodes}
            
        node_numbers_energies = [(str(v[0]),v[1]) for v in query_result]
        
        node_coords_energies = [(float(node_coords[n[0]][0]), float(node_coords[n[0]][1]), n[1]) for n in node_numbers_energies]
         
        x = np.array([n[0] for n in node_coords_energies])
        y = np.array([n[1] for n in node_coords_energies])
        z = np.array([n[2] for n in node_coords_energies])

        enmean = np.sum(z) / z.size
        z = (z - enmean) / enmean

        zfull = z.max() - z.min()
        zlow = z.min() + zfull*0.0
        zhigh = z.max() - zfull*0.5
        zmin = z.min()
        zmax = z.max()

        triang = tri.Triangulation(x, y)
        refiner = tri.UniformTriRefiner(triang)
        tri_refi, z_refi = refiner.refine_field(z, subdiv=3)
        
        coordinates = extractor_str.get_coords('unscos_pview/')

        sigmas = np.loadtxt('B10Q')
        polars = np.loadtxt('B10P')
        fieldv = sigmas[:len(coordinates)]
        field_min = fieldv.min()
        field_max = fieldv.max()

        for i,pack in enumerate(zip(coordinates[:], fieldv[:])):
            c, fv = pack
            coord = [(x,y,z) for x,y,z in zip(c[0][0::5], c[1][0::5], c[2][0::5])]
            
            x1 = np.array([v[0] for v in coord])
            y1 = np.array([v[1] for v in coord])
            z1 = np.array([v[2] for v in coord])

            z1 = (z1 - z1.min()) / (z1.max() - z1.min())

            fig = plt.figure(figsize=(12,11))
            spec = gridspec.GridSpec(ncols=2, nrows=1, wspace=0.1, hspace=0.1, width_ratios=[9, 0.5])
            mainplot = fig.add_subplot(spec[:, 0])
            energyplot = fig.add_subplot(spec[:, 1])

            from matplotlib.colors import LinearSegmentedColormap
            colors = [(0.0, 0.0, 1.0), (0.0, 1.0, 0.0), (1.0, 0.0, 0.0)]
            cmap_name = 'domwall_map'
            mycm = LinearSegmentedColormap.from_list(cmap_name, colors, N=13)

            cf = mainplot.tricontourf(tri_refi, z_refi, cmap=cm.seismic, levels=np.linspace(zlow, zhigh, 271, endpoint=True))
            cf_ = mainplot.tricontourf(x1, y1, z1, cmap=mycm, alpha=0.4, levels=[0.0, 0.35, 0.65, 1.0])

            from matplotlib.collections import PatchCollection
            from matplotlib.patches import Rectangle

            rect = Rectangle((-50, 0), 100, fv)
            pc = PatchCollection([rect])
            energyplot.add_collection(pc)

            x0m,x1m = mainplot.get_xlim()
            y0m,y1m = mainplot.get_ylim()
            mainplot.set_aspect(abs(x1m-x0m)/abs(y1m-y0m))

            mainplot.set(xlabel=r'Side length (nm)', ylabel=r'Side length (nm)')

            energyplot.set_xlim(0,1)
            energyplot.set_ylim(field_min, field_max)
            energyplot.set_xticks([])
            energyplot.tick_params(axis='y', left=False, right=True, labelleft=False, labelright=True)
            energyplot.yaxis.set_label_position('right')

            energyplot.set(ylabel=r'Surface charge, Q/S (C/m$^{2}$)')

            divider = make_axes_locatable(mainplot)
            cax = divider.new_vertical(size="5%", pad=0.9, pack_start=True)
            fig.add_axes(cax) 
            cb = fig.colorbar(cf, cax=cax, orientation="horizontal", label='Normalized domain wall pinning relief', ticks=[zlow + (zhigh-zlow)/5*i for i in range(6)], format=matplotlib.ticker.FuncFormatter(lambda x, p: '{:.2f}'.format(x*1000)))
            cf.set_clim(zlow, zhigh)

            plt.figtext(0.25, 0.9, 'Domain wall displacement as a responce\n          to the charge at the electrodes', fontsize=24)
            plt.figtext(0.78, 0.1175, 'x 10$^{-3}$', fontsize=20)

            for axv in [mainplot, energyplot, cax]:
                for item in ([axv.title, axv.xaxis.label, axv.yaxis.label]):
                    item.set_fontsize(24)
                for item in (axv.get_xticklabels() + axv.get_yticklabels()):
                    item.set_fontsize(20)

            fig.tight_layout()

            plt.savefig('{}.png'.format(i))
            plt.close()
