import pygame

class Collectible(pygame.sprite.Sprite):
    def __init__(self, tmx_object):
        super().__init__()
        # Use Tiled object’s position
        self.rect = pygame.Rect(tmx_object.x, tmx_object.y, tmx_object.width, tmx_object.height)
        
        # Use the Tiled object's image (surface)
        self.image = tmx_object.image  # pytmx stores the object’s tile image here

    def collect(self, hero):
        # Example: increase score or health
        hero.score += 1
        self.kill()




