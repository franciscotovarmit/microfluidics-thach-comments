
from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics

import math

class CellTrapSimple(i3.PCell):
    """
    Provide a description of this PCell
    """
    _name_prefix = "CELLTRAP" # a prefix added to the unique identifier
    channel_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate(), doc="Channel template")

    class Layout(i3.LayoutView):
        cell_trap_length = i3.PositiveNumberProperty(default = 300.0, doc="total length")
        cell_trap_gap = i3.NumberProperty(default = 10.0, doc="trap gap")
        cell_trap_gap_length = i3.NumberProperty(default = 60.0, doc="length of trap section")
        in_angle = i3.NumberProperty(default= 85, doc="internal entry angle of the trap ")
        out_angle = i3.NumberProperty(default =85, doc="internal exit angle of the trap ")
        radius_fillet = i3.NumberProperty(default =3, doc="radius for rounding internal edges/corners")

        '''
        ----------------------------\           /--------------
                        in angle     \         /  outangle
                                      \       /
                                       |_____|        
                                       
                                        _____
                                       |     |
                                      /       \
                        in angle     /         \outangle
        ____________________________/           \------------------  
        '''

        def _generate_elements(self, elems):

            cell_trap_width = self.channel_template.channel_width

            alpha = math.radians(self.in_angle)
            beta = math.radians(self.out_angle)

            point_list = []

            point_list.append( (-self.cell_trap_length*0.25, -cell_trap_width*0.5))
            point_list.insert(0,  (-self.cell_trap_length*0.25, cell_trap_width*0.5))

            point_list.append( (-(cell_trap_width-self.cell_trap_gap)/math.tan(alpha)-self.cell_trap_gap_length*0.5,-(cell_trap_width*0.5)))
            point_list.insert(0, (-(cell_trap_width-self.cell_trap_gap)/math.tan(alpha)-self.cell_trap_gap_length*0.5,(cell_trap_width*0.5)))

            point_list.append( (-self.cell_trap_gap_length*0.25,-self.cell_trap_gap*0.5 ))  # end of array
            point_list.insert(0,  (-self.cell_trap_gap_length*0.25,self.cell_trap_gap*0.5 ))  # begging of array, position 0

            point_list.append( (self.cell_trap_gap_length*0.25,-self.cell_trap_gap*0.5 ))
            point_list.insert(0, (self.cell_trap_gap_length*0.25,self.cell_trap_gap*0.5 ))

            point_list.append( ((cell_trap_width-self.cell_trap_gap)/math.tan(beta)+self.cell_trap_gap_length*0.25,-(cell_trap_width*0.5)))
            point_list.insert(0, ((cell_trap_width-self.cell_trap_gap)/math.tan(beta)+self.cell_trap_gap_length*0.25,(cell_trap_width*0.5)))

            point_list.append( (-self.cell_trap_length*0.25+self.cell_trap_length*0.5,-cell_trap_width*0.5))
            point_list.insert(0, (-self.cell_trap_length*0.25+self.cell_trap_length*0.5,cell_trap_width*0.5))

            t = i3.Shape(point_list, closed=True)

            rectang = i3.ShapeRound(original_shape=t, start_face_angle=0, end_face_angle=0, radius=self.radius_fillet)
            bo = i3.Boundary(self.channel_template.layer, rectang)
            #insts += bo  #comm/uncomm for debugging round stl

            #creating an inlet rectangle boundary to avoid round corners
            point_list = []
            #w = 3
            point_list.append((-self.cell_trap_length * 0.5, -cell_trap_width * 0.5))
            point_list.insert(0, (-self.cell_trap_length * 0.5, cell_trap_width * 0.5))

            point_list.append((-self.cell_trap_length * 0.25 + self.radius_fillet, -cell_trap_width * 0.5))
            point_list.insert(0, (-self.cell_trap_length * 0.25 + self.radius_fillet, cell_trap_width * 0.5))

            t = i3.Shape(point_list, closed=True)
            bo1 = i3.Boundary(self.channel_template.layer, t)

            #creating an outlet rectangle boundary to avoid round corners
            point_list = []
            point_list.append((self.cell_trap_length*0.25-self.radius_fillet, -cell_trap_width * 0.5))
            point_list.insert(0, (self.cell_trap_length*0.25-self.radius_fillet, cell_trap_width * 0.5))

            point_list.append((self.cell_trap_length*0.5, -cell_trap_width * 0.5))
            point_list.insert(0, (-self.cell_trap_length * 0.5 + self.cell_trap_length, cell_trap_width * 0.5))

            t = i3.Shape(point_list, closed=True)
            bo2 = i3.Boundary(self.channel_template.layer, t)



            #boolean operation adding main geometry and inlet rectangle
            b_add =  bo1 | bo

            #boolean operation adding main geometry and outlet rectangle
            b_add2 = bo2 | b_add[0]
            elems += b_add2
            return elems

        def _generate_ports(self, ports):

            #port1
            ports += microfluidics.FluidicPort(name='in1', position = (-self.cell_trap_length*0.5, 0.0),
                                               direction = i3.PORT_DIRECTION.IN,
                                               angle_deg=180,
                                               trace_template=self.channel_template
                                               )

            ports += microfluidics.FluidicPort(name='out1', position = (self.cell_trap_length*0.5, 0.0),
                                               direction = i3.PORT_DIRECTION.IN,
                                               angle_deg=0,
                                               trace_template=self.channel_template
                                               )

            return ports



class CellTrapRounded(CellTrapSimple):
    """
    Provide a decription of this PCell
    What is the difference between this and CellTrapSimple?
    """

    _name_prefix = "CELLTRAP_ROUNDED" # a prefix added to the unique identifier
    cInp = i3.Coord2Property(default= (0.0,0.0), doc="Center of trap, reference point needed to define rounded corner")

    class Layout(CellTrapSimple.Layout):
        '''
        ----------------------------\           /--------------
                        in angle     \         /  outangle
                                      \       /
                                       |_____|

                         |-funnel length-| _____
                                         .     .
                                        .       .
                                      .           .
                                    .               .
                                 .                    .
        _____________________.                          .__________
                ###UNDER CONSTRUCTION

        '''

        funnel_length = i3.NumberProperty(default = 100.0, doc="Francisoc: What is this?")

        def _generate_elements(self, elems):
            cell_trap_width = self.channel_template.channel_width
            entry_Lfd = self.cell_trap_length * 0.5  # 1000.0
            exit_Lfd = self.cell_trap_length * 0.5  # 500.0
            beta = math.radians(self.out_angle)

            lf = self.funnel_length
            wi = cell_trap_width
            wf = self.cell_trap_gap
            #lfd = 0

            taper_samples = 200
            a = lf / (wi / wf - 1.0)

            dx = lf / taper_samples
            x = 0.0
            xl = []
            wl = []

            point_list = []
            x_offset = self.funnel_length + self.cell_trap_gap_length # all expansion will be at 0.0x
            a = 0.5
            b = .35
            point_list.append(self.cInp + (-(self.cell_trap_length * b), wi * 0.5))  # end of array
            point_list.insert(0, self.cInp + (-(self.cell_trap_length * b), -wi * 0.5))  # begging of array, position 0

            for i in reversed(range(1, taper_samples + 1)):
                #xa = lf * math.exp(10.0 * (i / taper_samples - 1.0))  #discretization
                radius =0.5*wi   ### this needs to be improved
                xa = (radius)*math.cos(0.5*math.pi*i/taper_samples)
                #w = wi / (1.0 + xa / a)    #function value
                w = (radius)*math.sin(0.5*math.pi*i/taper_samples)
                p = (xa - radius-self.cell_trap_gap_length*0.5, 0.5*(w+0.5*wi))
                point_list.append(self.cInp + p)
                p = (xa - radius-self.cell_trap_gap_length*0.5, -0.5*(w+0.5*wi))
                point_list.insert(0, self.cInp + p)


            # GAP LENGTH
            p = (point_list[-1][0], wf*0.5) #wGet last point, coordX use it for next point with wf as coordY
            point_list.append(self.cInp + p)  # Insert it at the bottom of point_list
            p = point_list[-1] + (0.0, (-wf))  # Get last point, add -wf
            point_list.insert(0,self.cInp + p)  # Insert it at the bottom of point_list

            p = point_list[-1] + (self.cell_trap_gap_length, 0.0)  # Get last point and add length
            point_list.append(self.cInp + p)  # Insert it at [0] in the point_list

            p = point_list[-1] + (0.0, -wf)  # Get last point and add length
            point_list.insert(0, self.cInp + p)  # Insert it at [0] in the point_list

            # EXIT ANGLE
            p = point_list[-1] + (0.5 * (cell_trap_width - self.cell_trap_gap) / math.tan(beta),
                                  -cell_trap_width * 0.5 - wf * .50)  # Get last point and add length of angle
            point_list.insert(0, self.cInp + p)  # Insert it at [0] in the point_list

            p = point_list[0] + (0, wi)
            point_list.append(self.cInp + p)  # Insert it at the bottom of point_list

            # EXIT LENGTH
            p = (self.cell_trap_length*b,point_list[-1][1])  # get first point (last point added) and add length
            point_list.append(self.cInp + p)

            p = point_list[-1] + (0, -wi)  ##get last point and add length
            point_list.insert(0, self.cInp + p)

            t = i3.Shape(point_list, closed=True)

            rectang = i3.ShapeRound(original_shape=t, start_face_angle=0, end_face_angle=0, radius=self.radius_fillet)
            bo = i3.Boundary(self.channel_template.layer, rectang)

            #creating an inlet rectangle boundary to avoid round corners
            point_list = []
            point_list.append((-self.cell_trap_length * a, -cell_trap_width * 0.5))
            point_list.insert(0, (-self.cell_trap_length * a, cell_trap_width * 0.5))

            point_list.append((-self.cell_trap_length * b +self.radius_fillet, -cell_trap_width * 0.5))
            point_list.insert(0, (-self.cell_trap_length * b +self.radius_fillet, cell_trap_width * 0.5))

            t = i3.Shape(point_list, closed=True)
            bo1 = i3.Boundary(self.channel_template.layer, t)

            #creating an outlet rectangle boundary to avoid round corners
            point_list = []
            point_list.append((self.cell_trap_length*b -self.radius_fillet, -cell_trap_width * 0.5))
            point_list.insert(0, (self.cell_trap_length*b -self.radius_fillet, cell_trap_width * 0.5))

            point_list.append((self.cell_trap_length*a, -cell_trap_width * 0.5))
            point_list.insert(0, (self.cell_trap_length*a, cell_trap_width * 0.5))

            t = i3.Shape(point_list, closed=True)
            bo2 = i3.Boundary(self.channel_template.layer, t)

            #boolean operation adding main geometry and inlet rectangle
            b_add =  bo | bo1

            #boolean operation adding main geometry and outlet rectangle
            b_add2 = b_add[0] | bo2
            #s2 = i3.Structure(elements=b_add2)
            elems += b_add2
            #insts += bo
            return elems

        def _generate_ports(self, ports):

            #port1
            ports += microfluidics.FluidicPort(name='in1', position = (-self.cell_trap_length*0.5, 0.0),
                                               direction = i3.PORT_DIRECTION.IN,
                                               #angle_deg=0,
                                               trace_template=self.channel_template
                                               )

            ports += microfluidics.FluidicPort(name='out1', position = (self.cell_trap_length*0.5, 0.0),
                                               direction = i3.PORT_DIRECTION.IN,
                                               #angle_deg=0,
                                               trace_template=self.channel_template
                                               )

            return ports

