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

