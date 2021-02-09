
#####
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


from microfluidics_ipkiss3.technology import * #comment when running main script, uncomment to debug geometry

from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics

from vacuum import Vacuum_BooleanBoundary

TECH = i3.get_technology()
trap = Vacuum_BooleanBoundary()
#trap = CellTrapRounded()
trap_layout= trap.Layout()
trap_layout.visualize(annotate = True)
trap_layout.visualize_2d()


