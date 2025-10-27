import pygame
from Config import *
from ClassSpriteSheet import SpriteSheet

runSprties = [
    (24, 16, 40, 52),
    (104, 16, 40, 52),
    (184, 16, 40, 52),
    (264, 16, 40, 52),
    (344, 16, 40, 52),
    (424, 16, 40, 52),
    (504, 16, 40, 52),
    (584, 16, 40, 52)
]

idleSprites = [
    (12, 12, 44, 52),
    (76, 12, 44, 52),
    (140, 12, 44, 52),
    (204, 12, 44, 52)
 ]

attackSprites = [
    (4, 0, 92, 80),
    (100, 0, 92, 80),
    (196,0, 92, 80),
    (294, 0, 92, 80),
    (388,0, 92, 80),
    (484, 0, 92, 80),
    (580, 0, 92, 80),
    (676, 0, 92, 80)
]


class Hero():

    def __init__(self, position, faceRight):

        # Load Sprites
        # Paths to get the character animations
        idlepath = os.path.join(SPRITESHEET_PATH, "Character","Idle", "Idle-Sheet.png")
        runpath = os.path.join(SPRITESHEET_PATH, "Character","Run","Run-Sheet.png")
        runattack = os.path.join(SPRITESHEET_PATH, "Character","Attack","AttackSheet.png")

        idleSpriteSheet = SpriteSheet(idlepath, idleSprites)
        runSpriteSheet = SpriteSheet(runpath, runSprties)
        attackSpriteSheet = SpriteSheet(runattack, attackSprites)

        self.spriteSheets = {
            'IDLE' : SpriteSheet(idlepath, idleSprites),
            'RUN' : SpriteSheet(runpath, runSprties),
            'ATTACK' : SpriteSheet(runattack, attackSprites)
        }

        self.animationIndex = 0
        self.facingRight = faceRight
        self.currentState = 'IDLE'
        self.xDir = 0
        self.speed = SPEED_HERO
        self.xpos = position[0]
        self.ypos = position[1]

        # Jump physics
        self.yVel = 0
        self.gravity = 0.6
        self.jumpPower = -10
        self.isJumping = False

        #CHECK IF WORKS
        self.animationspeed = ANIMSPEED_HERO_DEFAULT
        self.image = None
        self.currentAnimation = []

    def update(self, level):
        self.previousState = self.currentState
        self.xDir = 0
        keys =pygame.key.get_pressed()

        if self.currentState != 'ATTACK':
            # Jump 
            if keys[pygame.K_w] and not self.isJumping:
                self.yVel = self.jumpPower
                self.isJumping = True
                self.currentState = 'JUMP'

            # Attack 
            if keys[pygame.K_SPACE]:
                self.currentState = 'ATTACK'

            # Horizontal movement
            elif keys[pygame.K_a]: # move left
                self.xDir = -1
                self.facingRight = False
                self.currentState = 'RUN'

            elif keys[pygame.K_d]: # move right
                self.xDir = 1
                self.facingRight = True
                self.currentState = 'RUN'

            # Idle
            else:
                self.currentState = 'IDLE'

        
        self.selectAnimation()

        # Reset animati9on if state changed
        if self.previousState != self.currentState:
            self.animationIndex = 0

        # Updates Image
        self.image = self.currentAnimation[int(self.animationIndex)]
        
        # Updates rects based on state 
        if self.currentState == 'IDLE':
            self.rect = pygame.Rect(self.xpos - 22, self.ypos - 52, 44, 52)
        elif self.currentState == 'RUN':
            self.rect = pygame.Rect(self.xpos - 20, self.ypos - 48, 40, 48)
        elif self.currentState == 'ATTACK':
            self.rect =pygame.Rect(self.xpos - 44, self.ypos - 64, 88, 64)
        elif self.currentState == "JUMP":
            self.rect = pygame.Rect(self.xpos - 30, self.ypos - 60, 60, 60)

        # Animation update
        self.image = self.currentAnimation[int(self.animationIndex)]
    
        if self.currentState == 'IDLE':
            self.rect = pygame.Rect(self.xpos - 22, self.ypos - 52, 44, 52)

        self.animationIndex += self.animationspeed
        if self.animationIndex >= len(self.currentAnimation):
            self.animationIndex = 0
            self.currentState = 'IDLE'

        # Move Hero
        self.moveHorizontal(level)
        self.moveVertical(level)


    def draw(self, displaySurface):
        displaySurface.blit(self.image, self.rect)



    def selectAnimation(self):
        # Sets animation speed
        self.animationspeed = ANIMSPEED_HERO_DEFAULT
        if self.currentState == 'IDLE':
            self.animationspeed = ANIMSPEED_HERO_IDLE

        # Selects correct sprite sheet
        spriteSheet = self.spriteSheets[self.currentState]
        self.currentAnimation = spriteSheet.getSprites(flipped = not self.facingRight)


    def moveHorizontal(self, level):
        self.rect.centerx += self.xDir * self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH

        self.xpos = self.rect.centerx


    def moveVertical(self, level):
        # Apply gravity
        self.yVel += self.gravity
        self.ypos += self.yVel

        # Simulate ground 
        ground_level = 400
        if self.ypos >= ground_level:
            self.ypos = ground_level
            self.yVel = 0
            self.isJumping = False
            if self.currentState == 'JUMP':
                self.currentState = 'IDLE'