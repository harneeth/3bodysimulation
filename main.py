import math, time
import numpy as np
import pygame
import os


terminal_length = os.get_terminal_size().columns

class Body:
    def __init__(self, mass, position, velocity, name, color, radius, trail=False, trail_length=500):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.name = name
        self.color = color
        self.radius = radius
        if trail:
            self.trail = []
            self.trail_length = trail_length
        else:
            self.trail = False


class System:
    def __init__(self, time_step=0.1, realtime=True, G=6.67430e-11):
        self.bodies = []
        self.time_step = time_step
        self.realtime = realtime
        self.G = G
    
    def add_body(self, body):
        self.bodies.append(body)
    
    def gravitational_force(self, body1, body2):
        distance = math.dist(body1.position, body2.position)
        f_g = self.G * (body1.mass * body2.mass)/(distance**2)
        dx = body2.position[0] - body1.position[0]
        dy = body2.position[1] - body1.position[1]
        
        ux = dx / distance
        uy = dy / distance

        Fx = f_g * ux
        Fy = f_g * uy

        if distance == 0:
            return [0, 0]

        return [Fx, Fy]
    
    def net_force(self, forces):
        Fx = 0
        Fy = 0

        for force in forces:
            Fx += force[0]
            Fy += force[1]

        return [Fx, Fy]
    
    def velocity_change(self, body, force):
        ax = force[0] / body.mass
        ay = force[1] / body.mass

        vx = body.velocity[0] + ax*self.time_step
        vy = body.velocity[1] + ay*self.time_step

        velocity = [vx, vy]

        body.velocity = velocity

        return velocity
    
    def update(self):
        for body in self.bodies:
            forces = []
            for body2 in self.bodies:
                if body2 != body:
                    gravitational_force = self.gravitational_force(body, body2)
                    forces.append(gravitational_force)
            net_force = self.net_force(forces)
            velocity = self.velocity_change(body, net_force)
            body.position[0] += velocity[0] * self.time_step
            body.position[1] += velocity[1] * self.time_step

            if body.trail != False:
                if len(body.trail) > body.trail_length:
                    body.trail.pop(0)
                
                body.trail.append(body.position[:])
            
            #print(f"[{body.name}] Position: ({body.position[0]}, {body.position[1]}), Velocity: {math.hypot(body.velocity[0], body.velocity[1])}")         
    
    def draw(self, screen, width, height, scale):
        for body in self.bodies:
            x = int(width/2 + body.position[0]*scale)
            y = height - int(height/2 + body.position[1]*scale)
            pygame.draw.circle(screen, body.color, (x,y), body.radius)
            print(f"\033[38;2;{body.color[0]};{body.color[1]};{body.color[2]}m{body.name}\033[0m")
            print(f"\033[38;2;{body.color[0]};{body.color[1]};{body.color[2]}mPosition: ({body.position[0]}, {body.position[1]}) meters,\nVelocity: {math.hypot(body.velocity[0], body.velocity[1])} m/s, x Velocity: {body.velocity[0]} m/s, y Velocity: {body.velocity[1]} m/s\033[0m")
            print()

            if body.trail != False and len(body.trail) > 1:
                points = []
                for pos in body.trail:
                    x = int(width/2 + pos[0]*scale)
                    y = height - int(height/2 + pos[1]*scale)
                    points.append((x, y))
                pygame.draw.aalines(screen, body.color, False, points, blend=1)
        print("-"*terminal_length + "\n")
    
    def run(self, runs, width, height, scale):
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        clock = pygame.time.Clock()
        pygame.display.set_caption("3 Body Simulation")

        if runs == 0:
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                
                self.update()
                screen.fill((0, 0, 0))
                self.draw(screen, width, height, scale)
                pygame.display.flip()
                clock.tick(60)
        
        else:
            run = 0
            while run < runs:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = runs
                
                self.update()
                screen.fill((0, 0, 0))
                self.draw(screen, width, height, scale)
                pygame.display.flip()
                clock.tick(60)

                run += 1
        
        pygame.quit()
        quit()



# Values are Figure-8 orbit initial conditions - you can experiment with them
body1 = Body(1, [0.97000436,-0.24308753], [0.46620368,0.43236573], "Body 1", (100, 100, 100), 10, True)
body2 = Body(1, [-0.97000436,0.24308753], [0.46620368,0.43236573], "Body 2", (82, 196, 113), 10, True)
body3 = Body(1, [0, 0], [-0.93240736,-0.86473146], "Body 3", (82, 158, 196), 10, True)


world = System(0.005, True, 1)
world.add_body(body1)
world.add_body(body2)
world.add_body(body3)

world.run(0, 1500, 700, 100)
