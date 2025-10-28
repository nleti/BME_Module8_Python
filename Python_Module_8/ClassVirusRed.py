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

        # Attack sprite sheet
        virusattackpath = os.path.join(SPRITESHEET_PATH, "Enemies", "Virus_Red","virus1_red_ATTACK.png")
        self.attackSpriteSheet = SpriteSheet(os.path.join(virusattackpath), virusSprites)

        # Initialise sprite image and position 
        self.image = self.flySpriteSheet.getSprites(moveRight)[0]
        self.rect = self.image.get_rect(bottomleft = position)
        self.movingRight = moveRight

        # Animation State
        self.animationIndex = 0
        self.currentState = "FLY"



    def update(self, level):
        heroRect = level.hero.rect
        heroX = heroRect.centerx

        # Move horizontally
        if not self.movingRight:
            self.rect.x -= SPEED_VIRUS_RED
        else:
            self.rect.x += SPEED_VIRUS_RED


        # Turn around when leaving window bounds
        if self.rect.right < 0:
            self.movingRight = True
        elif self.rect.left > WINDOW_WIDTH:
            self.movingRight = False


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

             else:
                    if self.rect.left > heroX or self.rect.left < heroX - 60:
                        self.currentState = 'FLY'
                        self.animationIndex = 0


        # Select animation for current state
        self.selectAnimation()


        # --- Animate sprite ---
        self.animationIndex += self.animationSpeed
        if self.animationIndex >= len(self.currentAnimation):
            if self.currentState == 'ATTACK':
                # Keep attack animation on last frame
                self.animationIndex = len (self.currentAnimation) -1
            else:
                # Loop fly animation
                self.currentState = 'FLY'
                self.animationIndex = 0

        self.image = self.currentAnimation[int(self.animationIndex)]


    def selectAnimation(self):
        # Set the animation speed
        self.animationSpeed = ANIMSPEED_VIRUS

        # Choose animation based on current state
        if self.currentState == "FLY":
            self.currentAnimation = self.flySpriteSheet.getSprites(flipped = self.movingRight)
        elif self.currentState == "ATTACK":
            self.currentAnimation = self.attackSpriteSheet.getSprites(flipped=self.movingRight)


    def draw(self,displaySurface):
        # Draw sprite on the given surface
        displaySurface.blit(self.image,self.rect)
        pass
