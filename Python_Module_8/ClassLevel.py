from shutil import move
import pygame
from Config import *
from ClassHero import Hero
from ClassBackground import Background
from ClassVirusRed import VirusRed
from ClassVirusGreen import VirusGreen

class Level():
    def __init__(self,displaySurface):

        self.background = Background()
        # sets position of the virus and where it is 

        self.hero = pygame.sprite.GroupSingle()
        self.viruses = pygame.sprite.Group()
        
        self.hero.add(Hero((400, 400), faceRight = True))
        self.viruses.add(VirusRed((200,400),moveRight = True))
        self.viruses.add(VirusRed((300,300),moveRight = False))
        
        self.displaySurface = displaySurface

    def update(self):
        self.hero.update(self)
        self.viruses.update(self)

      
    def draw(self):
        self.background.draw(self.displaySurface)
        self.hero.draw(self.displaySurface)
        self.viruses.draw(self.displaySurface)


    def run(self):
        self.update()
        self.draw()
