
from microfluidics_ipkiss3.technology import *
from circuits_using_components.block_with_vacuum import Vacuum_BooleanBoundary

trap = Vacuum_BooleanBoundary(feature_width = 50.0,
                              feature_height = 10.0,
                              gap_horiz = 30.0,
                              gap_vertical = 20.0,
                              vacuum_width = 50.0,
                              cInp = (0.0,0.0))
trap_layout = trap.Layout()
trap_layout.visualize(annotate=True)
trap_layout.visualize_2d()
trap_layout.write_gdsii("vacuum.gds")

