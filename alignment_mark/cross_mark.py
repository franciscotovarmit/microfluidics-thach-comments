
"""

PCell for Alignment markers

Author: Phuong Tang; modified by Markus Knoerzer, Thach Nguyen

"""


from ipkiss3 import all as i3

class CrossMark(i3.PCell):
    """
    Definition class for Cross Marker
    """

    _name_prefix = "CROSS_MARK" 

    class Layout(i3.LayoutView):
        """
        Cross marker Layout view
        """

        inversion = i3.BoolProperty(default=False, doc="if True: open cross - white cross on black background")
        cross_bar_width = i3.PositiveNumberProperty(default=8, doc="width of the cross")
        cross_boundary_width = i3.PositiveNumberProperty(default=50, doc="width the boundary box")
        #process = i3.ProcessProperty(default=i3.TECH.PPLAYER.CH2.TRENCH)#i3.TECH.PROCESS.WG, doc="Process Layer on which the cross is drawn")
    
        # Purpose Property cannot be set from outside
        #purpose = i3.PurposeProperty(locked=True, default=i3.TECH.PPLAYER.CH2.TRENCH)#i3.TECH.PURPOSE.DF.LINE, doc="Process Purpose of the cross")

        def _generate_elements(self, elems):

            rect_size = (self.cross_boundary_width - self.cross_bar_width)/2
            rect_center = self.cross_bar_width/2 + rect_size/2

            if not self.inversion:  # Dark cross
                elems += i3.Cross(layer=i3.TECH.PPLAYER.CH1.TRENCH,#i3.PPLayer(self.process,self.purpose),
                                  center=(0, 0),
                                  box_size=self.cross_boundary_width,
                                  thickness=self.cross_bar_width)

            else:  # Open cross: formed by 4 dark squares at corners
                elems += i3.Rectangle(layer=i3.TECH.PPLAYER.CH2.TRENCH,#i3.PPLayer(self.process, self.purpose),
                                      center=(rect_center, rect_center),
                                      box_size=(rect_size, rect_size))
                elems += i3.Rectangle(layer=i3.TECH.PPLAYER.CH2.TRENCH,#i3.PPLayer(self.process, self.purpose),
                                      center=(rect_center, - rect_center),
                                      box_size=(rect_size, rect_size))
                elems += i3.Rectangle(layer=i3.TECH.PPLAYER.CH2.TRENCH,#i3.PPLayer(self.process, self.purpose),
                                      center=(- rect_center, rect_center),
                                      box_size=(rect_size, rect_size))
                elems += i3.Rectangle(layer=i3.TECH.PPLAYER.CH2.TRENCH,#i3.PPLayer(self.process, self.purpose),
                                      center=(- rect_center, - rect_center),
                                      box_size=(rect_size, rect_size))
            return elems