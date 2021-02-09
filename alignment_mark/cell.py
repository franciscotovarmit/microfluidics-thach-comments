"""

PCell for Alignment markers

Author: Phuong Tang, Markus Knoerzer, Thach Nguyen

"""
from microfluidics_ipkiss3.technology import *
from ipkiss3 import all as i3
from vernier_scale import VernierScale
from cross_mark import CrossMark

__all__ = ["AlignmentMark"]

class AlignmentMark(i3.PCell):
    """
    Alignment mark between two process layers.
    """
    
    # List of Vernier scales and crosses for a basecell. They are locked properties and defined by default functions
    verniers = i3.ChildCellListProperty(locked=True, doc="Vernier scales")
    cross_marks = i3.ChildCellListProperty(locked=True, doc="Cross Marks")

    _name_prefix = "ALIGNMENT_MARKER" 

    def _default_verniers(self):
        vern_1 = VernierScale()        
        vern_2 = VernierScale()
        return [vern_1, vern_2]

    def _default_cross_marks(self):
        # Dark Cross on layer 1
        dark_cross = CrossMark()        
        # Open Cross on layer 1 
        open_cross = CrossMark()
        
        return [dark_cross, open_cross]

    class Layout(i3.LayoutView):
        """
        Alignment mark layout view.
        """

        # Specify two layers on which markers are drawn
        process1 = i3.ProcessProperty(default=i3.TECH.PPLAYER.CH2.TRENCH)#i3.TECH.PROCESS.CHANNEL_1, doc="Process Layer 1")  #was i3.TECH.PROCESS.WG
        process2 = i3.ProcessProperty(default=i3.TECH.PPLAYER.CH1.TRENCH)#i3.TECH.PROCESS.CHANNEL_2, doc="Process Layer 2")

        # Properties of crosses
        dark_cross_bar_width = i3.PositiveNumberProperty(default=30, doc="width of the dark cross")
        open_cross_bar_width = i3.PositiveNumberProperty(default=40, doc="width of the open cross")
        cross_boundary_width = i3.PositiveNumberProperty(default=150, doc="width of the cross boundary box")
    
        # Basic properties of Vernier scales
        vern_spacing_short = i3.PositiveNumberProperty(default=18, doc="spacing between bars of shorter vernier scale")
        vern_spacing_long = i3.PositiveNumberProperty(default=18.5, doc="spacing between bars of longer vernier scale")
        vern_number_of_bar = i3.IntProperty(default=13, doc="the number of vernier bars")
    
        # Detailed properties of Vernier scales
        vern_bar_length = i3.PositiveNumberProperty(default=30, doc="length of the shortest bars on the scale")
        vern_bar_extra_length = i3.PositiveNumberProperty(default=10, doc="extra length of the central bar")
        vern_bar_width = i3.PositiveNumberProperty(default=5, doc="width of a single bar")

        # Separation between Vernier scales and Crosses section
        vern_cross_spacing = i3.PositiveNumberProperty(default=30,
                                      doc="Distance between cross box and closest edge of scales")

        # Separation between 2 scales of 2 layers
        vern_layer_gap = i3.NonNegativeNumberProperty(default=0.0, doc="gap between 2 scales of 2 layers on alignment")

        def _default_verniers(self):
            vern_1 = self.cell.verniers[0].Layout(spacing=self.vern_spacing_long,
                                                number_of_bars=self.vern_number_of_bar,
                                                bar_length=self.vern_bar_length,
                                                bar_extra_length=self.vern_bar_extra_length,
                                                bar_width=self.vern_bar_width)#,
                                                #process=self.process1)
                                                
            vern_2 = self.cell.verniers[1].Layout(spacing=self.vern_spacing_short,
                                                number_of_bars=self.vern_number_of_bar,
                                                bar_length=self.vern_bar_length,
                                                bar_extra_length=self.vern_bar_extra_length,
                                                bar_width=self.vern_bar_width)#,
                                                #process=self.process2)

            return [vern_1, vern_2]

    
        def _default_cross_marks(self):
            # Dark Cross on layer 1
            dark_cross = self.cell.cross_marks[0].Layout(inversion=False, 
                                                         cross_bar_width=self.dark_cross_bar_width,
                                                         cross_boundary_width=self.cross_boundary_width)#,
                                                         #process=self.process1)

            open_cross = self.cell.cross_marks[1].Layout(inversion=True, 
                                                         cross_bar_width=self.open_cross_bar_width,
                                                         cross_boundary_width=self.cross_boundary_width)#,
                                                         #process=self.process2)
            return [dark_cross, open_cross]

        def _generate_instances(self, insts):
            insts += i3.SRef(reference=self.cross_marks[0])
            insts += i3.SRef(reference=self.cross_marks[1])
            
            vern_1_horz_trans = i3.VMirror() + \
                                i3.Translation((0, -self.cross_boundary_width * 0.5 - self.vern_cross_spacing -
                                                (self.vern_bar_length + self.vern_bar_extra_length) - self.vern_layer_gap))            
            
            insts += i3.SRef(reference=self.verniers[0], transformation=vern_1_horz_trans)           
            
            vern_2_horz_trans = i3.Translation((0, -self.cross_boundary_width * 0.5 - self.vern_cross_spacing -
                                                (self.vern_bar_length + self.vern_bar_extra_length)))        
            
            insts += i3.SRef(reference=self.verniers[1], transformation=vern_2_horz_trans) 

            vern_1_vert_trans = i3.Rotation(rotation=90) + \
                                i3.Translation((-self.cross_boundary_width*0.5 - 
                                                self.vern_cross_spacing -
                                                (self.vern_bar_length + self.vern_bar_extra_length) -
                                                self.vern_layer_gap,
                                                0))
                                
            insts += i3.SRef(reference=self.verniers[0], transformation=vern_1_vert_trans)  
            
            vern_2_vert_trans = i3.Rotation(rotation=270) + \
                                i3.Translation((-self.cross_boundary_width*0.5 -
                                                (self.vern_bar_length + self.vern_bar_extra_length) -
                                                self.vern_cross_spacing, 0))                    
            insts += i3.SRef(reference=self.verniers[1], transformation=vern_2_vert_trans)  
            
            return insts

if __name__ == "__main__":
    s = AlignmentMark()   # Create New Fluidic_Circuit object.
    s_layout = s.Layout()   # Define the Layout for the Fluidic_Circuit object.
    s_layout.visualize()         # Visualise the Fluidic_Circuit object in 2D.
    s_layout.visualize_2d()