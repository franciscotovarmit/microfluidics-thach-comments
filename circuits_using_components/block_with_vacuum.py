from microfluidics_ipkiss3.technology import * #comment when running main script, uncomment to debug geometry
from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics

from components.block_with_tees import BlockWithTees
from components.trap_with_tees import TrapWithTees
from components.vacuum import Vacuum_BooleanBoundary

# PCell containing several traps
class Block_with_Vacuum(i3.PCell):

    """Parametric cell with several traps, which are stacked vertically
    """
    _name_prefix = "BlockWithVacuum"
    block = i3.ChildCellProperty()  #  Generating block from Child Cell List Property
    #channel_template = i3.TraceTemplateProperty(doc="the trace template prop")
    vacuum = i3.ChildCellProperty()   #vacuum channel

    class Layout(i3.LayoutView):

        def _get_components(self):
            # 1. calculate the transformations of the rings based on their properties
            circuitWidth = block_layout.size_info()

            circuit_x_gap = 2000.0
            separation = abs(circuitWidth.west) + abs(circuitWidth.east)+ circuit_x_gap

            t1 = i3.Translation((separation*0, 0.0))
            t2 = i3.Translation((separation*1, 0.0))

            # 2. Generating the instances

            circuit_1= i3.SRef(name="t_1", reference=self.block, transformation=t1)
            circuit_2= i3.SRef(name="t_2", reference=self.vacuum, transformation=t1)
            return circuit_1, circuit_2

        def _generate_instances(self, insts):
            insts += self._get_components()
            return insts

if __name__ == "__main__":
    print "This is not the main file. Run 'execute.py' in the same folder"
    block = TrapWithTees() # BlockWithTees()
    block_layout= block.Layout()#(inlet_diameter=4e3)

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

