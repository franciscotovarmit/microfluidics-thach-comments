# Import the Microfluidic Technology File.

from microfluidics_ipkiss3.technology import *

# Import IPKISS3 Packages.

from ipkiss3 import all as i3

# Import microfluidics API.

import microfluidics_ipkiss3.all as microfluidics

# Define a Custom Class.
class Obstacle_BooleanBoundary(i3.PCell):

    layer = i3.LayerProperty(default=i3.TECH.PPLAYER.CH1.TRENCH, doc='Layer to drawn on')
    # Properties of trap
    channel_trap_width = i3.PositiveNumberProperty(default=50., doc="width of trap")
    obstacle_trap_width = i3.PositiveNumberProperty(default=25., doc="width of obstacle")
    obstacle_trap_length = i3.PositiveNumberProperty(default=30., doc="length of trap")
    gap_btw_barriers = i3.PositiveNumberProperty(default=20., doc="gap between obstacles")
    cInp = i3.Coord2Property(default = (0.0,0.0),required = True)

    class Layout(i3.LayoutView):
        def _generate_instances(self, insts):
            # First create shapes
            # Break the channel that contain two obstacles into three segments
            # Obstacles need to intersect these three segments
            #  Obs 1. Segment 1:2,   Obs 2 Segment 2:3
            #define points will be helpful to make schematic
            p1 = (self.cInp.x+0.0,self.cInp.y+0.0)
            p2 = ((self.gap_btw_barriers+self.obstacle_trap_length)*0.5,0.0)
            p3 = ((self.gap_btw_barriers+self.obstacle_trap_length)*0.5,self.channel_trap_width)
            p4 = (0.0,self.channel_trap_width)
            p5 = ((self.gap_btw_barriers+self.obstacle_trap_length)*1.5, 0.0)
            p6 = ((self.gap_btw_barriers+self.obstacle_trap_length)*2, 0.0)
            p7 = ((self.gap_btw_barriers+self.obstacle_trap_length)*2, self.channel_trap_width)
            p8 = ((self.gap_btw_barriers+self.obstacle_trap_length)*1.5,self.channel_trap_width)

            sr1 = i3.Shape(points = [p1,p2,p3,p4], closed =True)
            sr2 = i3.Shape(points = [p2,p5,p8,p3], closed =True)
            sr3 = i3.Shape(points = [p5,p6,p7,p8], closed =True)

            #Internal holes as Circles  #It is needed to define position of SC2 as a function of perpendicular GAP
            #sc1 = i3.ShapeCircle(center = (self.cInp.x+(self.gap_btw_barriers+self.obstacle_trap_length)*0.65, 0.0), radius = (self.obstacle_trap_width))
            #sc2 = i3.ShapeCircle(center = (self.cInp.x+(self.gap_btw_barriers+self.obstacle_trap_length)*1.35,self.cInp.y+self.channel_trap_width), radius = (self.obstacle_trap_width))

            #Internal holes as Rectangles
            sc1 = i3.ShapeRectangle(center = (self.cInp.x+(self.gap_btw_barriers
                                                           +self.obstacle_trap_length)*0.5,
                                              self.cInp.y+self.obstacle_trap_width*0.5),
                                    box_size = (self.obstacle_trap_length,
                                                self.obstacle_trap_width))
            sc2 = i3.ShapeRectangle(center = (self.cInp.x+(self.gap_btw_barriers
                                                           +self.obstacle_trap_length)*1.5,
                                              self.cInp.y+self.channel_trap_width-self.obstacle_trap_width*0.5),
                                    box_size = (self.obstacle_trap_length,
                                                self.obstacle_trap_width))

            #Define the boundaries for shapes
            br1 = i3.Boundary(layer = self.layer, shape = sr1)
            br2 = i3.Boundary(layer = self.layer, shape = sr2)
            br3 = i3.Boundary(layer = self.layer, shape = sr3)

            bc1 = i3.Boundary(layer = self.layer, shape = sc1)
            bc2 = i3.Boundary(layer = self.layer, shape = sc2)

            #Substruct boundaries and add to the element list
            b_sub = br1-bc1

            s= i3.Structure(elements = b_sub)
            insts += i3.SRef(s)

            b_sub = br2-bc1
            b_sub = b_sub[0] - bc2

            s= i3.Structure(elements = b_sub)
            insts += i3.SRef(s)

            b_sub = br3-bc2

            s= i3.Structure(elements = b_sub)
            insts += i3.SRef(s)

            return insts

        #Thach added to define one inlet and one outlet
        def _generate_ports(self, ports):  # Use _generate_ports method to define ports
            #ports += i3.InFluidicPort(name = "in", position = (0., 10.), angle = 180.0)
            ports += i3.OpticalPort(name = "in", position = (0., self.channel_trap_width*0.5), angle = 180.0)
            #ports += i3.OutFluidicPort(name ="out", position = (30., 10.), angle = 0.0)
            ports += i3.OpticalPort(name ="out", position = ((self.obstacle_trap_length+self.gap_btw_barriers)*2, self.channel_trap_width*0.5), angle = 0.0)

            return ports

# Main program
if __name__ == "__main__":
    trap = Obstacle_BooleanBoundary(channel_trap_width = 50.0,
                                   obstacle_trap_width = 10.0,
                                   obstacle_trap_length = 30.0,
                                   gap_btw_barriers = 20.0,
                                   cInp = (0.0,0.0))
    trap_layout = trap.Layout()
    trap_layout.visualize(annotate=True)
    trap_layout.visualize_2d()
    # visualize_2d displays a top down view of the fabricated layout
    #trap_layout.cross_section(i3.Shape([(0, 25), (100, 25)]), process_flow=TECH.VFABRICATION.PROCESS_FLOW).visualize()
    #lay.cross_section(i3.Shape([(-9, 3), (9, 3)]), process_flow=vfab_flow).visualize()
    trap_layout.write_gdsii("erik_trapI3.gds")

