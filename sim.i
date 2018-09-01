[Mesh]
  type = FileMesh
  file = {subs:mesh_name}
[]

[Variables]
  [./polar_x]
    order = FIRST
    family = LAGRANGE
  [../]
  [./polar_y]
    order = FIRST
    family = LAGRANGE
  [../]
  [./polar_z]
    order = FIRST
    family = LAGRANGE
  [../]
[]

[ICs]
  active = {subs:active_ics}
  
  #RANDOM CONDITIONS FOR FIRST ITERATION
  [./ic_polar_x_ferro_random]
    type = RandomIC
    min = {subs:polar_x_value_min}
    max = {subs:polar_x_value_max}
    variable = polar_x
  [../]
  [./ic_polar_y_ferro_random]
    type = RandomIC
    min = {subs:polar_y_value_min}
    max = {subs:polar_y_value_max}
    variable = polar_y
  [../]
  [./ic_polar_z_ferro_random]
    type = RandomIC
    min = {subs:polar_z_value_min}
    max = {subs:polar_z_value_max}
    variable = polar_z
  [../]
  
  [./ic_polar_z_ferro_func]
    type = FunctionIC
    function = initial_cond_func
    variable = polar_z
  [../]
  
  [./pxic]
      type = FunctionIC
      variable = polar_x
      function = pxf
  [../]
  [./pyic]
    type = FunctionIC
    variable = polar_y
    function = pyf
  [../]
  [./pzic]
    type = FunctionIC
    variable = polar_z
    function = pzf
  [../]
  
  [./pz_dom_ic]
    type = FunctionIC
    variable = polar_z
    function = polar_func
  [../]
[]

[Functions]
  active = {subs:active_funcs}
  
  [./pxf]
    type = SolutionFunction
    solution = soln
    from_variable = polar_x
  [../]
  [./pyf]
    type = SolutionFunction
    solution = soln
    from_variable = polar_y
  [../]
  [./pzf]
    type = SolutionFunction
    solution = soln
    from_variable = polar_z
  [../]
  
  
  [./initial_cond_func]
    type = ParsedFunction
    value = cos(y/20*pi)
  [../]
  
  [./polar_func]
    type = DomainFunc
    af = {subs:af}
    ax = {subs:ax}
    min = {subs:min_domain_perturbation}
    max = {subs:max_domain_perturbation}
  [../]
[]

[Kernels]
  #FERROELECTRIC BLOCK
  [./bed_x_ferro]
    type = BulkEnergyDerivativeSixthAlt
    variable = polar_x
    polar_x = polar_x
    polar_y = polar_y
    polar_z = polar_z
    alpha1 = {subs:alpha1}
    alpha11 = {subs:alpha11}
    alpha12 = {subs:alpha12}
    alpha111 = {subs:alpha111}
    alpha112 = {subs:alpha112}
    alpha123 = {subs:alpha123}
    component = 0
  [../]
  [./bed_y_ferro]
    type = BulkEnergyDerivativeSixthAlt
    variable = polar_y
    polar_x = polar_x
    polar_y = polar_y
    polar_z = polar_z
    alpha1 = {subs:alpha1}
    alpha11 = {subs:alpha11}
    alpha12 = {subs:alpha12}
    alpha111 = {subs:alpha111}
    alpha112 = {subs:alpha112}
    alpha123 = {subs:alpha123}
    component = 1
  [../]
  [./bed_z_ferro]
    type = BulkEnergyDerivativeSixthAlt
    variable = polar_z
    polar_x = polar_x
    polar_y = polar_y
    polar_z = polar_z
    alpha1 = {subs:alpha1}
    alpha11 = {subs:alpha11}
    alpha12 = {subs:alpha12}
    alpha111 = {subs:alpha111}
    alpha112 = {subs:alpha112}
    alpha123 = {subs:alpha123}
    component = 2
  [../]

  [./walled_x_ferro]
    type = WallEnergyDerivative
    variable = polar_x
    polar_x = polar_x
    polar_y = polar_y
    polar_z = polar_z
    len_scale = {subs:lscale}
    G110 = {subs:G110}
    G11_G110 = {subs:G11_G110}
    G12_G110 = {subs:G12_G110}
    G44_G110 = {subs:G44_G110}
    G44P_G110 = {subs:G44P_G110}
    component = 0
  [../]
  [./walled_y_ferro]
    type = WallEnergyDerivative
    variable = polar_y
    polar_x = polar_x
    polar_y = polar_y
    polar_z = polar_z
    len_scale = {subs:lscale}
    G110 = {subs:G110}
    G11_G110 = {subs:G11_G110}
    G12_G110 = {subs:G12_G110}
    G44_G110 = {subs:G44_G110}
    G44P_G110 = {subs:G44P_G110}
    component = 1
  [../]
  [./walled_z_ferro]
    type = WallEnergyDerivative
    variable = polar_z
    polar_x = polar_x
    polar_y = polar_y
    polar_z = polar_z
    len_scale = {subs:lscale}
    G110 = {subs:G110}
    G11_G110 = {subs:G11_G110}
    G12_G110 = {subs:G12_G110}
    G44_G110 = {subs:G44_G110}
    G44P_G110 = {subs:G44P_G110}
    component = 2
  [../]

  [./polar_x_time_ferro]
     type = TimeDerivativeScaled
     variable = polar_x
     time_scale = {subs:time_scale}
  [../]
  [./polar_y_time_ferro]
     type = TimeDerivativeScaled
     variable = polar_y
     time_scale = {subs:time_scale}
  [../]
  [./polar_z_time_ferro]
     type = TimeDerivativeScaled
       variable = polar_z
       time_scale = {subs:time_scale}
  [../]
  
  [./depol_z_ferro]
      type = DepolEnergy
      permitivitty = {subs:permitivitty_depol_ferro}
      lambda = {subs:lmbd}
      len_scale = {subs:lscale}
      variable = polar_z
      avePz = Polar_z_ferro_avg_element
      polar_z = polar_z
      sigma = {subs:sigma}
  [../]
  
[]

[BCs]

   active = {subs:active_bcs}

[]

[Postprocessors]
   [./dt]
     type = TimestepSize
   [../]
  
  [./Fbulk]
      type = BulkEnergy
      polar_x = polar_x
      polar_y = polar_y
      polar_z = polar_z
      alpha1 = {subs:alpha1}
      alpha11 = {subs:alpha11}
      alpha12 = {subs:alpha12}
      alpha111 = {subs:alpha111}
      alpha112 = {subs:alpha112}
      alpha123 = {subs:alpha123}
      execute_on = 'initial timestep_end final'
   [../]
   [./Fwall]
      type = WallEnergy
      polar_x = polar_x
      polar_y = polar_y
      polar_z = polar_z
      G110 = {subs:G110}
      G11_G110 = {subs:G11_G110}
      G12_G110 = {subs:G12_G110}
      G44_G110 = {subs:G44_G110}
      G44P_G110 = {subs:G44P_G110}
      len_scale = {subs:lscale}
      execute_on = 'initial timestep_end final'
    [../]
    [./Fdepol]
      type = DepolEnergyPost
      permitivitty = {subs:permitivitty_depol_ferro}
      lambda = {subs:lmbd}
      len_scale = {subs:lscale}
      avePz = Polar_z_ferro_avg_element
      polar_z = polar_z
      sigma = {subs:sigma}
      execute_on = 'initial timestep_end final'
    [../]

    [./Ftotal]
      type = LinearCombinationPostprocessor
      pp_names = 'Fbulk Fwall Fdepol '
      pp_coefs = '   1     1     1   '
      execute_on = 'initial timestep_end final'
    [../]
    [./perc_change]
     type = EnergyRatePostprocessor
     postprocessor = Ftotal
     dt = dt 
     execute_on = 'initial timestep_end final'
   [../]
   
   [./Polar_x_ferro_avg_element]
    type = ElementAverageValue
    execute_on = 'initial timestep_end final'
    variable = polar_x
   [../]
   [./Polar_y_ferro_avg_element]
    type = ElementAverageValue
    execute_on = 'initial timestep_end final'
    variable = polar_y
   [../]
   [./Polar_z_ferro_avg_element]
    type = ElementAverageValue
    execute_on = 'initial timestep_end final'
    variable = polar_z
   [../]
   
    
   [./Polar_sqr_x_ferro]
     type = PolarizationComponentValue
     polar = polar_x
     execute_on = 'initial timestep_end final'
   [../]
   [./Polar_sqr_y_ferro]
     type = PolarizationComponentValue
     polar = polar_y
     execute_on = 'initial timestep_end final'
   [../]
   [./Polar_sqr_z_ferro]
     type = PolarizationComponentValue
     polar = polar_z
     execute_on = 'initial timestep_end final'
   [../]
    
   [./Polar_ferro]
     type = PolarizationValue
     polar_x = polar_x
     polar_y = polar_y
     polar_z = polar_z
     execute_on = 'initial timestep_end final'
   [../]
[]

[UserObjects]
  active = {subs:active_user_objects}

  [./soln]
    type = SolutionUserObject
    mesh = {subs:previous_sim}
    system_variables = 'polar_x polar_y polar_z'
    timestep = LATEST
    execute_on = initial
 [../]
  
  [./kill]
    type = Terminator
    expression = 'perc_change <= 1.0e-6'
  [../]

[]

[Preconditioning]
  [./smp]
    type = SMP
    full = true
    petsc_options_iname = '-ksp_gmres_restart -snes_atol -snes_rtol -ksp_rtol  -pc_type  '     
    petsc_options_value = '    120               1e-10      1e-8     1e-5        bjacobi '    
    #petsc_options_iname = '-ksp_type -snes_atol -snes_rtol -ksp_rtol -snes_type  -pc_type  -sub_pc_type  -pc_asm_type'
    #petsc_options_value = '  gmres      1e-10      1e-8      1e-5      newtonls       asm       lu           basic   '
  [../]
[]

[Executioner]

  [./TimeStepper]
     type = IterationAdaptiveDT
     dt = 0.01
     growth_factor = 1.414
     cutback_factor =  0.707
  [../]

  type = Transient
  solve_type = 'NEWTON'       #"PJFNK, JFNK, NEWTON"
  scheme = 'bdf2'   #"implicit-euler, explicit-euler, crank-nicolson, bdf2, rk-2"
  
  dtmax = 0.25
[]

[Outputs]
  print_linear_residuals = false
  print_perf_log = true
  
  [./out]
    type = Exodus
    execute_on = 'initial timestep_end final'
    file_base = {subs:filebase}
    elemental_as_nodal = true
    interval = 1
  [../]
  
  [./outcsv]
    type = CSV
    file_base = {subs:filebase}
    execute_on = 'initial timestep_end final'
  [../]
[]
