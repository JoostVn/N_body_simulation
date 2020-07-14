from random import randint, uniform
from Color import Color
from Particle import Arrow, Planet
from math import sqrt


class N_Body:
    """
    Simulation parent class. All other classes inherit all functionality from
    this class, with the exception of different generate_bodies functions,
    which determines the actual bodies in the simulation. New simulations can
    be added by just inhereting this class, and importing them to main.py.
    """
    
    def __init__(self, G):
        self.G = G
        
    def update_bodies(self, iteration):
        """
        Updates all bodies in the simulation by merging them, computing the 
        net force, updating velocity and updating postions. The trail is not
        updated every iteration to save computational load.
        """
        for p in self.bodies:
            p.merge(self.bodies)  
            p.update_force(self.bodies, self.G)
            p.update_velocity()
            p.update_position() 
            if iteration % 4 == 0:
                p.update_trail()
            
    def draw(self, screen, pan_offset, background_colour):
        """
        Draws the simulation bodies on the Pygame screen.
        """
        for p in self.bodies:
            p.draw_trail(screen, pan_offset)
        for p in self.bodies:
            p.draw(screen, pan_offset)

    def mouse_line(self, start_pos, end_pos, duration, pan_offset):
        """
        Function that can utilize a line drawn in the simulation. This line,
        as well as the duration of the mouse press are used to create a new
        body, velocity and mass.
        """
        vx = 0.02 * (start_pos[0] - end_pos[0])
        vy = 0.02 * (start_pos[1] - end_pos[1])
        mass = duration ** 3
        x = start_pos[0] - pan_offset[0]
        y = start_pos[1] - pan_offset[1]
        p = Planet([x,y], mass, Color.RED, Color.MGREY, [vx,vy], 20)
        self.bodies.append(p)



class Random_sim(N_Body):
    
    """
    Simple simulation with a number of random arrows, with little mass, and 
    planets, with larger mass.
    """
    
    def __init__(self, G):
        super().__init__(G)
    
    def generate_bodies(self, nr_planets, nr_particles, max_pos):
        self.bodies = []
        for i in range(nr_particles):
            position = [randint(0,max_pos[0]),randint(0,max_pos[1])] 
            mass = randint(1,200)
            color = Color.random_vibrant()                       
            trail_color = Color.MGREY       
            velocity = [uniform(-2,2),uniform(-2,2)]
            trail_size = 30
            p = Arrow(position, mass, color, trail_color, velocity, trail_size)
            self.bodies.append(p)
        
        for i in range(nr_planets):
            position = [randint(0,max_pos[0]),randint(0,max_pos[1])]
            mass = randint(200,1000)
            color = Color.DGREY       
            trail_color = Color.MGREY               
            velocity = [uniform(-1,1),uniform(-1,1)]
            trail_size = 200
            p = Planet(position, mass, color, trail_color, velocity, trail_size)
            self.bodies.append(p)
        
    
        
    
    
    
class Solar_system(N_Body):
    
    """
    Simulation with a central 'sun' and numerous planets rotating around it.
    """
    
    
    def __init__(self, G):
        super().__init__(G)
    
    def generate_bodies(self, nr_planets, max_pos):
        self.bodies = []
        
        # Simulation starting midpoint of screen
        mid = [int(max_pos[0]/2), int(max_pos[1]/2)]
        
        # Creating sun
        sun = Planet(position = mid, mass = 30000, color = Color.GOLD,                      
                     trail_color = Color.MGREY, velocity = [0,0], trail_size = 50)
        self.bodies.append(sun)
        
        for i in range(nr_planets):
            
            # Random parameters
            x, y = randint(0, max_pos[0]), randint(0, max_pos[1])
            mass = randint(1,150)
            
            # Unit vector pointing at the sun
            dis_x = mid[0] - x
            dis_y = mid[0] - y
            dis = sqrt(dis_x**2 + dis_y**2)
            sun_normalized_x = dis_x / dis         
            sun_normalized_y = dis_y / dis 
            
            # Velocity unit vector, perpendicular to sun vector
            vel_x = sun_normalized_y 
            vel_y = - sun_normalized_x

            # Velocity: velocity unit vector scaled with distance, G, sun mass and constant
            combined_mass = self.bodies[0].m + mass
            vx = 3.8 * sqrt(self.G * combined_mass / sqrt(dis)) * vel_x
            vy = 3.8 * sqrt(self.G * combined_mass / sqrt(dis)) * vel_y
            
            # Creating planet
            position = [x, y] 
            color = Color.random_dull()    
            trail_color = color
            velocity = [vx, vy]
            trail_size = 20
            p = Planet(position, mass, color, trail_color, velocity, trail_size)
            self.bodies.append(p)
        





