
from microfluidics_ipkiss3.technology import *
from circuits_using_components.block_with_vacuum import Block_with_Vacuum
from components.vacuum import Vacuum_BooleanBoundary
from components.trap_with_tees import TrapWithTees


block = TrapWithTees() # BlockWithTees()
block_layout = block.Layout()#(inlet_diameter=4e3)
circuitWidth = block_layout.size_info()

vacuum = Vacuum_BooleanBoundary(feature_width = circuitWidth.east-circuitWidth.west,
                                feature_height = circuitWidth.north-circuitWidth.south,
                                gap_horiz =50,
                                gap_vertical =50,
                                vacuum_width = 100)
vacuum_layout = vacuum.Layout()

Block_with_Vacuum = Block_with_Vacuum(name = "Block_with_Vacuum",
                      block=block, vacuum = vacuum)
Block_with_Vacuum_layout = Block_with_Vacuum.Layout()
Block_with_Vacuum_layout.visualize(annotate = True)
Block_with_Vacuum_layout.write_gdsii("vacuum_channel.gds")

