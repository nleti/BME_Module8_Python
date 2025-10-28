import pygame
from Config import *

class SpriteSheet():

    def __init__(self, spriteSheetPath, spritePositions):
        # Load the full sprite sheet
        image = pygame.image.load(spriteSheetPath).convert_alpha()

        # Lists for animation frames
        self.sprites = []         # normal orientation
        self.spritesFlipped = []  # horizontally flipped

        # Slice frames from the sheet
        for position in spritePositions:
            sprite = image.subsurface(pygame.Rect(position))
            self.sprites.append(sprite)
            self.spritesFlipped.append(pygame.transform.flip(sprite, True, False))

    def getSprites(self, flipped):
        # Return normal or flipped frames based on direction
        if flipped:
            return self.spritesFlipped
        else:
            return self.sprites