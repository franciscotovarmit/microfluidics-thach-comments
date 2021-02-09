from technologies import silicon_photonics
from microfluidics_ipkiss3.technology import *

from cell import AlignmentMark
s = AlignmentMark()   # Create New Fluidic_Circuit object.
s_layout = s.Layout()   # Define the Layout for the Fluidic_Circuit object.
s_layout.visualize()         # Visualise the Fluidic_Circuit object in 2D.
s_layout.visualize_2d()