from random import sample

class Color:
    
    WHITE = (255,255,255)
    DGREY = (70,70,70)
    MGREY = (190,190,190)
    LGREY = (230,230,230)
    NAVY = (20,20,80)
    BLUE = (40,40,200)
    GREEN = (40,200,40)
    RED = (200,40,40)
    GOLD = (240, 190, 50)
    
    def random_vibrant():
        """
        Returns a random vibrant color in RGB format. Works by forcing a 
        large enough difference between the R, G, and B values.
        """
        while True:
            R, G, B = sample(range(0,256), 3)
            diff_sum = abs(R-G) + abs(G-B) + abs(R-B)
            if diff_sum > 200:
                return (R, G, B)
            
    def random_dull():
        """
        Returns a random dull color in RGB format. Works by forcing the RGB 
        difference to be between two values.
        """
        while True:
            R, G, B = sample(range(0,256), 3)
            diff_sum = abs(R-G) + abs(G-B) + abs(R-B)
            totl_sum = R + G + B
            if diff_sum > 80 and diff_sum < 200 and totl_sum  > 200 and totl_sum < 500:
                return (R, G, B)
            
            

class ColorGradient:
    """
    A color gradient object contains two colors, and the number of partitions
    for the desired color gradient. The get_color function returns a color
    that is 'between' the color1 and color2 at the given partition.
    """
    
    def __init__(self, color_1, color_2, nr_partitions):
        self.c1 = color_1
        self.c2 = color_2
        self.parts = nr_partitions
        
    def get_color(self, part):
        """
        Get RGB color values of the color that sits between color1 and color2
        at the desired partition part should be >= 0  and <= nr_partitions. 
        """
        R_width = self.c2[0] - self.c1[0]
        G_width = self.c2[1] - self.c1[1]
        B_width = self.c2[2] - self.c1[2]
        R = int(self.c1[0] + (part / self.parts) * R_width)
        G = int(self.c1[1] + (part / self.parts) * G_width)
        B = int(self.c1[2] + (part / self.parts) * B_width)
        return (R, G, B)
        
        
        
