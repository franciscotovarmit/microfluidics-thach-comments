#from microfluidics_ipkiss3.technology import * #comment when running main script, uncomment to debug geometry
from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics

from trap import CellTrapSimple, CellTrapRounded
from tee import TeeSimple

# PCell containing two tees
class TrapWithTees(i3.PCell):
    """Parametric cell with trap and tee defined by the user
    """
    _name_prefix = "TRAP_W_TEES"

    # 1.
    # The trap and tee are defined as ChildCellProperties. This is a special property
    # that for hierarchical PCells. In each view of the PCell of a certain type (e.g. Layout)
    # the corresponding viewtype (e.g. Layout) of the ChildCell will automatically available.

    trap = i3.ChildCellProperty(default=CellTrapSimple())
    tee = i3.ChildCellProperty(default=TeeSimple())
    TECH = i3.get_technology()

    # Layout view
    class Layout(i3.LayoutView):

        def _generate_instances(self, insts):
            insts += i3.place_insts(
                insts={
                    'inlet': self.tee,
                    'trap': self.trap,
                    'outlet': self.tee
                },
                specs=[
                    i3.Place('trap', (0, 0)),
                    i3.Join([
                        ('inlet:out1', 'trap:in1'),
                        ('outlet:out1', 'trap:out1')
                    ]),
                    i3.FlipH('outlet'),
                    ]
                )
            return insts

        def _generate_ports(self, ports):
            return i3.expose_ports(self.instances,
                                   {'inlet:in1': 'in1',
                                    'inlet:in2': 'in2',
                                    'outlet:in1': 'out1',
                                    'outlet:in2': 'out2'
                                    })

