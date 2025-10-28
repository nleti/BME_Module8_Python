import pygame
from Config import *
from ClassSpriteSheet import SpriteSheet

# Sprite Coordinates
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

deathSprites = [
    (0,0,64,56),
    (80,0,64,56),
    (160,0,64,56),
    (240,0,64,56),
    (320,0,64,56),
    (400,0,64,56),
    (480,0,64,56),
    (560,0,64,56)
    ]


class Hero(pygame.sprite.Sprite):

    def __init__(self, position, faceRight):
        super().__init__()

        # --- Load Sprite sheets ---
        idlepath = os.path.join(SPRITESHEET_PATH, "Character","Idle", "Idle-Sheet.png")
        runpath = os.path.join(SPRITESHEET_PATH, "Character","Run","Run-Sheet.png")
        attackpath = os.path.join(SPRITESHEET_PATH, "Character","Attack","AttackSheet.png")
        deathpath = os.path.join(SPRITESHEET_PATH, "Character", "Death", "DeathSheet.png")


        # Directionary of animatiuons
        self.spriteSheets = {
            'IDLE' : SpriteSheet(idlepath, idleSprites),
            'RUN' : SpriteSheet(runpath, runSprties),
            'ATTACK' : SpriteSheet(attackpath, attackSprites),
            'DIE' : SpriteSheet(deathpath, deathSprites)
        }

        # --- Animation & State ---
        self.animationIndex = 0
        self.facingRight = faceRight
        self.currentState = 'IDLE'
        self.currentAnimation = []
        self.animationspeed = ANIMSPEED_HERO_DEFAULT

        # --- Position & Movement ---
        self.xDir = 0
        self.speed = SPEED_HERO
        self.xpos = position[0]
        self.ypos = position[1]

        # --- Jump physics ---
        self.yVel = 0
        self.gravity = 0.6
        self.jumpPower = -10
        self.isJumping = False

        # Initial image placeholder
        self.image = None


    def update(self, level):
        """ Update hero state with each frame"""
        self.previousState = self.currentState
        self.xDir = 0
        keys =pygame.key.get_pressed()

        # --- KEYS INPUT ---
        if self.currentState != 'ATTACK' and self.currentState != 'DIE': 
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

        # --- Select animation for current state ---
        self.selectAnimation()

        # Reset animati9on if state changed
        if self.previousState != self.currentState:
            self.animationIndex = 0

        # Updates current image
        self.image = self.currentAnimation[int(self.animationIndex)]
        

        # --- Updates rects based on state ---
        if self.currentState == 'IDLE':
            self.rect = pygame.Rect(self.xpos - 22, self.ypos - 52, 44, 52)
        elif self.currentState == 'RUN':
            self.rect = pygame.Rect(self.xpos - 20, self.ypos - 48, 40, 48)
        elif self.currentState == 'ATTACK':
            self.rect =pygame.Rect(self.xpos - 44, self.ypos - 64, 88, 64)
        elif self.currentState == "JUMP":
            self.rect = pygame.Rect(self.xpos - 30, self.ypos - 60, 60, 60)
        elif self.currentState == 'DIE':
            self.rect =pygame.Rect(self.xpos - 32, self.ypos - 48, 64, 48)

        # --- Animation progression ---
        self.animationIndex += self.animationspeed
        if self.animationIndex >= len(self.currentAnimation):
            if self.currentState == "DIE":
                self.animationIndex = len(self.currentAnimation) - 1
            else:
                self.animationIndex = 0
                self.currentState = 'IDLE'

        # --- Apply the movement ---
        self.moveHorizontal(level)
        self.moveVertical(level)

        self. checkEnemyCollisions(level.viruses)



    def selectAnimation(self):
        """Select the correct animation spritesheet based on state"""
        self.animationspeed = ANIMSPEED_HERO_DEFAULT
        if self.currentState == 'IDLE':
            self.animationspeed = ANIMSPEED_HERO_IDLE

        # Selects correct sprite sheet
        spriteSheet = self.spriteSheets[self.currentState]
        self.currentAnimation = spriteSheet.getSprites(flipped = not self.facingRight)


    def moveHorizontal(self, level):
        """Move hero horizontally and keep within window bounds"""
        self.rect.centerx += self.xDir * self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH

        self.xpos = self.rect.centerx



    def moveVertical(self, level):
        """Apply gravity and simulate ground"""

        self.yVel += self.gravity
        self.ypos += self.yVel


        # Simulate ground level
        ground_level = 400
        if self.ypos >= ground_level:
            self.ypos = ground_level
            self.yVel = 0
            self.isJumping = False
            if self.currentState == 'JUMP':
                self.currentState = 'IDLE'
    
    def die(self):
        if self.currentState != "DIE":
            self.currentState = "DIE"
            self.animationIndex = 0



    def checkEnemyCollisions(self,enemies):
        collidedSprites = pygame.sprite.spritecollide(self,enemies, False)
        for enemy in collidedSprites:
            if self.currentState == "ATTACK":
                if self.facingRight == True:
                    if enemy.rect.left < self.rect.right - 20:
                        enemy.die()

                else:
                    if enemy.rect.right > self.rect.left + 20:
                        enemy.die()

            else:
                if enemy.currentState != "DYING":
                    if self.rect.left < enemy.rect.left:
                        if self.rect.right > enemy.rect.left + 16:
                            self.die()
                    elif self.rect.right > enemy.rect.right:
                        if self.rect.left < enemy.rect.right - 16:
                            self.die()
