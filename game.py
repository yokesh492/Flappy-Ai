from hmac import new
from tkinter import Y
import pygame
import os
import neat
import random 
import time

Win_width = 500
Win_Heigth = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird1.png'))),pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird2.png'))),pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird3.png')))]
PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','pipe.png')))
BASE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','base.png')))
BG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bg.png')))

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

# to draw the window with bG and bird
def draw_win(win,bird):
    win.blit(BG,(0,0))
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(200,200)
    win = pygame.display.set_mode((Win_width,Win_Heigth))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        bird.move()
        draw_win(win,bird)
    pygame.quit()
    quit()
main()









