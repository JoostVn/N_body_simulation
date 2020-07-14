import pygame
from math import sin, cos, atan2
from Color import Color, ColorGradient
from random import uniform



class Body:
    
    def __init__(self, position, mass, color, trail_color, velocity, trail_size):
        self.m = mass           # Particle mass
        self.p = position       # Particle postion (unit vector: x,y)
        self.v = velocity       # Particle velocity (unit vector: x,y)
        self.f = [0,0]          # Particle net force (unit vector: x,y)
        self.rad = max(int(mass ** (1/3)), 1)
        self.trail_color = trail_color
        self.color = color
        self.thickness = self.rad
        self.prev_positions = [(position[0], position[1])]
        self.trail_size = trail_size
   
    def update_force(self, bodies, G):
        """
        Updates the particles' net force based on the gravitational pull of
        each body given in a list, and a gravitational constant.
        """
        Fx, Fy = [], []
        for b in bodies:
            if not b is self:
                x_a, y_a = self.p[0], self.p[1]                     # Body a position
                x_b, y_b = b.p[0], b.p[1]                           # Body b position
                r_ab = ((x_a - x_b)**2 + (y_a - y_b)**2) ** (1/2)   # Cartesian distance
                m_ab = self.m * b.m                                 # Mass product
                rxab = x_b - x_a
                ryab = y_b - y_a
                Fx.append(G * (m_ab / r_ab**2) * rxab)
                Fy.append(G * (m_ab / r_ab**2) * ryab)
        self.f[0], self.f[1] = sum(Fx), sum(Fy)
        
    def update_velocity(self):
        self.v[0] += self.f[0] / self.m
        self.v[1] += self.f[1] / self.m
    
    def update_position(self):
        self.p[0] += self.v[0]
        self.p[1] += self.v[1]
    
    def merge(self, bodies):
        """
        Loops over a given list of bodies. If any of these bodies are 
        within the particles radius, merges the two particles.
        When two particles are merged, are their properties are merged as well. 
        The particle that merges with this particle subsequently gets removed
        from the list of bodies.
        """
        for b in bodies:
            if not b is self:
                x_a, y_a = self.p[0], self.p[1]
                x_b, y_b = b.p[0], b.p[1]
                distance = ((x_a - x_b)**2 + (y_a - y_b)**2) ** (1/2)
                if distance < 0.8 * self.rad:
                    ratio = self.m / (self.m + b.m)
                    self.v[0] = ratio * self.v[0] + (1-ratio) * b.v[0]
                    self.v[1] = ratio * self.v[1] + (1-ratio) * b.v[1]
                    self.m += b.m
                    self.rad = max(int(self.m ** (1/3)), 1)
                    bodies.remove(b)
      
    def bounce(self, xbound, ybound):
        """
        Bounces particles that have exceeded the screen boundaries back
        into to simulation space.
        """
        if self.p[0] > xbound:
            self.p[0] = 2 * xbound - self.p[0]
            self.v[0] = - self.v[0]
        if self.p[1] > ybound:
            self.p[1] = 2 * ybound - self.p[1]
            self.v[1] = - self.v[1]
        if self.p[0] < 0:
            self.p[0] = - self.p[0]
            self.v[0] = - self.v[0]
        if self.p[1] < 0:
            self.p[1] = - self.p[1]
            self.v[1] = - self.v[1]
      
    def update_trail(self):
        """
        Appends the current position to the trail list.  Also 
        removes segments after lines become too long to reduce computational 
        load. Optionally scrambles the tail for a visual effect
        """
        self.prev_positions.append((int(self.p[0]),int(self.p[1])))
        if len(self.prev_positions) > self.trail_size:
            self.prev_positions.pop(0)
        
    def draw_trail(self, screen, pan_offset):
        """
        Draws a line connecting all segments of the prev_positions list using 
        a gradient.
        """
        width = int(max(1, self.rad/3))
        g = ColorGradient(self.trail_color, (230, 230, 230), self.trail_size)
        positions = list(reversed(self.prev_positions))
        offset_positions = [(x+pan_offset[0], y+pan_offset[1]) for x,y in positions]
        for i, p in enumerate(offset_positions[:-1]):
            col = g.get_color(i)
            pygame.draw.line(screen, col, p, offset_positions[i+1], width)

    def draw_line(self, screen, pan_offset, to_position, color):
        """
        Draws a line from the particle to another position. Used for debugging
        and visualizing forces or angles.
        """
        x = self.p[0] + pan_offset[0]
        y = self.p[1] + pan_offset[1]
        to_position[0] += pan_offset[0]
        to_position[1] += pan_offset[1]
        pygame.draw.line(screen, color, (x,y), to_position, 1)




class Arrow(Body):
    """
    Arrow shaped body
    """

    def __init__(self, position, mass, color, trail_color, velocity, trail_size):
        super().__init__(position, mass, color, trail_color, velocity, trail_size) 
    
    def draw(self, screen, pan_offset):
        """
        Draws an arrow on the particles' coordinates indicating its current
        direction. The arrow is defined by X1, Y1 and Y2 which are multiplied
        by the particles' radius.        
        """
        x = self.p[0] + pan_offset[0]
        y = self.p[1] + pan_offset[1]
        theta = atan2(self.v[1],self.v[0])
        X1, Y1, Y2 = 0.6*self.rad, 1.6*self.rad, 0.3*self.rad
        p_top = (int(x + Y1 * cos(theta)), int(y + Y1 * sin(theta)))
        p_right = (int(x - X1 * sin(theta)), int(y + X1 * cos(theta)))
        p_left = (int(x + X1 * sin(theta)), int(y - X1 * cos(theta)))
        p_bottom = (int(x - Y2 * cos(theta)), int(y - Y2 * sin(theta)))
        pointslist = (p_top, p_right, p_bottom, p_left)
        pygame.draw.polygon(screen, self.color, pointslist)
    
    
    
    
class Planet(Body):
    """
    Spherical body
    """
    
    def __init__(self, position, mass, color, trail_color, velocity, trail_size):
        super().__init__(position, mass, color, trail_color, velocity, trail_size) 
    
    def draw(self, screen, pan_offset):
        x = self.p[0] + pan_offset[0]
        y = self.p[1] + pan_offset[1]
        pygame.draw.circle(screen, self.color, (int(x),int(y)), self.rad)
    
    
    
    
class Particle(Body):
    """
    Body used for visual effects
    """
    
    def __init__(self, position, mass, color, trail_color, velocity, trail_size):
        super().__init__(position, mass, color, trail_color, velocity, trail_size) 
        
    def gradient_particle(self, color1, color2, velocity, randomness, duration):
        pass
        
        
    
    
    
    
    
