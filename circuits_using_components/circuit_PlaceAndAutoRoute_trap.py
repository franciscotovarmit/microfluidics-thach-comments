from microfluidics_ipkiss3.technology import * #comment when running main script, uncomment to debug geometry
from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics

from components.trap import CellTrapSimple
from components.tee import TeeSimple
from components.trap_with_tees import TrapWithTees


# PCell containing several traps
class CircuitOfBlocks(microfluidics.PlaceAndAutoRoute):
    """Parametric cell with several traps, which are stacked vertically (Parallel) or horizontally (Series)
    """
    #_name_prefix = "circuitOfTraps"
    type = i3.NumberProperty(default = 0) #  0 Paralell 1 Series
    block_distance = i3.NumberProperty(default = 400.) #distance betwn traps
    block_with_tee = i3.ChildCellListProperty() #  Generating traps with Tee from Child Cell List Property
    trace_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate())
    n_blocks_x = i3.PositiveIntProperty(default = 30)
    n_blocks_y = i3.PositiveIntProperty(default = 30)
    x_footprint = i3.PositiveIntProperty(default = 1000)
    y_footprint = i3.PositiveIntProperty(default = 1000)

    def _default_child_cells(self):
        return {"blk_w_tee{}".format(cnt) : self.block_with_tee[cnt]
                for cnt in range(self.n_blocks_x*self.n_blocks_y)}


    def _default_links(self):
        links = []
        bx = self.n_blocks_x

        ########################
        #############   PARALLEL
        if self.type == 0:
            for cntx in range(0, self.n_blocks_x):
                # self connection at the top -bypass
                top = self.n_blocks_y * self.n_blocks_x - self.n_blocks_x + cntx
                links.append(("blk_w_tee{}:in2".format(top),"blk_w_tee{}:out2".format(top)))
                # connecting bottom to top
                for cnty in range(0, self.n_blocks_y-1):
                    links.append(("blk_w_tee{}:in2".format(cnty*bx+cntx), "blk_w_tee{}:in1".format((cnty+1)*bx+cntx)))
                    links.append(("blk_w_tee{}:out2".format(cnty*bx+cntx), "blk_w_tee{}:out1".format((cnty+1)*bx+cntx)))

            #interconnecting horizontally
            if self.n_blocks_x > 1:
                for cntd in range(0, self.n_blocks_x-1):
                    links.append(("blk_w_tee{}:out1".format(cntd), "blk_w_tee{}:in1".format(cntd+1)))
        ########  END PARALLEL #################

        ########################
        #############   SERIES
        if self.type == 1:             # series
            #all by-pass, each object
            for cnt in range(0, self.n_blocks_y*self.n_blocks_x): #all bypass
                links.append(("blk_w_tee{}:in2".format(cnt), "blk_w_tee{}:out2".format(cnt)))

            #all interconnecting horizontally
            if self.n_blocks_x > 1:
                for cnty in range(0, self.n_blocks_y):
                 for cntd in range(0, (self.n_blocks_x-1)):
                    links.append(("blk_w_tee{}:out1".format(cnty*bx+cntd), "blk_w_tee{}:in1".format(cnty*bx+cntd+1)))

            #left connections
            for cntd in range(1, (self.n_blocks_y-1),2):
                #links.append(("blk_w_tee{}:in1".format(cntd * bx), "blk_w_tee{}:in1".format((cntd+1) * bx)))
                links.append(("blk_w_tee{}:in1".format((cntd+1) * bx), "blk_w_tee{}:in1".format(cntd * bx)))

            #right connections
            for cntd in range(1, (self.n_blocks_y),2):
                links.append(("blk_w_tee{}:out1".format(cntd * bx-1), "blk_w_tee{}:out1".format((cntd+1) * bx-1)))

        ########  END SERIES #################

        return links




    def _default_block_with_tee(self):  # Generating traps from Child Cell List Property
        tee1 = TeeSimple()
        tee1.Layout(tee_length=(200.0))
        my_block = CellTrapSimple()
        my_block.Layout(cell_trap_length= 300.0)
        return [TrapWithTees(name="blk_w_tee_{}".format(cnt),
                             trap=my_block,
                             tee=tee1,
                             )
                for cnt in range(self.n_blocks_x*self.n_blocks_y)]

    class Layout(microfluidics.PlaceAndAutoRoute.Layout):

        def _default_child_transformations(self):

            # generate grid
            x = np.linspace(0, self.cell.x_footprint, self.cell.n_blocks_x)
            y = np.linspace(0, self.cell.y_footprint, self.cell.n_blocks_y)

            # generate positions
            from functions.position_coordinates import generate_positions
            coords = generate_positions(x, y, self.type)

            return {"blk_w_tee{}".format(cnt): i3.Translation(coords[cnt])
                 for cnt in range(self.n_blocks_x*self.n_blocks_y)}

        def _generate_ports(self, ports):
            # Add ports
            if self.type == 0:
                ports += i3.expose_ports(self.instances,{
                    'blk_w_tee0:in1': 'in1',
                    'blk_w_tee{}:out1'.format(self.n_blocks_x-1): 'out1'
                })

            if self.type == 1:
                if self.n_blocks_y %2 == 0:
                    ports += i3.expose_ports(self.instances,{
                    'blk_w_tee0:in1': 'in1',
                    'blk_w_tee{}:in1'.format(self.n_blocks_x*self.n_blocks_y-self.n_blocks_x): 'out1' # last left
                })
                else:
                    ports += i3.expose_ports(self.instances, {
                        'blk_w_tee0:in1': 'in1',
                        'blk_w_tee{}:out1'.format(self.n_blocks_x*self.n_blocks_y - 1): 'out1'  # last right
                    })

            return ports

if __name__ == "__main__":
    print "This is not the main file. Run 'execute.py' in the same folder"
    import numpy as np
    x_footp = 3500 #foot print of array on X
    y_footp = 3500 #foot print of array on Y
    n_traps_x= 2
    n_traps_y = 2

    myCircuiTrap = CircuitOfBlocks(name = "circuitOfTraps",
                             n_blocks_x = n_traps_x,
                             n_blocks_y = n_traps_y,
                             x_footprint = x_footp,
                             y_footprint = y_footp,
                             type= 1# 0 Paralell, 1 Series
                          )

    myCircuiTrap_layout = myCircuiTrap.Layout(bend_radius =200)
    myCircuiTrap_layout.visualize(annotate = True)
    s = myCircuiTrap_layout.get_channels_shapes()
    size = myCircuiTrap_layout.size_info()
    cells = myCircuiTrap_layout.get_cell()

    #new_Shape = i3.Shape([(-350, 3800),(-3500, 1345),(-4700, 1345),(-4700, 1647),(-3500, 1647),(-350, 1800)])
    #myCircuiTrap_layout = myCircuiTrap.Layout(channels_shapes=[None,None,None,None,
    #                                                          new_Shape,None,None])
    myCircuiTrap_layout.visualize(annotate = True)

    #myCircuiTrap_layout.write_gdsii("myCircuiTrapTrapsJune2020.gds")

    #generating STL and OF sim

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
    params["inlets"] = [FixedVelocityInlet(in_port_number=0, velocity=(0.0, 50.0e-3, 0)),
                        #FixedVelocityInlet(in_port_number=1, velocity=(0.0, -30e-3, 0.0)),
                        #FixedVelocityInlet(in_port_number=2, velocity=(0.0, 30e-3, 0.0))
                         ]

    window_si = SizeInfo(west=-260, east=260, south=-360, north=360)
    #params["window_size_info"] = window_si

    # 2D simulation
    params["dimensions"] = 3

    # Create and run simulation

    from ipkiss.plugins.simulation import *

    simul = myCircuiTrap_layout.create_simulation(simul_params=params)

    # Start running simulation

    simul.procedure.run(case_name='block2x4_round', use_existing_mesh=False, interactive=True)
