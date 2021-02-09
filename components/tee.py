from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics

import math


class TeeSimple(i3.PCell):
    """
    Provide a description of this PCell
    """

    channel_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate(),
                                                             doc="Channel template of the tee")
    _name_prefix = "Tee" # a prefix added to the unique identifier

    class Layout(i3.LayoutView):

        tee_length = i3.NumberProperty(default=300.0, doc="length of each tee branch")

        def _generate_instances(self, insts):
            channel1 = microfluidics.Channel(trace_template = self.cell.channel_template)
            channel1_lo = channel1.Layout(shape=[(0, -self.tee_length), (0, self.tee_length)])
            insts += i3.SRef(channel1_lo, position=(0, 0))

            channel2 = microfluidics.Channel(trace_template=self.cell.channel_template)
            channel2_lo = channel2.Layout(shape=[(0, 0), (-self.tee_length, 0)])
            insts += i3.SRef(channel2_lo, position=(self.tee_length, 0))

            return insts

        def _generate_ports(self, ports):
            #port1
            ports += microfluidics.FluidicPort(name='in1',
                                               position = (0, -self.tee_length),
                                               direction = i3.PORT_DIRECTION.IN,
                                               angle_deg=270,
                                               trace_template=self.cell.channel_template
                                               )
            #port2
            ports += microfluidics.FluidicPort(name='in2',
                                               position = (0, self.tee_length),
                                               direction = i3.PORT_DIRECTION.IN,
                                               angle_deg=90,
                                               trace_template=self.cell.channel_template
                                               )
            #port3
            ports += microfluidics.FluidicPort(name='out1',
                                               position = (self.tee_length, 0.0),
                                               direction = i3.PORT_DIRECTION.OUT,
                                               angle_deg=0,
                                               trace_template=self.cell.channel_template
                                               )
            return ports
