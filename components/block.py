from microfluidics_ipkiss3.technology import * #comment when running main script, uncomment to debug geometry

from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics

import math

#Trap has been updated with boolean operation, to have flat ends

class Block(i3.PCell):
    """A generic cell trap class. It is defined by a boundary which are defined by points
    """
    _name_prefix = "BLOCK" # a prefix added to the unique identifier
    channel_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate(), doc="Channel template")
    TECH = i3.get_technology()
    class Layout(i3.LayoutView):
        # definition of the default values of the block PCELL
        block_length = i3.PositiveNumberProperty(default = 300.0)

        def _generate_elements(self, insts):

            block_width = self.channel_template.channel_width

            point_list = []

            point_list.append( (-self.block_length*0.5, -block_width*0.5))
            point_list.insert(0,  (-self.block_length*0.5, block_width*0.5))

            point_list.append( (self.block_length*0.5, -block_width*0.5))
            point_list.insert(0, (self.block_length*0.5, block_width*0.5))

            t = i3.Shape(point_list, closed=True)
            bo = i3.Boundary(i3.TECH.PPLAYER.CH2.TRENCH, t)
            insts += bo  #comm/uncomm for debugging round stl

            return insts

        def _generate_ports(self, ports):

            #port1
            ports += microfluidics.FluidicPort(name='in1', position = (-self.block_length*0.5, 0.0),
                                               direction = i3.PORT_DIRECTION.IN,
                                               angle_deg=180,
                                               trace_template=self.channel_template
                                               )

            ports += microfluidics.FluidicPort(name='out1', position = (self.block_length*0.5, 0.0),
                                               direction = i3.PORT_DIRECTION.IN,
                                               angle_deg=0,
                                               trace_template=self.channel_template
                                               )

            return ports



if __name__ == "__main__":
    print "This is not the main file. Run 'execute.py' in the same folder"
    #from microfluidics_ipkiss3.technology import *


    trap = Block()
    #trap = CellTrapRounded()
    trap_layout= trap.Layout()
    trap_layout.visualize(annotate = True)
    trap_layout.visualize_2d()

    #STL and OF sim

    from microfluidics_ipkiss3.pysimul.openfoam.openfoam_engine import *
    from microfluidics_ipkiss3.pysimul.openfoam.turbulence_model import *
    from microfluidics_ipkiss3.pysimul.openfoam.transport_model import *

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

    transport_model = NewtonianModel(kinematic_viscosity=0.001 / 1050)
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
    params["inlets"] = [FixedVelocityInlet(in_port_number=0, velocity=(50e-3, 0, 0)),
                        #FixedVelocityInlet(in_port_number=1, velocity=(0.0, -30e-3, 0.0)),
                        #FixedVelocityInlet(in_port_number=2, velocity=(0.0, 30e-3, 0.0))
                         ]

    window_si = SizeInfo(west=-250, east=250, south=-360, north=360)
    params["window_size_info"] = window_si

    # 2D simulation
    params["dimensions"] = 3

    # Create and run simulation

    from ipkiss.plugins.simulation import *

    simul = trap_layout.create_simulation(simul_params=params)

    # Start running simulation

    simul.procedure.run(case_name='one_blockt', use_existing_mesh=False, interactive=True)
