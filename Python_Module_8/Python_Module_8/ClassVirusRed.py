import pygame
from Config import *
from ClassSpriteSheet import SpriteSheet

virusSprites = [
    (16,0,48,48),
    (80,0,48,48),
    (144,0,48,48),
    (208,0,48,48)
    ]


class VirusRed(pygame.sprite.Sprite):

    def __init__(self,position,moveRight):
        super().__init__()

        # --- Load spritesheet ---
        # Normal movement of sprite sheet
        viruspath = os.path.join(SPRITESHEET_PATH, "Enemies","Virus_Red", "virus1_red.png")
        self.flySpriteSheet = SpriteSheet(os.path.join(viruspath),virusSprites)

        virusattackpath = os.path.join(SPRITESHEET_PATH, "Enemies", "Virus_Red","virus1_red_ATTACK.png")
        self.attackSpriteSheet = SpriteSheet(os.path.join(virusattackpath), virusSprites)

        virushitpath = os.path.join(SPRITESHEET_PATH,"Enemies", "Virus_Red","virus1_red_HIT.png")
        self.hitSpriteSheet = SpriteSheet(os.path.join(virushitpath),virusSprites)

        # Store spritesheets in a dictionary for easier animation selection
        self.spriteSheets = {
            'FLY': self.flySpriteSheet,
            'ATTACK': self.attackSpriteSheet,
            'DYING': self.hitSpriteSheet
        }

        # Initialise sprite image and position 
        self.image = self.flySpriteSheet.getSprites(moveRight)[0]
        self.rect = self.image.get_rect(bottomleft = position)
        self.movingRight = moveRight
        self.yDir = 0

        # Animation State
        self.animationIndex = 0
        self.currentState = "FLY"
        self.currentAnimation = self.flySpriteSheet.getSprites(moveRight)

    def selectAnimation(self):
        """Update the current animation based on current state."""
        if self.currentState == "FLY":
            self.currentAnimation = self.flySpriteSheet.getSprites(self.movingRight)
        elif self.currentState == "ATTACK":
            self.currentAnimation = self.attackSpriteSheet.getSprites(self.movingRight)
        elif self.currentState == "DYING":
            self.currentAnimation = self.hitSpriteSheet.getSprites(self.movingRight)

    def update(self, level):
        heroRect = level.hero.sprite.rect
        heroX = heroRect.centerx

        # Move horizontally
        if self.currentState != "DYING":
            if not self.movingRight:
                self.rect.x -= SPEED_VIRUS_RED
            else:
                self.rect.x += SPEED_VIRUS_RED


        # Turn around when leaving window bounds
        if self.rect.right < 0:
            self.movingRight = True
        elif self.rect.left > WINDOW_WIDTH:
            self.movingRight = False

        if self.currentState == "DYING":
            self.yDir += GRAVITY
            self.rect.y += self.yDir
            if self.rect.top > WINDOW_HEIGHT:
                self.kill()



        # --- Attack Logic ---
        distance = heroRect.centerx - self.rect.centerx
        
        if self.currentState == 'FLY':
            # Checks vertical alignment with hero
            if heroRect.top < self.rect.bottom <= heroRect.bottom:

                # Moving right: checks if hero in range
                if self.movingRight and 0 <= distance <= ATTACK_RANGE:
                    self.currentState = 'ATTACK'
                    self.animationIndex = 0

                # Moving left: checks if hero in range
                elif not self.movingRight and -ATTACK_RANGE <= distance <= 0:
                    self.currentState = 'ATTACK'
                    self.animationIndex = 0


        elif self.currentState == 'ATTACK':
            # Stops attacking when hero out of range
             if (self.movingRight and (distance < 0 or distance > ATTACK_RANGE)) or \
             (not self.movingRight and (distance > 0 or distance < -ATTACK_RANGE)):
                    self.currentState = 'FLY'
                    self.animationIndex = 0 

        

        # --- Update animation ---
        self.selectAnimation()
        self.animationIndex += ANIMSPEED_VIRUS
        if self.animationIndex >= len(self.currentAnimation):
            if self.currentState in ["ATTACK", "DYING"]:
                self.animationIndex = len(self.currentAnimation) - 1
            else:
                self.animationIndex = 0
        self.image = self.currentAnimation[int(self.animationIndex)]

    def die(self):
        """Set the virus to dying state and update animation."""
        if self.currentState != "DYING":
            self.currentState = "DYING"
            self.animationIndex = 0
            # Switch animation to the hit/dying animation
            self.currentAnimation = self.hitSpriteSheet.getSprites(self.movingRight)
        