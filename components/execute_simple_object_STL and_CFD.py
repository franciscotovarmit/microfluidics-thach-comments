
from microfluidics_ipkiss3.technology import * #comment when running main script, uncomment to debug geometry

from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics

from trap import CellTrapSimple

TECH = i3.get_technology()
trap = CellTrapSimple()
#trap = CellTrapRounded()
trap_layout= trap.Layout()
trap_layout.visualize(annotate = True)
trap_layout.visualize_2d()

# Pressure Drop calculation

from circuits_using_components.functions.resistance import calculate_resistance, calculate_pressure_drop, \
    convertFlowRateuLminTom3s, velocityCFD

QuLmin = 10
Qm3s = convertFlowRateuLminTom3s(QuLmin)

# wide section
lengthWide = trap_layout.cell_trap_length - trap_layout.cell_trap_gap_length
widthWide = trap_layout.channel_template.channel_width
height = 20  # i3.TECH.MATERIALS.MSTACK_SU8_HEIGHT #i3.TECH.MATERIALS.SU8   #THACH HOW to do this?
inlet_velocity = velocityCFD(Qm3s, widthWide * 1e-6, height * 1e-6)
RWide = calculate_resistance(lengthWide * 1e-6, widthWide * 1e-6, height * 1e-6)
PWide = calculate_pressure_drop(RWide)
# gap section
length = trap_layout.cell_trap_gap_length
width = trap_layout.cell_trap_gap
height = 20
RTrap = calculate_resistance(length * 1e-6, height * 1e-6, width * 1e-6)
PTrap = calculate_pressure_drop(RTrap)
print 'L trap trap: ', length
print 'W trap trap: ', width
print 'Pressure drop trap', PTrap
print 'Resistance trap', RTrap

TotalP = PWide + PTrap
TotalR = RWide + RTrap
print 'Pressure drop', TotalP / 1000
print 'Resistance', TotalR
# End pressure Calculation

# STL and OF sim

from microfluidics_ipkiss3.pysimul.openfoam.openfoam_engine import *
from microfluidics_ipkiss3.pysimul.openfoam.turbulence_model import *
from microfluidics_ipkiss3.pysimul.openfoam.transport_model import *

# Control how the mesh is generated

snap_control = SnapControl(num_smooth_patch=1)
add_layer_control = AddLayerControl(final_layer_thickness=10, min_thickness=1, num_grow=10)
mesh_quality_control = MeshQualityControl(max_non_orthogonal=90)
mesh_control = MeshControl(mesh_size=10, feature_refinement_level=2,
                           surface_refinement_level=(1, 4),
                           refinement_regions=[(1, 2)],
                           snap_mesh=True, snap_control=snap_control,
                           add_layer=True, add_layer_control=add_layer_control,
                           mesh_quality_control=mesh_quality_control)

# Transport and turbulence models

transport_model = NewtonianModel(kinematic_viscosity=8.94e-4 / 1000)
turbulence_model = LaminarModel()

# Create a list of properties required by simpleFoam solver including the transport property
# and a list of properties returned by turbulenace model

properties = [transport_model.get_model_property()] + turbulence_model.get_model_properties()

# Initialise the engine with simpleFoam solver

engine = OpenFoamEngine(mesh_control=mesh_control, solver='simpleFoam',
                        properties=properties)

from microfluidics_ipkiss3.pysimul.runtime.basic import *

params = dict()
params["engine"] = engine
params["inlets"] = [FlowRateInletVelocity(in_port_number=0, flowRate=(Qm3s)),
                    # FixedVelocityInlet(in_port_number=0, velocity=(inlet_velocity, 0, 0)),  #0.019 #94.3
                    # FixedVelocityInlet(in_port_number=1, velocity=(0.0, -30e-3, 0.0)),
                    # FixedVelocityInlet(in_port_number=2, velocity=(0.0, 30e-3, 0.0))
                    ]

window_si = SizeInfo(west=-250, east=250, south=-360, north=360)
# params["window_size_info"] = window_si

# 2D simulation
params["dimensions"] = 3

# Create and run simulation

from ipkiss.plugins.simulation import *

simul = trap_layout.create_simulation(simul_params=params)

# Start running simulation

simul.procedure.run(case_name='one_blocktFlowRate', use_existing_mesh=False, interactive=True)

print 'Qm3s', Qm3s
print 'vel: ', inlet_velocity
print 'L trap wide: ', lengthWide
print 'W trap wide: ', widthWide
print 'Pressure drop wide', PWide
print 'Resistance wide', RWide

print 'Pressure drop trap', PTrap
print 'Resistance trap', RTrap

print 'Pressure drop', TotalP
print 'Pressure drop 1/rho', TotalP / 1000