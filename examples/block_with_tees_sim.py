
from microfluidics_ipkiss3.technology import *
from components import CellTrapSimple, TeeSimple
from components.block_with_tees import BlockWithTees

from microfluidics_ipkiss3.pysimul.openfoam.openfoam_engine import *
from microfluidics_ipkiss3.pysimul.openfoam.turbulence_model import *
from microfluidics_ipkiss3.pysimul.openfoam.transport_model import *
from microfluidics_ipkiss3.pysimul.runtime.basic import *       #Thach what is this?

#block = Block()
#block = CellTrapRounded()
block = CellTrapSimple()
block.Layout(cell_trap_length= 300.0)#(block_length= 300.0)
tee = TeeSimple()
tee.Layout(tee_length=300)

myBlock_withTees= BlockWithTees(
                        block = block,
                        tee = tee)
layout = myBlock_withTees.Layout()

#Writing to GDSII and visualization
#layout.write_gdsii("myTrap_withTees.gds")
layout.visualize(annotate = True)

#generating STL and OF sim
# Control how the mesh is generated

snap_control = SnapControl(num_smooth_patch=1)
add_layer_control = AddLayerControl(final_layer_thickness=10, min_thickness=1, num_grow=10)
mesh_quality_control = MeshQualityControl(max_non_orthogonal=90)
mesh_control = MeshControl(mesh_size=20, feature_refinement_level=2,
                           surface_refinement_level=(1, 2),
                           refinement_regions=[(1, 2)],
                           snap_mesh=True, snap_control=snap_control,
                           add_layer=True, add_layer_control=add_layer_control,
                           mesh_quality_control=mesh_quality_control)

# Transport and turbulence models

transport_model = NewtonianModel(kinematic_viscosity=0.00345 / 1050)
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
params["inlets"] = [FixedVelocityInlet(in_port_number=2, velocity=(0.0, 50.0e-3, 0)),
                    FixedVelocityInlet(in_port_number=0, velocity=(0.0, -50e-3, 0.0)),
                    #FixedVelocityInlet(in_port_number=2, velocity=(0.0, 30e-3, 0.0))
                     ]

window_si = SizeInfo(west=-260, east=260, south=-360, north=360)
#params["window_size_info"] = window_si

# 2D simulation
params["dimensions"] = 3

# Create and run simulation

from ipkiss.plugins.simulation import *

simul = layout.create_simulation(simul_params=params)

# Start running simulation

simul.procedure.run(case_name='one_block_with_tees', use_existing_mesh=False, interactive=True)
