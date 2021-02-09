# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 16:01:10 2018
@author: francisco
"""

# Import the Microfluidic Technology File.
from microfluidics_ipkiss3.technology import *
# Import IPKISS3 Packages.
from ipkiss3 import all as i3
# Import microfluidics API.
import microfluidics_ipkiss3.all as microfluidics
from debri_trap_single import Obstacle_BooleanBoundary

class JoinedObstacles(i3.PCell):#(Structure):
    channel_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate(), doc="Channel template for ports")

    mysingleObstacle = i3.ChildCellProperty(doc='the single Obstacle child cell, which will be clonned many times',
                                            default=Obstacle_BooleanBoundary())
    wholeTrapX = i3.PositiveNumberProperty(default=500.0, doc="total X distance length of traps")
    wholeTrapY = i3.PositiveNumberProperty(default=500.0, doc="total Y distance length of traps")
    cInp = i3.Coord2Property(default=0.0, doc="")

    class Layout(i3.LayoutView):

        def _generate_instances(self, insts):
            x_inc = (self.mysingleObstacle.gap_btw_barriers+self.mysingleObstacle.obstacle_trap_length)*2
            y_inc = self.mysingleObstacle.channel_trap_width*1.5

            cycles_x = int(self.wholeTrapX/((self.mysingleObstacle.gap_btw_barriers +
                                             self.mysingleObstacle.obstacle_trap_length)*2))
            cycles_y = int(self.wholeTrapY/(y_inc))

            insts += i3.ARef(reference=self.mysingleObstacle, origin=(0,0.0*self.cell.wholeTrapY),
                             period=(x_inc, y_inc),
                             n_o_periods=(cycles_x, cycles_y))

            print 'insts',insts


            return insts

        def _generate_ports(self, ports):
            #port1
            ports += microfluidics.FluidicPort(name='in',
                                               position = (0, self.wholeTrapY*0.5),
                                               #position = (0, 'insts_0'.size_info().north*0.5),
                                               direction = i3.PORT_DIRECTION.IN,
                                               angle_deg=180,
                                               trace_template=self.cell.channel_template
                                               )
            #port2
            ports += microfluidics.FluidicPort(name='out',
                                               position = (self.wholeTrapX,self.wholeTrapY*0.5),
                                               direction = i3.PORT_DIRECTION.OUT,
                                               angle_deg=0,
                                               trace_template=self.cell.channel_template
                                               )

            return ports

# Main program
if __name__ == '__main__':
    singleObstacle = Obstacle_BooleanBoundary(channel_trap_width=50.0,
                                 obstacle_trap_width=25.0,
                                 obstacle_trap_length=30.0,
                                 gap_btw_barriers=20.0,
                                 cInp=(0.0, 0.0))
    singleObstacle_Layout =  singleObstacle.Layout()
    #singleObstacle_Layout.visualize()
    multipleObstacle = JoinedObstacles(wholeTrapX= 500,#2000,
                                       wholeTrapY=500,#2500,
                                       mysingleObstacle=singleObstacle)
    multipleObstacle_Layout = multipleObstacle.Layout()
    multipleObstacle_Layout.visualize(annotate = True)
    multipleObstacle_Layout.write_gdsii("Trapi3All.gds")
