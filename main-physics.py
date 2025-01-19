import numpy as np
import math
import pygame
import pymunk
import pymunk.pygame_util
import time
from lib_env import PhysicsObject

pygame.init()
pygame.joystick.init()


WIDTH = 800
HEIGHT = 800

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Force")
FPS = 30
DT = 1/FPS
OBJECT_MASS = 20
RADIUS = 20
MAX_VEL = 10
FRICTION_COEFF = 2

JoyStick_Conn = []

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255 ,0)

WIND = pygame.Vector2(100, 20)
GRAVITY = pygame.Vector2(0, 10)

# Movement variables
move_up = move_down = move_left = move_right = False


def vector_move_input_WASD():
    vector_movement_WASD = pygame.Vector2(0, 0)
    if move_up:
        vector_movement_WASD += pygame.Vector2(0, -1)
    if move_down:
        vector_movement_WASD += pygame.Vector2(0, 1)
    if move_left:
        vector_movement_WASD += pygame.Vector2(-1, 0)
    if move_right:
        vector_movement_WASD += pygame.Vector2(1, 0) 

    return vector_movement_WASD.copy()      

def create_ball(space, radius, mass):
    body = pymunk.Body()
    body.position = (300, 300)
    shape = pymunk.Circle(body=body, radius=radius)
    shape.mass = mass
    shape.color = BLUE
    space.add(body, shape) 
    return shape

def main():
    global move_up, move_down, move_left, move_right
    running = True
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity =(0,0)
    prevTime = time.time()

    vector_move = pygame.Vector2(0,0)

    test = PhysicsObject(100,100,OBJECT_MASS,0,win,RADIUS)

    while running:
        # udpate game
        clock.tick(FPS)
        win.fill(BLACK)
        now = time.time()
        dt = now - prevTime
        prevTime = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                joy.init()
                JoyStick_Conn.append(joy)
            if event.type == pygame.JOYDEVICEREMOVED:
                JoyStick_Conn.clear()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:  # W key
                    move_up = True
                elif event.key == pygame.K_s:  # S key
                    move_down = True
                elif event.key == pygame.K_a:  # A key
                    move_left = True
                elif event.key == pygame.K_d:  # D key
                    move_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    move_up = False
                elif event.key == pygame.K_s:
                    move_down = False
                elif event.key == pygame.K_a:
                    move_left = False
                elif event.key == pygame.K_d:
                    move_right = False
        
        # cek joystick
        for joy in JoyStick_Conn:
            axes = joy.get_numaxes()
            for i in range(axes):
                axis = joy.get_axis(i)
                #test.debug_text(f"Axis {i}/{joy.get_numaxes()} value: {axis:>6.3f}", 10, HEIGHT - 20*(i+1))
            axis = joy.get_axis(0)
            vector_move.x = axis
            axis = joy.get_axis(1)
            vector_move.y = axis

            #print(joy.get_axis(9))
            if(joy.get_axis(5) > 0):
                #print("RUN", vector_move)
                test.applyForce(vector_move * 500 * joy.get_axis(5))


        vector_move = vector_move_input_WASD() # berasal dari WASD
        test.debug_joystick(vector_move.x, vector_move.y) # gerak robot
        test.applyForce(vector_move * 100)
        test.friction(FRICTION_COEFF) # gaya gesek
        #test.applyForce(WIND)

        # update game
        test.update(DT)
        test.edges(HEIGHT, WIDTH)
        test.show()
        pygame.display.update()

        

    pygame.quit()

if __name__ == '__main__':
    print("Physic force and friction test")
    main()