
"""

PCell for Alignment markers

Author: Phuong Tang; modified by Markus Knoerzer, Thach Nguyen

"""


from ipkiss3 import all as i3

class VernierScale(i3.PCell):
    """
    Definition class for Venier scales
    """
    
    _name_prefix = "VERNIER_SCALE" 
    
    class Layout(i3.LayoutView):
        """
        This section is to draw a Vernier scale
        """

        # Basic properties of the scale
        spacing = i3.PositiveNumberProperty(default=4, doc="spacing between bars")
        number_of_bars = i3.IntProperty(default=13, doc="the number of bars")
        # Detailed properties of the scale
        bar_length = i3.PositiveNumberProperty(default=10, doc="length of the shortest bars on the scale")
        bar_extra_length = i3.PositiveNumberProperty(default=10, doc="extra length of the central bar")
        bar_width = i3.PositiveNumberProperty(default=2, doc="width of a single bar")
        process = i3.ProcessProperty(default=i3.TECH.PPLAYER.CH2.TRENCH) #i3.TECH.PROCESS.WG, doc="Process Layer on which the cross is drawn")
    
        # Purpose property cannot be set from outside
        purpose = i3.PurposeProperty(locked=True, default=i3.TECH.PPLAYER.CH2.TRENCH)#i3.TECH.PURPOSE.DF.LINE, doc="Process Purpose of the cross")
    
        def validate_properties(self):
            # The scale is symmetric with respect to its central bar so the number of bars is an odd number
            if self.number_of_bars%2 == 0:
                raise i3.PropertyValidationError(self, "The number of bars should be an odd number",
                                                 {"number_of_bars": self.number_of_bars})
            return True
    
        def _generate_elements(self, elems):

            # Draw the central bar, which is longer than the others
            elems += i3.Rectangle(layer=i3.TECH.PPLAYER.CH1.TRENCH,#i3.PPLayer(self.process, self.purpose),
                                  center=(0, (self.bar_length + self.bar_extra_length) * 0.5),
                                  box_size=(self.bar_width, self.bar_length + self.bar_extra_length))

            # Draw the other bars 
            for i in range((self.number_of_bars - 1)/2):
                elems += i3.Rectangle(layer=i3.TECH.PPLAYER.CH1.TRENCH,#i3.PPLayer(self.process, self.purpose),
                                      center=(- (i+1)*self.spacing, self.bar_length * 0.5),
                                      box_size=(self.bar_width, self.bar_length))

            for j in range((self.number_of_bars - 1)/2):
                elems += i3.Rectangle(layer=i3.TECH.PPLAYER.CH1.TRENCH,#i3.PPLayer(self.process, self.purpose),
                                      center=((j+1)*self.spacing, self.bar_length * 0.5),
                                      box_size=(self.bar_width, self.bar_length))

            return elems
