# Example: Definition of a PCell with Properties
from microfluidics_ipkiss3.technology import *

from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics

class coverslide(i3.PCell):
        _name_prefix = "COVERSLIDE"  # a prefix added to the unique identifier

        class Layout(i3.LayoutView):
            channel_template = microfluidics.ShortChannelTemplate()
            length = i3.NumberProperty(default=60e3)
            width = i3.NumberProperty(default=20e3)
            cInp = i3.Coord2Property(default=(0.0, 0.0))

            def _generate_elements(self, elems):
                elems += i3.RoundedRectanglePath(layer=i3.TECH.PPLAYER.CH2.TRENCH,
                                                 center = (0.0,0.0),
                                                 box_size = (self.length,self.width),
                                                 radius=200., line_width=2.0)
                return elems

class shime(i3.PCell):
    _name_prefix = "SHIME"  # a prefix added to the unique identifier

    class Layout(i3.LayoutView):
        channel_template = microfluidics.ShortChannelTemplate()
        length = i3.NumberProperty(default=60e3)
        width = i3.NumberProperty(default=20e3)
        perspex_width_shime = i3.NumberProperty(default=2e3)
        cInp = i3.Coord2Property(default=(0.0, 0.0))

        def _generate_elements(self, elems):
            elems += i3.RoundedRectanglePath(layer=i3.TECH.PPLAYER.CH1.TRENCH,
                                             center=(0.0, 0.0),
                                             box_size=(self.length+self.perspex_width_shime, self.width+self.perspex_width_shime),
                                             radius=1000., line_width=self.perspex_width_shime)
            return elems

class wafer(i3.PCell):
    """A generic wafer class.
    It is defined by a circle
    """
    _name_prefix = "WAFER"  # a prefix added to the unique identifier

    class Layout(i3.LayoutView):
        channel_template = microfluidics.ShortChannelTemplate()
        size = i3.NumberProperty(default =10e4)
        cInp = i3.Coord2Property(default=(0.0,0.0))

        def _generate_elements(self, elems):
            elems += i3.CirclePath(layer=i3.TECH.PPLAYER.CH2.TRENCH,
                                        center=(0.0,0.0),
                                        radius=self.size*0.5, line_width = 200)
            return elems

class accessHole(i3.PCell):
    """A generic inlet/outlet hole class.
    It is defined by a circular
    """
    _name_prefix = "ACCESSHOLE"  # a prefix aded to the unique identifier
    diameter = i3.NumberProperty(default =300.)
    class Layout(i3.LayoutView):
        channel_template = microfluidics.ShortChannelTemplate()
        #inlet_diameter = i3.NumberProperty(default =300.)
        cInp = i3.Coord2Property(default=(0.0,0.0))

        def _generate_elements(self, elems):
            #solid
            #circle = i3.ShapeCircle(center=(0.0,0.0), radius=self.inlet_diameter*0.5)
            #elems += i3.Boundary(layer=i3.TECH.PPLAYER.CH2.TRENCH, shape=circle)
            #line (faster on MLA)
            elems += i3.CirclePath(layer=i3.TECH.PPLAYER.CH2.TRENCH,
                                        center=(0.0,0.0),
                                        radius=self.diameter*0.5, line_width = 200)


            return elems

        def _generate_ports(self, ports):
            ports += microfluidics.FluidicPort(name='in', position = (0.0, 0.0),
                                               direction = i3.PORT_DIRECTION.IN,
                                               trace_template=self.channel_template,
                                               angle_deg=90
                                               )

            ports += microfluidics.FluidicPort(name = 'out', position = (0.0, 0.0),
                                               direction = i3.PORT_DIRECTION.OUT,
                                               trace_template=self.channel_template,
                                               angle_deg=90
                                               )

            return ports

class accessHoleFlat(i3.PCell):
    """A generic inlet/outlet hole class.
    It is defined by a circular
    """
    _name_prefix = "ACCESSHOLE_FLAT"  # a prefix aded to the unique identifier

    reduction_ratio =i3.NumberProperty(default=1.0) #transition from BigRes to Trap
    diameter = i3.NumberProperty(default=300.)

    class Layout(i3.LayoutView):
        channel_template = microfluidics.ShortChannelTemplate()
        cInp = i3.Coord2Property(default=(0.0, 0.0))


        def _generate_elements(self, elems):
            elems += i3.CirclePath(layer=i3.TECH.PPLAYER.CH2.TRENCH,
                                   center=(0.0, 0.0),
                                   radius=self.diameter * 0.5, line_width=50)

            point_list = []



            point_list.append((0, -self.diameter * 0.5))
            point_list.insert(0, (0, self.diameter * 0.5))
            point_list.append(( self.diameter*self.cell.reduction_ratio, -self.diameter * 0.5*self.cell.reduction_ratio))
            point_list.insert(0, (self.diameter*self.cell.reduction_ratio, self.diameter * 0.5*self.cell.reduction_ratio))

            funnel = i3.Shape(point_list, closed=True)
            bo = i3.Boundary(i3.TECH.PPLAYER.CH2.TRENCH, funnel)
            elems += bo

            return elems



        def _generate_ports(self, ports):
            '''ports += microfluidics.FluidicPort(name='in', position=(0.0, 0.0),
                                               direction=i3.PORT_DIRECTION.IN,
                                               trace_template=self.channel_template,
                                               angle_deg=0
                                               )'''

            ports += microfluidics.FluidicPort(name='out', position=(self.diameter*self.cell.reduction_ratio, 0.0),
                                               direction=i3.PORT_DIRECTION.OUT,
                                               trace_template=self.channel_template,
                                               angle_deg=180
                                               )

            return ports




class identifierText(i3.PCell):
    """A generic label
    """
    _name_prefix = "LABEL"  # a prefix aded to the unique identifier
    text = i3.StringProperty(default="Identifier Label", doc="The text which will actually be displayed")
    font_size = i3.PositiveNumberProperty(default=1000.0, doc="Font size of the text")

    class Layout(i3.LayoutView):
        channel_template = microfluidics.ShortChannelTemplate()
        cInp = i3.Coord2Property(default=(0.0, 0.0))

        def _generate_elements(self, elems):
            elems += i3.PolygonText(layer=i3.TECH.PPLAYER.CH2.TRENCH,
                      coordinate=(0.,0.),
                        text=self.text,
                        height=self.font_size)
            return elems

class pinsRectangleFour(i3.PCell):
    """A generic inlet/outlet hole class.
    It is defined by a circular
    """
    _name_prefix = "PINS"  # a prefix aded to the unique identifier
    diameter = i3.NumberProperty(default =1000.)
    class Layout(i3.LayoutView):
        channel_template = microfluidics.ShortChannelTemplate()
        #inlet_diameter = i3.NumberProperty(default =300.)
        cInp = i3.Coord2Property(default=(0.0,0.0))

        def _generate_elements(self, elems):
            #solid
            #circle = i3.ShapeCircle(center=(0.0,0.0), radius=self.inlet_diameter*0.5)
            #elems += i3.Boundary(layer=i3.TECH.PPLAYER.CH2.TRENCH, shape=circle)
            #line (faster on MLA)
            elems += i3.CirclePath(layer=i3.TECH.PPLAYER.CH1.TRENCH,
                                        center=(26e3,9e3),
                                        radius=self.diameter*0.5, line_width = 200)
            elems += i3.CirclePath(layer=i3.TECH.PPLAYER.CH1.TRENCH,
                                   center=(-26e3, 9e3),
                                   radius=self.diameter * 0.5, line_width=200)

            elems += i3.CirclePath(layer=i3.TECH.PPLAYER.CH1.TRENCH,
                                   center=(-26e3, -9e3),
                                   radius=self.diameter * 0.5, line_width=200)

            elems += i3.CirclePath(layer=i3.TECH.PPLAYER.CH1.TRENCH,
                                   center=(26e3, -9e3),
                                   radius=self.diameter * 0.5, line_width=200)
            return elems


if __name__ == "__main__":
    print "This is not the main file. Run 'execute.py' in the same folder"


    inlet_hole = accessHoleFlat()
    inlet_hole_layout= inlet_hole.Layout(diameter=100.0)
    inlet_hole_layout.visualize(annotate = True)


    inlet_hole = accessHole()
    inlet_hole_layout= inlet_hole.Layout(diameter = 100.0)
    inlet_hole_layout.visualize(annotate = True)
    '''
    myCoverslide = coverslide()
    myCoverslide_layout = myCoverslide.Layout()
    myCoverslide_layout.visualize()

    myWafer = wafer()
    myWafer_layout = myWafer.Layout()
    myWafer_layout.visualize()'''

    myShime = shime()
    myShime_layout = myShime.Layout()
    myShime_layout.visualize()
    '''
    myText = identifierText()
    myText_layout = myText.Layout()
    myText_layout.visualize()

    myPins = pinsRectangleFour()
    myPins_layout = myPins.Layout()
    myPins_layout.visualize()'''