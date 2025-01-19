from pygame.math import Vector2
import pygame


ORANGE = (254, 138, 24)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class PhysicsObject:

    def __init__(self, x, y, mass, heading, surface, radius):
        self.vec = Vector2(x,y)
        self.heading = heading
        self.mass = mass
        self.net_force = Vector2(0,0)
        self.friction_force = Vector2(0,0)
        self.acc_vec = Vector2(0,0)
        self.vel_vec = Vector2(0,0)
        self.BLUE = (0, 0, 255)
        self.radius = radius
        self.debug = True
        self.__screen__ = surface

    def show(self):
        #print("SHOW", self.vec)
        pygame.draw.circle(self.__screen__, self.BLUE, (self.vec.x, self.vec.y), self.radius)
        self.__debug_physics__()


    def update(self, dt):
        self.vel_vec += self.acc_vec * dt
        self.vec += self.vel_vec * dt
        if(self.debug):
            self.debug_text(f"Accelaration : {self.acc_vec}")
        self.acc_vec.update(0,0)

    def go_to_target(self, pos_target):
        force_apply = pos_target - self.vec
        self.applyForce(force_apply, 1)

    def applyForce(self, force_vec, num=1):
        #print(force_vec)
        force_vec_copy = force_vec.copy()
        if(self.debug and force_vec_copy.length() != 0):
            # print(num, " ", force_vec_copy)
            mag_force =  force_vec_copy + self.vec + (force_vec_copy.normalize() * self.radius)
            if num == 2:
                pygame.draw.line(self.__screen__, RED, self.vec, mag_force, 5)
            else:     
                pygame.draw.line(self.__screen__, ORANGE, self.vec, mag_force, 5)
        self.acc_vec += (force_vec_copy / self.mass)

    def friction(self, coeff):
        vel_vec_copy = self.vel_vec.copy()

        if(vel_vec_copy.length() != 0):
            vel_vec_copy = vel_vec_copy.normalize()
        normal = self.mass
        self.friction_force = -1 * coeff * normal * vel_vec_copy
        self.applyForce(self.friction_force, 2)
    
    def __debug_physics__(self):
        if(self.debug):
            # true
            if(self.vel_vec.length() != 0):
                general_vel_vec = self.vel_vec + self.vec + (self.vel_vec.normalize() * self.radius)
                pygame.draw.line(self.__screen__, GREEN, self.vec, general_vel_vec, 5)

            self.debug_text(f"Velocity(Green) : {self.vel_vec}", 10, 40)


    def debug_text(self, text, x = 10, y = 10):
        FONT = pygame.font.Font(None, 30)
        debug_surf = FONT.render(str(text), True, 'White')
        debug_rect = debug_surf.get_rect(topleft=(x,y))
        pygame.draw.rect(self.__screen__, 'Black', debug_rect)
        self.__screen__.blit(debug_surf, debug_rect)


    def edges(self, height, width):
        if self.vec.y > height:
            self.vec.update(self.vec.x, 0)
        if self.vec.y < 0:
            self.vec.update(self.vec.x, height - 1)
        if self.vec.x > width:
            self.vec.update(0, self.vec.y)
            #print(self.vec)
        if self.vec.x < 0:
            self.vec.update(width - 1, self.vec.y)

    def switchDebug(self, bool):
        self.debug = bool

    def debug_joystick(self, axesX, axesY):
        w, h = pygame.display.get_surface().get_size()
        circle_center = Vector2(w-50, h-50)
        radius = 50
        if self.debug:  # Only draw when debugging is enabled
        # Draw the outer circle (joystick boundary)
            pygame.draw.circle(self.__screen__, (255, 255, 255), circle_center, radius, 5)

        # Compute the joystick's directional vector
        vec_dir_joy = Vector2(axesX, axesY) * radius  # Scale by the outer circle's radius
        if vec_dir_joy.length() > radius:  # Cap the vector length to the circle's radius
            vec_dir_joy = vec_dir_joy.normalize() * radius

        # Compute the position of the joystick indicator
        indicator_pos = circle_center + vec_dir_joy

        # Draw the joystick position indicator (inner circle)
        pygame.draw.circle(self.__screen__, (0, 255, 0), indicator_pos, 10)




