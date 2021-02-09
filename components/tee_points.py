from microfluidics_ipkiss3.technology import * #comment when running main script, uncomment to debug geometry
from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics


# This script contains two classes.
# Class 1:  TeeSimple: overlapping geometries
# Class 2: TeeBoolean: adding geometries with boolean operation

class TeeSimple(i3.PCell):
    """A generic Tee to connect elements. It is defined by a boundary which are defined by points
    """
    channel_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate(), doc="Channel template of the tee")
    _name_prefix = "Tee" # a prefix added to the unique identifier
    TECH = i3.get_technology()

    class Layout(i3.LayoutView):

        tee_length = i3.NumberProperty(default=10.0, doc="length of each tee branch")

        def _generate_instances(self, elems):# insts):
            channel1 = microfluidics.Channel(trace_template = self.cell.channel_template)
            channel1_lo = channel1.Layout(shape=i3.Shape([(0, -self.tee_length), (0, self.tee_length)]))
            elems += i3.SRef(channel1, position=(0, 0))

            channel2 = microfluidics.Channel(trace_template=self.cell.channel_template)
            channel2_lo = channel2.Layout(shape=[(0, 0), (-self.tee_length, 0)])
            elems += i3.SRef(channel2, position=(self.tee_length, 0))

            return elems #insts

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
                                               direction = i3.PORT_DIRECTION.IN,
                                               angle_deg=0,
                                               trace_template=self.cell.channel_template
                                               )
            return ports





class TeeBoolean(i3.PCell):
    """A generic Tee to connect elements. It is defined by a boundary which are defined by points
    """
    channel_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate(), doc="Channel template of the tee")
    _name_prefix = "Tee" # a prefix added to the unique identifier

    class Layout(i3.LayoutView):
        tee_length = i3.NumberProperty(default=10.0, doc="length of each tee branch")

        def _generate_instances(self, elems):# insts):
            rectangle = i3.RoundedRectangle(layer=i3.TECH.PPLAYER.CH2.TRENCH, center=(0.0, 0.0), box_size=(self.tee_length,2*self.tee_length), radius=1.0)
            rectangle2 = i3.RoundedRectangle(layer=i3.TECH.PPLAYER.CH2.TRENCH, center=(0.5*self.tee_length, 0.0), box_size=(self.tee_length,self.tee_length), radius=1.0)
            #boolean operation add main trap and 1st rectangle
            b_add =  rectangle  | rectangle2
            s= i3.Structure(elements = b_add)
            elems += i3.SRef(s)

            return elems #insts

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
                                               direction = i3.PORT_DIRECTION.IN,
                                               angle_deg=0,
                                               trace_template=self.cell.channel_template
                                               )
            return ports
