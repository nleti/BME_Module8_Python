from shutil import move
import pygame
from pytmx.util_pygame import load_pygame
from Config import *
from ClassHero import Hero
from ClassBackground import Background
from ClassVirusRed import VirusRed
from ClassTile import Tile
from ClassVirusGreen import VirusGreen

class Level():
    def __init__(self,displaySurface):
        #Load the level tmx file
        self.levelData = load_pygame(LEVEL_PATH + "level1/level.tmx")

        self.background = Background()
        
        # Groups for organizing our sprites
        self.hero = pygame.sprite.GroupSingle()
        self.viruses = pygame.sprite.Group()
        self.platformTiles = pygame.sprite.Group()

        # Pull the platform tile layer from the TMX level
        layer = self.levelData.get_layer_by_name('Platforms')

        # Loop through each tile in the Platforms layer and create Tile sprites
        for x, y, tileSurface in  layer.tiles():
            # Convert tile location from grid space into pixel space
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.platformTiles.add(tile)
        
        # Add hero to the level (starting position + facing direction) 
        self.hero.add(Hero((32, 464), faceRight = True))
        self.viruses.add(VirusRed((200,400),moveRight = True))
        self.viruses.add(VirusRed((300,300),moveRight = False))
        
        # The surface we draw everything on (screen from main game loop)
        self.displaySurface = displaySurface

    def update(self):
        # Update hero logic (movement, physics, collision, etc.)
        self.hero.update(self)

        # Update viruses (movement, behavior, etc.)
        self.viruses.update(self)
 
      
    def draw(self):
        self.background.draw(self.displaySurface)
        # Draw static platform tiles
        self.platformTiles.draw(self.displaySurface)
        self.hero.draw(self.displaySurface)
        self.viruses.draw(self.displaySurface)

    # Draw the hero manually because GroupSingle doesn't auto-draw sprites
    def run(self):
        # Game loop call: update logic then draw everything to the screen
        self.update()
        self.draw()
