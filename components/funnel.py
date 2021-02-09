# Example: Definition of a PCell with Properties
from microfluidics_ipkiss3.technology import *

from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics

import math
# Get the technology
# We will define a TrapellTrapLength which consists of
# a geometry with a microcontracion

class Funnel(i3.PCell):
    """A generic Funnel to connect elements. It is defined by a boundary which are defined by points
    """
    # 1. First we define our 2 Channel Templates with different Width's.
    channel_1_template = microfluidics.ShortChannelTemplate()
    channel_2_template = microfluidics.ShortChannelTemplate()

    # 2. Then we use the LinearWindowChannelTransition class to create a transition between Channels.

    #####################3
    ###################

    channel_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate(), doc="Channel template of the tee")
    _name_prefix = "Funnel" # a prefix added to the unique
    funnel_length = i3.NumberProperty(default=100.0, doc="length of funnel")
    initial_width = i3.NumberProperty(default=200.0, doc="initial with of funnel")
    final_width = i3.NumberProperty(default=100.0, doc="final width of funnel")

    class Layout(i3.LayoutView):


        def _generate_instances(self, insts):
            channel_1_template= self.cell.channel_1_template.Layout(channel_width = self.cell.initial_width)
            channel_2_template = self.cell.channel_2_template.Layout(channel_width = self.cell.final_width)

            funnel = microfluidics.LinearWindowChannelTransition(start_trace_template = self.cell.channel_1_template,
                                                                    end_trace_template = self.cell.channel_2_template)

            funnel_layout = funnel.Layout(start_position=(0.0, 0.0), end_position=(self.cell.funnel_length, 0.0))
            insts += i3.SRef(reference = funnel_layout, name='funnel', position=(0,0))
            return insts

        def _generate_ports(self, ports):
            #port1
            ports += microfluidics.FluidicPort(name='in',
                                               position = (0,0),
                                               direction = i3.PORT_DIRECTION.IN,
                                               angle_deg=180,
                                               trace_template=self.cell.channel_template
                                               )
            #port2
            ports += microfluidics.FluidicPort(name='out',
                                               position = (self.funnel_length,0),
                                               direction = i3.PORT_DIRECTION.OUT,
                                               angle_deg=0,
                                               trace_template=self.cell.channel_template
                                               )

            return ports

if __name__ == "__main__":
    print "This is not the main file. Run 'execute.py' in the same folder"
    myFunnel = Funnel()
    myFunnel_layout= myFunnel.Layout(funnel_length=100)
    myFunnel_layout.visualize(annotate = True)
    myFunnel_layout.visualize_2d()
