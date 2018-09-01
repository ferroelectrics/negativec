import numpy as np
import math
import matplotlib as mpl
from matplotlib import colors as mcolors
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
from matplotlib import ticker
from matplotlib.ticker import FuncFormatter, MaxNLocator

plt.rcParams["font.family"] = "Arial"

def mirror_plot(x, y):
    ex_x = np.append(-x[::-1], x)
    ex_y = np.append(-y[::-1], y)
    return ex_x, ex_y

handles = []
labels = []

fig = plt.figure()

tta = fig.text(0.13, 0.86, "a", ha="center", va="center", size=32)
ttb = fig.text(0.35, 0.86, "b", ha="center", va="center", size=32)

spec = gridspec.GridSpec(ncols=2, nrows=1, wspace=0.1, hspace=0.0, width_ratios=[1, 2])
ax = fig.add_subplot(spec[:, 1:])
ax.set_xlim([-0.23, 0.23])
axins = plt.axes([0.75, 0.47, 0.18, 0.275]) #inset_axes(ax, width='20%', height='30%', loc=1) #zoomed_inset_axes(ax, 3, loc=1) 

ax.annotate('(3)', xy=(-0.045, 0.47), xytext=(-0.09, 0.47), arrowprops=dict(facecolor='black', width=2, headwidth=8), size=18)
ax.annotate('(2)', xy=(-0.02, 0.26), xytext=(-0.06, 0.35), arrowprops=dict(facecolor='black', width=2, headwidth=8), size=18)
ax.annotate('(1)', xy=(0.005, 0.01), xytext=(0.03, 0.1), arrowprops=dict(facecolor='black', width=2, headwidth=8), size=18)

ax.scatter([-0.04], [0.47], s=100, c='tab:orange', edgecolors='white', linewidths=1.5, zorder=10)
ax.scatter([-0.016], [0.26], s=100, c='tab:orange', edgecolors='white', linewidths=1.5, zorder=10)
ax.scatter([0.0], [0.01], s=100, c='tab:orange', edgecolors='white', linewidths=1.5, zorder=10000)

bases = ['D02', 'D05', 'D10', 'B10', 'S00', 'Rand10', 'Back10', 'Rev10']
Qs = {b:'{}Q'.format(b) for b in bases}
Ps = {b:'{}P'.format(b) for b in bases}
names = {'D02':r'Cylindrical nanodot, R = 2 nm', 
         'D05':r'Cylindrical nanodot, R = 5 nm', 
         'D10':r'Cylindrical nanodot, R = 10 nm', 
         'B10':r'Rectangular nanodot, 20x20 nm', 
         'Back10':r'Cylindrical nanodot, Backward 10 nm',
         'Rand10':r'Cylindrical nanodot, Random 10 nm',
         'S00':'Ideal s-curve',
         'Rev10':'Cylindrical nanodot, R = 10 nm, reverse',
         'tc':'Theoretical curves'}

sigma = np.loadtxt(Qs['Rand10'])
polar = np.loadtxt(Ps['Rand10'])
sigma, polar = mirror_plot(sigma, polar)
sigma1 = ((sigma+polar) / (8.85*10**(-2.0)))[::3]
polar1 = -polar[::3]
todel = sigma1 > -0.015
sigma1 = sigma1[todel]
polar1 = polar1[todel]
todel = sigma1 < 0.0025
sigma1 = sigma1[todel]
polar1 = polar1[todel]
axins.plot(sigma1, polar1, 'o', markersize=5, alpha=0.2)

for name in ['D02', 'D05', 'D10', 'B10']:
    sigma = np.loadtxt(Qs[name])
    polar = np.loadtxt(Ps[name])
    sigma, polar = mirror_plot(sigma, polar)
    h, = ax.plot((sigma+polar) / (8.85*10**(-2.0)), -polar, 'o-', markersize=5, label = '{}'.format(name))
    if name == 'D02':
        axins.plot((sigma+polar) / (8.85*10**(-2.0)), -polar, 'o-', markersize=5, color='tab:blue')
    if name == 'D05':
        axins.plot((sigma+polar) / (8.85*10**(-2.0)), -polar, 'o-', markersize=5, color='tab:orange')
    if name == 'B10':
        axins.plot((sigma+polar) / (8.85*10**(-2.0)), -polar, 'o-', markersize=5, color='tab:red')
    if name == 'D10':
        axins.plot((sigma+polar) / (8.85*10**(-2.0)), -polar, 'o-', markersize=5, color='tab:green')
    handles.append(h)
    labels.append(names[name])
   
sigma = np.loadtxt(Qs['S00'])
polar = np.loadtxt(Ps['S00'])
sigma, polar = mirror_plot(sigma, polar)
ax.plot((sigma+polar) / (8.85*10.0**(-2.0)), -polar, linewidth=2, label = '{}'.format('S00'))

for fitps in zip([2,5,10], [range(0,4100), range(0,4550), range(0,4700)]):
    fit_e = np.loadtxt('Efit{}.out'.format(fitps[0]))[fitps[1]]
    fit_p = np.loadtxt('Pfit{}.out'.format(fitps[0]))[fitps[1]]
    fit_e, fit_p = mirror_plot(fit_e, fit_p)
    theoretical_h, = ax.plot(fit_e, fit_p, linewidth=2, color='black', alpha=0.5, label = '{}'.format('tc'))
handles.append(theoretical_h)
labels.append(names['tc'])

x1, x2, y1, y2 = -0.025, 0.01, 0.0, 0.4
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.yaxis.get_major_locator().set_params(nbins=7)
axins.xaxis.get_major_locator().set_params(nbins=7)

rect = patches.Rectangle((-0.03,0),0.04,0.44,linewidth=1,edgecolor='black',facecolor='none', zorder=100)
ax.add_patch(rect)

con = patches.ConnectionPatch((0.01,0.44), (0.075,0.64), 'data', 'data', shrinkA=0, shrinkB=0, fc="w")
ax.add_artist(con)
con1 = patches.ConnectionPatch((0.01,0.0), (0.07,-0.05), 'data', 'data', shrinkA=0, shrinkB=0, fc="w")
ax.add_artist(con1)

axins.axvline(x=0, linewidth=1, color='black') 
axins.set_xticks([-0.015,0.0,x2])
def my_formatter_fun(x, p):
    if x == 0.0:
        return 0.0
    return "%.1e" % (x)
 
ax.set(xlabel=r'Electric field, E (kV/cm)', ylabel=r'Polarization, P (C/m$^{2}$)')

ax.axhline(y=0, linewidth=1, color='black') 
ax.axvline(x=0, linewidth=1, color='black') 

def isclose(val1, val2, delta=0.0001):
    return abs(val1-val2) < delta

def format_fn(tick_val, tick_pos):
    if any((isclose(tick_val, v) for v in (-0.2, -0.1, 0.1, 0.2))):
        return int(math.ceil(tick_val * 10000.0)) 
    elif isclose(tick_val, 0.0):
        return 0
    else:
        return ''
    
ax.xaxis.set_major_formatter(FuncFormatter(format_fn))

def format_fn_axins(tick_val, tick_pos):
    if any((isclose(tick_val, v) for v in (-0.015, 0.01))):
        return int(math.ceil(tick_val * 10000.0)) 
    elif isclose(tick_val, 0.0):
        return 0
    else:
        return ''
    
axins.xaxis.set_major_formatter(FuncFormatter(format_fn_axins))

for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(2.0)
    axins.spines[axis].set_linewidth(2.0)
for item in ([ax.title, ax.xaxis.label, ax.yaxis.label]):
    item.set_fontsize(24)
for item in (ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(20)
for item in (axins.get_xticklabels() + axins.get_yticklabels()):
    item.set_fontsize(18)
    
ax.tick_params(axis='x', direction='in', length=5, width=2)
ax.tick_params(axis='y', direction='in', length=5, width=2)
axins.tick_params(axis='x', direction='in', length=5, width=2)
axins.tick_params(axis='y', direction='in', length=5, width=2)

ax1 = fig.add_subplot(spec[:, 0])
img = mpimg.imread('picture6.png')
ax1.imshow(img)
ax1.set_xticks([])
ax1.set_yticks([])

axbox = ax.get_position()
ax.legend(handles, labels, loc=(axbox.x0-0.4, axbox.y0+0.1), prop={'size': 18}, frameon=False)
plt.show()
