from hmac import new
from tkinter import Y
import pygame
import os
import neat
import random 
import time
pygame.font.init()

Win_width = 500
Win_Heigth = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird1.png'))),pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird2.png'))),pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird3.png')))]
PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','pipe.png')))
BASE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','base.png')))
BG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bg.png')))

STAT_FONT = pygame.font.SysFont("comicsans",50)

class Bird:
    IMG = BIRD_IMGS
    max_rotation = 25
    rot_vel = 20
    animation_time = 5

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.img = self.IMG[0]
        self.height = self.y
        self.vel = 0
        self.img_count = 0

    def jump(self): # each jump the tickcount reset and heigth also reset
        self.vel = -10.5 # neagtive becoz as per pixel top to botton positive and bottom to top negative
        self.tick_count = 0
        self.height = self.y

    def move(self):#it alwys in moves and it goes downwards for each tickcounts , so we use jump to move up 
        self.tick_count +=1 #count increase each second
         #displacement
        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >=16: #going downward more means just be in 16 pos
            d =16
        if d < 0: #going upward means just move littel upward
            d -=2
        self.y = self.y + d # move slowly up or down
        #now going to tilt
        if d<0 or self.y < self.height + 50 :# if still moving upward dont start move down yet
            if self.tilt < self.max_rotation:
                self.tilt = self.max_rotation # tilting in upward direction

        else:#moving nose downward quickly means titlting to downward direction
            if self.tilt > -90:
                self.tilt -= self.rot_vel

    def draw(self,win):
        self.img_count +=1 #showing howmany times game loop runs or image shows
        #now going to show the image animation with 3 image based on the current image_count
        if self.img_count < self.animation_time:
            self.img = self.IMG[0]
        elif self.img_count < self.animation_time*2:
            self.img = self.IMG[1]
        elif self.img_count < self.animation_time*3:
            self.img = self.IMG[2]
        elif self.img_count < self.animation_time*4:
            self.img = self.IMG[1]
        elif self.img_count == self.animation_time*4 +1:
            self.img = self.IMG[0]
            self.img_count = 0

        if self.tilt < -80: # while tilting downward img2 need to show
            self.img = self.IMG[1]
            self.img_count = self.animation_time*2 #not to animation while sunndenly jumps
        
        # to Rotate image action program
        rotated_img = pygame.transform.rotate(self.img,self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)
        win.blit(rotated_img,new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img) 

class Pipe:#second object
    GAP = 200
    VEL = 5

    def __init__(self,x):
        self.x = x
        self.top = 0
        self.bottom = 0
        self.TOP_PIPE = pygame.transform.flip(PIPE,False,True)# to flip the image
        self.BOT_PIPE = PIPE

        self.passed = False
        self.set_height() # to setting the height of the pipe in random manner
    
    def set_height(self):
        self.height = random.randrange(50,450)#getting random no between range
        self.top = self.height - self.TOP_PIPE.get_height() # posistion of the top 
        self.bottom = self.height+ self.GAP # adding gap place then posistion of the bottom untill the end
    
    def move(self):
        self.x -= self.VEL # movement of pipe by frame 
        #print(self.x)   ##################################

    def draw(self,win): #adding the pipe in window
        win.blit(self.TOP_PIPE,(self.x,self.top)) 
        win.blit(self.BOT_PIPE,(self.x,self.bottom))

    def collide(self,bird): #to check the collide
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.TOP_PIPE) # backside algo to get the pixle mask of the object
        bot_mask = pygame.mask.from_surface(self.BOT_PIPE)

        top_offset = (self.x - bird.x,self.top - round(bird.y))  
        bot_offset =  (self.x - bird.x,self.bottom - round(bird.y))

        top_point = bird_mask.overlap(top_mask,top_offset)
        bot_point = bird_mask.overlap(bot_mask,bot_offset)#algo to check the collidation

        if top_point or bot_point:
            return True
        return False

class Base:#third object
    VEL = 5
    img = BASE
    width = BASE.get_width()
    

    def __init__(self,y):
        self.y = y 
        self.x1 = 0 # creating two image and looping it one after another
        self.x2 = self.width
        #print(self.x2)###################################

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width # making continous movement after one another
        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self,win):
        win.blit(self.img,(self.x1,self.y))
        win.blit(self.img,(self.x2,self.y))







# to draw the window with bG and bird
def draw_win(win,bird,pipes,base,score):
    win.blit(BG,(0,0))
    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render('Score: '+str(score),1,(255,255,255))
    win.blit(text,(Win_width -10 - text.get_width(),10))

    base.draw(win)
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(230,350)
    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((Win_width,Win_Heigth))
    clock = pygame.time.Clock()

    score = 0

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        add_pipe = False
        rem = [] # list of removing pipe
        
        for pipe in pipes:
            if pipe.collide(bird):
                pass

            if pipe.x + pipe.TOP_PIPE.get_width() < 0: #pipe cross the window it should be removed
                rem.append(pipe)
            
            if not pipe.passed and pipe.x < bird.x: # if bird pass the pipe means to create the another pipe
                pipe.passed = True
                add_pipe =True

            pipe.move()
        if add_pipe: # adding the pipe instantly
            score += 1
            pipes.append(Pipe(600))
        
        for r in rem: # removing the pipe from the list after it went from the screen
            pipes.remove(r)
        
        if bird.y + bird.img.get_height() >= 730:
            pass
        #bird.move()
        base.move()
        draw_win(win,bird,pipes,base,score)
    pygame.quit()
    quit()
main()









