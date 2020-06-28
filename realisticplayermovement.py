# https://github.com/EmilyBoarer/PlayerMovement

import pygame

pygame.init()

width, height = 1920,1080 # put your screen resolution here!
screen = pygame.display.set_mode((width,height), pygame.FULLSCREEN)

clock = pygame.time.Clock()

SCALE = 200

class PhysicsObject:
    def __init__(self):
        self.x = 7*SCALE
        self.y = 5*SCALE
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.terminalVelocity = 4 
        self.coeffFriction = 0.9 # coefficient with the ground must be between 0 and 1 in the real world
        self.thrust = 100000
        self.mass = 2000 # rather unrealistic but makes the physics work as intended to yeah,,, a feature?

        #acceleration due to gravity is 30 here
        self.weight = 30 * self.mass   #the mass cancels later, so can it be removed?
        self.Fmax = self.coeffFriction * self.weight

    def fricForce(self, thrust, v):
        if abs(thrust) > self.Fmax:
            return thrust # this means only friction to slow down # uncomment the 4 lines below and comment this one out for a more accurate simulation
            # if thrust > 0:
            #     return thrust - self.Fmax
            # else:
            #     return thrust + self.Fmax
        elif abs(v) > 0.2: # accounts for skipping over 0 repeatedly, deceleration forcec
            if v > 0:
                return -self.Fmax 
            else:
                return self.Fmax
        else:
            return 0

    def update(self, xinput, yinput, ticks):
        #calculate acceleration
        #F=ma   =>   a=F/m
        f = self.fricForce(xinput*self.thrust,self.vx)
        if f != 0:
            self.ax = f/self.mass 
        else: # should be stationary
            self.ax = 0
            self.vx = 0

        f = self.fricForce(yinput*self.thrust,self.vy)
        if f != 0:
            self.ay = f/self.mass 
        else: # should be stationary
            self.ay = 0
            self.vy = 0
        
        #calculate new velocity
        ux = self.vx
        uy = self.vy
        # v = u+at   =>   v += at
        self.vx += self.ax * (ticks/1000)  
        self.vy += self.ay * (ticks/1000)  

        #cap to terminal velocity TODO make work for diagonals too
        if self.vx > self.terminalVelocity: self.vx = self.terminalVelocity
        if self.vx < -self.terminalVelocity: self.vx = -self.terminalVelocity

        if self.vy > self.terminalVelocity: self.vy = self.terminalVelocity
        if self.vy < -self.terminalVelocity: self.vy = -self.terminalVelocity

        #calculate new position
        # s = 1/2 (u+v)t    add distance to position, x += s
        self.x += 0.5*(ux+self.vx)*(ticks/1000)*SCALE
        self.y += 0.5*(uy+self.vy)*(ticks/1000)*SCALE

        #keep bounded in region
        if self.x < 0:
            self.x = 0
            self.vx = 0
            self.ax = 0

        if self.x > 1920-SCALE:
            self.x = 1920-SCALE
            self.vx = 0
            self.ax = 0

        if self.y < 0:
            self.y = 0
            self.vy = 0
            self.ay = 0

        if self.y > 1080-SCALE:
            self.y = 1080-SCALE
            self.vy = 0
            self.ay = 0

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
    
    player.update(xThrust, yThrust, ticks)
    
    screen.fill((0,0,0))
    
    screen.blit(p,(player.x, player.y))

    pygame.display.flip()

pygame.quit()
