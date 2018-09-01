from copy import deepcopy
from sys import exit
from subprocess import run
from Indices import Indices
import pickle
import path_conf
from pathlib import Path
import math

def create_mesh(mesh_parameters, only_consume):
    msh_name = 'width_eq_{}_thickness_eq_{}'.format(mesh_parameters['dimx'], mesh_parameters['thickness_ferro'])
    processed_template = msh_name + '.geo'
    msh_name = msh_name + '.msh'
    
    if not only_consume:
        msh = Path('./{}'.format(msh_name))
        if msh.exists():
            pass
        else:
            prepend_lines = ['SetFactory("OpenCASCADE");\n']
            for k in mesh_parameters:
                prepend_lines.append('{} = {};\n'.format(k, mesh_parameters[k]))

            template = 'template_mesh_ST-PT-ST.geo'
            with open(template, 'r') as geo:
                geo_content = geo.readlines()

            geo = Path('./{}'.format(processed_template))
            if geo.exists():
                pass
            else:
                with open(processed_template, 'w') as geo:
                    geo.writelines(prepend_lines)
                    geo.writelines(geo_content)

                return_code = run("{} -3 {} -format msh -o {}".format(path_conf.gmsh_path, processed_template, msh_name), shell=True)

    return msh_name

def congifure_parameters(variables, global_parameters):
    parameters = {}
    
    t = variables['t']
    um = variables['um']
    phase = variables['phase']
    need_prev = variables['need_prev']
    ferro_width = variables['ferro_width']
    para_width = variables['para_width']
    thickness = variables['thickness']
    sigma = variables['sigma']
    
    if phase not in 'rcaiz':
        print("Wrong phase - {}!".format(phase))
        exit(1)
    
    alpha1 = 3.8 * (t - 479.0) * 10.0**(-4) 
    alpha3 = 3.8 * (t - 479.0) * 10.0**(-4)
    alpha11 = -0.73 * 10**(-1)
    alpha12 = 7.5 * 10**(-1)
    alpha111 = 2.6 * 10**(-1)
    alpha112 = 6.1 * 10**(-1)
    alpha123 = -37.0 * 10**(-1)
    Q11 = 0.089 
    Q12 = -0.026
    Q44 = 0.0675 
    s11 = 8.0 * 10.0**(-3)
    s12 = -2.5 * 10.0**(-3)
    s44 = 9.0 * 10.0**(-3)
    
    alpha1_star = alpha1 - um * ( (Q11 + Q12) / (s11 + s12) )
    alpha3_star = alpha1 - um * ( (2.0 * Q12) / (s11 + s12) )
    alpha11_star = ( alpha11 + 0.5 * ( 1.0 / (s11**2.0 - s12**2.0) ) *
                            ( s11*(Q11**2.0 + Q12**2.0) - 2.0*Q11*Q12*s12 ) )
    alpha33_star = ( alpha11 + ( (Q12**2.0) / (s11 + s12) ) )
    alpha13_star = ( alpha12 + ( Q12*(Q11 + Q12) / (s11 + s12) ) )
    alpha12_star = ( alpha12 - ( 1.0 / (s11**2.0 - s12**2.0) ) *
                            ( s12*(Q11**2.0 + Q12**2.0) - 2.0*Q11*Q12*s11 ) +
                            ( (Q44**2.0) / (2.0*s44) ) )
    parameters['alpha111'] = alpha111
    parameters['alpha112'] = alpha112
    parameters['alpha123'] = alpha123
    
    parameters['alpha1'] = "'{} {}'".format(alpha1_star, alpha3_star)
    parameters['alpha11'] = "'{} {}'".format(alpha11_star, alpha33_star)
    parameters['alpha12'] = "'{} {}'".format(alpha12_star, alpha13_star)
    
    parameters['G110'] = 0.173
    parameters['G11_G110'] = 1.6
    parameters['G12_G110'] = 0
    parameters['G44_G110'] = 0.8
    parameters['G44P_G110'] = 0.8
    
    parameters['eps_0'] = 8.85 * 10**(-3)
    parameters['eps_i'] = 10.0
    parameters['permittivity_electrostatic_ferro'] = parameters['eps_0'] * parameters['eps_i']
    parameters['permitivitty_depol_ferro'] = parameters['eps_0'] * parameters['eps_i']
    
    parameters['lmbd'] = 1.0
    parameters['sigma'] = sigma
    
    parameters['up_pot'] = 0.0
    parameters['bottom_pot'] = 0.0
    
    parameters['ferro_robin_alpha'] = 0.1
    parameters['ferro_robin_beta'] = 1.0
    
    parameters['ax'] = '{}'.format(ferro_width)
    parameters['af'] = '{}'.format(thickness)
    parameters['min_domain_perturbation'] = '{}'.format(-1e-5)
    parameters['max_domain_perturbation'] = '{}'.format(1e-5)
    
    parameters['polar_x_value_min'], parameters['polar_x_value_max'], parameters['polar_y_value_min'], parameters['polar_y_value_max'], parameters['polar_z_value_min'], parameters['polar_z_value_max'] = {
        'c' : (-1e-5, 1e-5, -1e-5, 1e-5, 0.7, 0.7),
        'a' : (0.5, 0.5, 0.5, 0.5, -1e-5, 1e-5),
        'r' : (0.1, 0.1, 0.1, 0.1, 0.1, 0.1),
        'i' : (-1e-5, 1e-5, -1e-5, 1e-5, -1e-5, 1e-5),
        'z' : (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    }[phase]
    
    parameters['lscale'] = 1.0
    parameters['time_scale'] = 1.0
    
    parameters['filebase'] = 't_{}_um_{}_phase_{}_width_{}_thickness_{}_sigma_{}'.format(t, um, phase, ferro_width, thickness, sigma)

    mesh_parameters = {
        'lc' : 1.0,
        'thickness_para' : thickness / 2,
        'thickness_ferro' : thickness,
        'layers_para' : math.ceil(thickness / 2) * 5,
        'layers_ferro' : thickness * 5,
        'dimx' : ferro_width,
        'dispx' : -ferro_width / 2.0,
        'dimy' : 1,
        'dispy' : -0.5
    }
    
    parameters['x_dir_periodic_trans'] = "'{} {} {}'".format(0, 1, 0)
    parameters['y_dir_periodic_trans'] = "'{} {} {}'".format(ferro_width, 0, 0)
    
    parameters['mesh_name'] = 'box1.msh' #create_mesh(mesh_parameters, only_consume = False)

    parameters['active_bcs'] = "''" #"'zero_column_x zero_column_y zero_column_z'"
    #parameters['active_meshmod'] = "'column'"
    #parameters['column_coords'] = "'{}'".format(' '.join(['{} {} {}'.format(c.x, c.y, c.z) for c in columns]))
    
    if need_prev:
        parameters['active_ics'] = "'pxic pyic pzic'"
        parameters['active_funcs'] = "'pxf pyf pzf'" 
        parameters['active_user_objects'] = "'soln kill'"
        parameters['previous_sim'] = "'{}.e'".format(global_parameters[-1]['previous_sim_name'])
    else:
        parameters['active_ics'] = "'ic_polar_x_ferro_random ic_polar_y_ferro_random ic_polar_z_ferro_func'" #pz_dom_ic ic_polar_z_ferro_random
        parameters['active_funcs'] = "'initial_cond_func'" #polar_func
        parameters['active_user_objects'] = "'kill'"
        parameters['previous_sim'] = "'{}.e'".format('none_prev_sim')
        
    global_parameters.append(deepcopy(parameters))
    global_parameters[-1]['previous_sim_name'] = parameters['filebase']
    
    return parameters

class Template:
    def __init__(self, template):
        with open(template) as config:
            lines = config.readlines()
        self.lines = lines

    def prepare_template(self, parameters):
        subs = {name : [] for name in parameters}
        for line_number, line in enumerate(self.lines):
            for sp in subs:
                if '{{subs:{}}}'.format(sp) in line:
                    subs[sp].append(line_number)
                    
        new_config = deepcopy(self.lines)
        
        for sub in subs:
            for ln in subs[sub]:
                new_config[ln] = new_config[ln].split('=')[0] + ' = ' + "{}\n".format(parameters[sub])
                
        return new_config

def simulation(arguments):
    orders = [int(arguments[entry]['order']) for entry in [var for var in arguments]]
    orders = sorted(list(set(orders)))
    prepared_parameters = [[] for i in range(len(orders))]
    for order in orders:
        ktd = []
        for arg in arguments:
            if arguments[arg]['order'] == order:
                prepared_parameters[order].append(arguments[arg])
                ktd.append(arg)
        for k in ktd:
            del arguments[k]

    for p in prepared_parameters:
        if len(p) > 1:
            lens = []
            for entry in p:
                lens.append(len(entry))
            for li in range(len(lens) - 1):
                if lens[li] != lens[li - 1]:
                    print("Parameters of same order should have same length!")
                    exit(1)

    try:
        indices = Indices([len(p[0]['values']) - 1 for p in prepared_parameters])
    except ValueError as e:
        print(e)
        indices = [tuple(0 for i in range(len(prepared_parameters)))]
    
    global_parameters = [{'previous_sim_name':'prev'}] #[{'previous_sim_name':'t_25_um_-0.013_phase_i_width_5_thickness_3_prev'}]
    
    template = Template('sim.i')

    for ind in indices:
        conf_args = {}
        configs = [{pe['name'] : pe['values'][ind[n]] for pe in p} for n, p in enumerate(prepared_parameters)]
        for c in configs:
            conf_args.update(c)
        parameters = congifure_parameters(conf_args, global_parameters)
        
        simulation_file = '{}.i'.format(parameters['filebase'])
    
        with open(simulation_file, 'w') as new_run_file:
            new_run_file.writelines(template.prepare_template(parameters))
                
        ferret_run = '{} -i {} --n-threads={}'
        retcode = run(ferret_run.format(path_conf.ferret_path, simulation_file, 2), shell=True)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Take serialized parameters.')
    parser.add_argument('--sfile', nargs = 1)
    args = parser.parse_args()
    f = args.sfile[0].strip().split()[0]

    with open(f, 'rb') as inp:
        data = pickle.load(inp)
        
    simulation(data)
