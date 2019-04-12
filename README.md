# NegativeC

Please note that this repository is mostly for illustrative purposes. Consider
it as one-shot simulation set of scripts. General purpose package will be 
available soon.

Here is a collection of tools to run and process negative capacitance
simulations conducted within FERRET module for MOOSE framework.

## Notes on using

To run these codes you will need:

* Python 3.4 or higher
* Numpy, Scipy and Matplotlib
* [netCDF4](https://www.unidata.ucar.edu/software/netcdf/) with Python bindings 
* [Gmsh](http://gmsh.info/)
* [MOOSE](http://mooseframework.org/) and [Ferret](https://bitbucket.org/mesoscience/ferret)
* ffmpeg

## Brief description

To run simulation you need to config variables in the __pderunner.py__ script.
Variables are encoded as python lists or numpy arrays. If variable has only
single value across simulations, then it is just single element list.
__sim.i__ contains MOOSE/Ferret configuration of simulation. Notice templated
variables (_{subs:var}_), which are substituted from __pde.py__ script.

To reproduce s-curves figure one can use __picture.py__ script.

Domain wall movement movie was made using of __domain_wall_evo.py__
script. It allows you to generate single pictures and then glue them
with __make_video.sh__ script.
