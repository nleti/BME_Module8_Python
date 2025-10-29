from shutil import move
import pygame
from pytmx.util_pygame import load_pygame
from Config import *
from ClassHero import Hero
from ClassBackground import Background
from ClassVirusRed import VirusRed
from ClassTile import Tile
from ClassVirusGreen import VirusGreen
from ClassCollectible import Collectible

class Level():
    def __init__(self,displaySurface):
        #Load the level tmx file
        self.levelData = load_pygame(os.path.join( LEVELS_PATH, "level.tmx"))


        # Initialize groups and background
        self.background = Background()
        self.hero = pygame.sprite.GroupSingle()
        self.viruses = pygame.sprite.Group()
        self.platformTiles = pygame.sprite.Group()
        self.backgroundTiles = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()

        # Platform layer
        layer = self.levelData.get_layer_by_name('Platforms')

        # Load background layers 
        for bg_layer in self.levelData.visible_layers:
             if bg_layer.name != 'Platforms' and hasattr(bg_layer, 'tiles'):
                for x, y, surface in bg_layer.tiles():
                    tile = Tile((x * TILESIZE, y * TILESIZE), surface)
                    self.backgroundTiles.add(tile)


        # Load platform tiles
        for x, y, tileSurface in  layer.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.platformTiles.add(tile)
        
        # Add hero and enemies
        self.hero.add(Hero((32, 464), faceRight = True))
        self.viruses.add(VirusRed((500,300),moveRight = True))
        self.viruses.add(VirusRed((500,350),moveRight = False))
        self.viruses.add(VirusRed((200,280),moveRight = False))
        self.viruses.add(VirusRed((700,500),moveRight = True))
        self.viruses.add(VirusRed((100,100),moveRight = False))
        
        # Surface to draw everything on
        self.displaySurface = displaySurface

    def update(self):
        self.hero.update(self)
        self.viruses.update(self)
 
      
    def draw(self):
        self.background.draw(self.displaySurface)          # static background
        self.backgroundTiles.draw(self.displaySurface)    # tiled background layers
        self.platformTiles.draw(self.displaySurface)      # platforms
        self.viruses.draw(self.displaySurface)           # enemies
        self.hero.draw(self.displaySurface)               # hero on top


    def run(self):
        # Update logic and draw the level
        self.update()
        self.draw()



    def showEndingScreen(self):
        # Create semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # transparent black
        self.displaySurface.blit(overlay, (0, 0))

        # Fonts and text
        font = pygame.font.Font(None, 64)
        text = font.render("Game Over", True, (255, 0, 0))
        subtext = pygame.font.Font(None, 36).render("Press R to Restart", True, (255, 255, 255))

        # Position text
        text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
        subtext_rect = subtext.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 20))

        # Draw text on overlay
        self.displaySurface.blit(text, text_rect)
        self.displaySurface.blit(subtext, subtext_rect)

        pygame.display.update()  # Refresh display

        # Wait for player input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Exit game
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart level
                        waiting = False

