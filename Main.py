import pygame
import time
from Color import Color
from Ticker import Ticker
from Simulations import Random_sim, Solar_system, User_controlled


"""
TODO:
    - Zooming function
    - Drawer class that can draw and update figures based on a list of points and a rotation
    - Player controlled node with engine and particles
    - Saving simulation state with button
    - Reading simulation states
    - Visaul effect for merging bodies
    - Selection buttons for showing force and velocity for each particle
"""


class Window:
    """
    Handles the main components of a simulation. Contains the game loop and 
    functionality for panning and drawing lines on the screen. All actual 
    simulation in handled in the Simulation object, to which pan_offset and
    drawn lines are passed.
    """
    
    def __init__(self, window_x, window_y, background_colour):
        pygame.init() 
        self.window_x = 800
        self.window_y = 800
        self.font = pygame.font.SysFont('monospace', 15) 
        self.bg = Color.LGREY
        self.screen = pygame.display.set_mode((window_x, window_y))
        self.screen.fill(self.bg)
        self.pan_offset = [0,0]

    def main_loop(self, simulation):
        """
        Pygame main loop. Uses the ticker class to create consistent timespaces
        between ticks. In the main loop: Updates simulation, checks events,
        updats statistics on screen, draws screen en increments tick. 
        """
        running = True
        ticker = Ticker(start_time=time.time(), tick_len=1/30)
        arrowkey_hold = {pygame.K_LEFT:False, pygame.K_RIGHT:False, pygame.K_UP:False}
        
        # Main loop
        while running:  

            # Update simulation                       
            simulation.update_bodies(ticker.i)  
            self.screen.fill(self.bg)
            simulation.draw(self.screen, self.pan_offset, self.bg)
            
            # Check events
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:
                    running = False
                if event.type ==pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.pan(simulation)
                    if event.button == 3:
                        self.mouse_draw(simulation)
                if event.type == pygame.KEYDOWN:
                    if event.key in arrowkey_hold:
                        arrowkey_hold[event.key] = True
                if event.type == pygame.KEYUP:
                    if event.key in arrowkey_hold:
                        arrowkey_hold[event.key] = False
                    
            # Arrow key hold - for user controlled particle
            if arrowkey_hold[pygame.K_LEFT]:
                self.key_left(simulation)
            if arrowkey_hold[pygame.K_RIGHT]:
                self.key_right(simulation)
            if arrowkey_hold[pygame.K_UP]:
                self.key_up(simulation, 0.15)
                        
            # Tick load stats
            stats = ticker.string_stats()       
            self.display_textlist(stats, Color.DGREY, 15, 5)
            bodies_text = f'nr_bodies : {len(simulation.bodies)}'
            self.display_text(bodies_text, Color.DGREY, 650, 5)
            
            # Screen display and next tick
            pygame.display.flip()               # Draw screen
            ticker.next_tick()                  # Incement tick
         
        pygame.quit()
        
    def pan(self, simulation):
        """
        Pans the simulation screen using the left mouse button. The x and y
        pan_offset is passed to all drawing functions.
        """
        initial_offset = self.pan_offset.copy() # Offset when panning is started
        pan_start = pygame.mouse.get_pos()      # Initial position of mouse
        hold = True
        while hold:
            pan_new = pygame.mouse.get_pos()    # Computing pan offset
            self.pan_offset[0] = initial_offset[0] + pan_new[0] - pan_start[0]
            self.pan_offset[1] = initial_offset[1] + pan_new[1] - pan_start[1]
            self.screen.fill(self.bg)           
            sim.draw(self.screen, self.pan_offset, self.bg)     
            pygame.display.flip()
            for event in pygame.event.get():    # check for mouse release
                if event.type == pygame.MOUSEBUTTONUP:
                    hold = False
    
    def mouse_draw(self, simulation):
        """
        Lets the user draw a line with their rigt mouse button. The line info
        is then passed on the the simulation which can use it to create new
        particles.
        """
        hold = True
        duration = 1    # Increases when the mouse is pressed longer
        start_pos = pygame.mouse.get_pos()
        while hold:
            end_pos = pygame.mouse.get_pos()
            self.screen.fill(self.bg)
            pygame.draw.circle(self.screen, Color.DGREY, start_pos, int(duration))
            pygame.draw.line(self.screen, Color.DGREY, start_pos, end_pos)
            sim.draw(self.screen, self.pan_offset, self.bg)
            pygame.display.flip()
            for event in pygame.event.get():    # check for mouse release
                if event.type == pygame.MOUSEBUTTONUP:
                    hold = False
                    simulation.user_drawn_particle(start_pos, end_pos, duration, self.pan_offset)
            duration += 0.03
        
    def display_text(self, text, color, x, y):
        """
        Draws one line of text on specified coordinates
        """
        textblock = self.font.render(text, True, color)
        self.screen.blit(textblock, (x,y))
    
    def display_textlist(self, text_list, color, x, y):
        """
        Draws a list of text
        """
        for line in text_list:  
            self.display_text(line, color, x, y)
            y += 15

    def key_left(self, simulation):
        simulation.arrowkey_rotation(-1)
    
    def key_right(self, simulation):
        simulation.arrowkey_rotation(1)
    
    def key_up(self, simulation, force):
        simulation.arrowkey_acceleration(force)



# Parameters
x, y = 800, 800
simtype = 3

# Simulation types
if simtype == 1:
    sim = Random_sim(G=0.001)
    sim.generate_bodies(nr_planets=5, nr_particles=50, max_pos = [x,y])
    
elif simtype == 2:
    sim = Solar_system(G=0.001)
    sim.generate_bodies(nr_planets=60, max_pos=[x,y])

elif simtype == 3:
    sim = User_controlled(G=0.001)
    sim.generate_bodies(max_pos=[x,y])


# Running
w = Window(x, y, Color.LGREY)
w.main_loop(sim)
    





