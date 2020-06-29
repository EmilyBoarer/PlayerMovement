# https://github.com/EmilyBoarer/PlayerMovement

import pygame

pygame.init()

width, height = 1920,1080 # put your screen resolution here!
screen = pygame.display.set_mode((width,height), pygame.FULLSCREEN)

clock = pygame.time.Clock()

SCALE = 200

class Vector2D:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    def __rmul__(self, value): # this is value * self
        if type(value) == int or type(value) == float: 
            return Vector2D(self.x * value, self.y * value)
        elif type(value) == Vector2D:
            return value.x * self.x + value.y + self.y
        else:
            raise ValueError("Can only multiply two 2D vectors or vector and integer")
    def __mul__(self, value):
        if type(value) == int or type(value) == float:
            return self.__rmul__(value)
        elif type(value) == Vector2D:
            return value.__rmul__(self)
        else:
            raise ValueError("Can only multiply two 2D vectors or vector and integer")
            
    def __add__(self, value):
        if type(value) == Vector2D:
            return Vector2D(self.x + value.x, self.y + value.y)
        else:
            raise ValueError("Can only add two vectors")
    def __abs__(self):
        return (self.x**2 + self.y**2)**0.5  #use pythag to calculate the magnitude of vector

    def copy(self):
        return Vector2D(self.x, self.y)
    

class PhysicsObject:
    def __init__(self):
        self.position = Vector2D(5*SCALE, 5*SCALE)
        self.velocity = Vector2D()
        self.acceleration = Vector2D
        self.terminalVelocity = 4 
        self.thrustPotential = 50 # thrust Force/mass
        self.thrust = Vector2D()
        self.Fmax = 27    # Frictional Force/mass

    def thrustfromvector(self, x, y):
        self.thrust = Vector2D(x, y)
        if abs(self.thrust) != 0 :
            compensation = self.thrustPotential / abs(self.thrust)
            self.thrust = self.thrust * compensation

    def update(self, ticks):
        #calculate acceleration
        #F=ma   =>   a=F/m   (mass is eliminated when declaring forces though, so no need to divide through here)
        if abs(self.thrust) > self.Fmax:
            self.acceleration = self.thrust
        elif abs(self.velocity) > 0.2: # threshold to make the entity actually stop
            resistiveForce = -1 * self.velocity
            compensation = self.Fmax/abs(resistiveForce)
            resistiveForce = resistiveForce * compensation # compensate to make magnitude the same as Fmax
            self.acceleration = resistiveForce
        else: # should be stationary
            self.acceleration = Vector2D()
            self.velocity = Vector2D()     #make both 0, so stationary
        
        #calculate new velocity
        prevVelocity = self.velocity.copy()
        # v = u+at   =>   v += at
        self.velocity = prevVelocity + self.acceleration * (ticks/1000)  

        #cap to terminal velocity 
        if abs(self.velocity) > self.terminalVelocity:
            self.velocity = self.velocity * (self.terminalVelocity / abs(self.velocity)) # adjust so scaled down proportionally in x and y so magnitude is terminal velocity

        #calculate new position
        # s = 1/2 (u+v)t    add distance to position, x += s
        self.position = self.position + 0.5*(prevVelocity+self.velocity)*(ticks/1000)*SCALE

        #keep bounded in region
        if self.position.x < 0:
            self.position.x = 0
            self.velocity.x = 0
            self.acceleration.x = 0

        if self.position.x > 1920-SCALE:
            self.position.x = 1920-SCALE
            self.velocity.x = 0
            self.acceleration.x = 0

        if self.position.y < 0:
            self.position.y = 0
            self.velocity.y = 0
            self.acceleration.y = 0

        if self.position.y > 1080-SCALE:
            self.position.y = 1080-SCALE
            self.velocity.y = 0
            self.acceleration.y = 0

player = PhysicsObject()


p = pygame.surface.Surface((SCALE,SCALE))
p.fill((255,255,255))

running = True
while running:
    ticks = clock.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running=False
    if keys[pygame.K_a]:    xThrust = -1
    elif keys[pygame.K_d]:  xThrust = 1
    else:                   xThrust = 0
    if keys[pygame.K_w]:    yThrust = -1
    elif keys[pygame.K_s]:  yThrust = 1
    else:                   yThrust = 0
    
    player.thrustfromvector(xThrust, yThrust)
    player.update(ticks)
    
    screen.fill((0,0,0))
    
    screen.blit(p,(player.position.x, player.position.y))

    pygame.display.flip()

pygame.quit()
