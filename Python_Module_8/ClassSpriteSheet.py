import pygame
from Config import *

class SpriteSheet():

    def __init__(self,spriteSheetPath, spritePositions):
        # this is so we can get the animations of the virus, if it is going other way around then it flips it
        image = pygame.image.load(spriteSheetPath).convert_alpha()

        # Lists to hold each frame of animation
        # sprites = normal orientation
        # spritesFlipped = horizontally flipped (for opposite direction movement)

        self.sprites = []
        self.spritesFlipped = []

        # Loop through a list of rectangle positions to slice frames from the sheet
        for position in spritePositions:
            # Extract a single frame from the sprite sheet
            sprite = image.subsurface(pygame.Rect(position))
            self.sprites.append(sprite)
            # Flip the frame horizontally for opposite direction animations
            sprite = pygame.transform.flip(sprite,True,False)
            self.spritesFlipped.append(sprite)

    def getSprites(self,flipped):
        # Return whichever list of animation frames matches character direction
        if flipped == True:
            return self.spritesFlipped

        else:
            return self.sprites