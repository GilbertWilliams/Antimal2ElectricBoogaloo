__author__ = 'Austen Stewart, Joey Tarleton, and Robert Wilhelmsen'

# Import pygame and all of it's classes
import pygame, time
from pygame.locals import *
from random import randrange

pygame.init() # Initiate pygame
pygame.display.set_caption("Space Shooter") # Set window title
screen = pygame.display.set_mode((800, 600)) # Set window dimensions
pygame.mouse.set_visible(0) # Cursor

#NOTE: All sprite images (with the exception of bullets) are 50x50

class Player(pygame.sprite.Sprite): # Player Class
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources/theplanmanbob.png') # Load player sprite image
        self.rect = self.image.get_rect() # Make a rectangle using the image dimensions
        self.rect.x = x # Set top left x coordinate to passed value
        self.rect.y = y # Set top left y coordinate to passed value
        self.dx = 0 # Set default velocity on the x-axis
        self.dy = 0 # Set default velocity on the y-axis
        self.headcount = 0

    def move(self, vel, ax):
        # Check if moving along the x- or y-axis based on passed ax value and change velocity according to vel value
        if ax == 'x':
            self.dx = vel
        elif ax =='y':
            self.dy = vel

    def update(self):
        # Change player position
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Set player boundaries
        if self.rect.x >= 750:
            self.rect.x = 750
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.y >= 550:
            self.rect.y = 550
        if self.rect.y <= 0:
            self.rect.y = 0

        # Creates collision with enemies and deletes itself
        if pygame.sprite.spritecollide(player, enemySprites, True):
            self.kill()


class Bullet(pygame.sprite.Sprite): # Projectile Class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Initiate parent class
        self.image = pygame.image.load('resources/disc.png') # Set sprite image
        self.rect = self.image.get_rect() # Get rectangle from sprite image
        self.vel = -20 # Default velocity

    def update(self):
        self.rect.y += self.vel # Change bullet position
        if pygame.sprite.spritecollide(bullet, enemySprites, True): # Check for collision between bullet and enemies
            self.kill() #remove bullet if it collides with an enemy
            player.headcount += 1 # Add to player score if enemy is hit

            # Set boundaries
            if self.rect.y < -50:
                self.kill()

class enemyBullet(Bullet):
    def __init__(self):
        Bullet.__init__(self)
        self.image = pygame.image.load('resources/kha.png')
        self.vel = 20


class Enemy(pygame.sprite.Sprite): # Enemy super class
    '''
    This is the enemy super class. It is designed to hold all of the necessary variables for enemies that can be
    changed according to varying enemy types. Perhaps later this can be consolidated into a super class for both the
    Player and Enemy classes.
    '''

    def __init__(self, x, y):
        # Default values
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources\Soulface.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = 0
        self.dy = 7
    def update(self):
        # Change enemy position
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Set enemy boundaries
        if self.rect.x > 800 or self.rect.x < -50:
            self.kill()
        if self.rect.y > 600 or self.rect.y < -50:
            self.kill()

class secretEnemy(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self, x, y)
        self.image = pygame.image.load('resources\OC.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = 3
        self.dy = 0
            
        
        

'''
Current goals:
    Add X axis movements for enemies
    Enemy subclasses for different enemy types
    Create collisions between players and enemies
    Design the first level and corresponding boss fight
    Title Screen
'''

def main():

    global bullet
    global bullet_list
    global allSprites
    global enemySprites
    global score


    # Create an instance of the player at a certain position
    global player
    player = Player(400, 550)

    global enemy
    #Spawns enemies at random X values and offscreen by 50 on the Y axis
    enemy = [Enemy(randrange(0, 750, 1), -50), 
             Enemy(randrange(0, 750, 1), -50),
             Enemy(randrange(0, 750, 1), -50),
             secretEnemy(-50, randrange(0, 300, 1))]



    # Define sprite groups
    allSprites = pygame.sprite.RenderPlain()
    playerSprite = pygame.sprite.RenderPlain()
    bullet_list = pygame.sprite.RenderPlain()
    enemySprites = pygame.sprite.RenderPlain()

    # Add sprites to appropriate groups
    playerSprite.add(player)
    allSprites.add(player)
    enemySprites.add(enemy)
    allSprites.add(enemy)

    pVel = 20 # Set default player velocity to pass to Player constructor

    scoreFont = pygame.font.SysFont("courier", 24)

    gameoverFont = pygame.font.SysFont("comicsansms", 48)


    #Set Clock
    clock = pygame.time.Clock()
    keepGoing = True
    counter = 0


    #Main Loop
    while keepGoing:
        clock.tick(30)
        #input
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                keepGoing = False
            #Controls
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(-pVel, 'x')
                elif event.key == pygame.K_RIGHT:
                    player.move(pVel, 'x')
                elif event.key == pygame.K_UP:
                    player.move(-pVel, 'y')
                elif event.key == pygame.K_DOWN:
                    player.move(pVel, 'y')
                elif event.key == pygame.K_SPACE:
                    bullet = Bullet()
                    bullet.rect.x = player.rect.x
                    bullet.rect.y = player.rect.y
                    bullet_list.add(bullet)
                    allSprites.add(bullet)

            # Stop Moving
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.move(0, 'x')
                elif event.key == pygame.K_RIGHT:
                    player.move(0, 'x')
                elif event.key == pygame.K_UP:
                    player.move(0, 'y')
                elif event.key == pygame.K_DOWN:
                    player.move(0, 'y')



        # Create screen surface object and draw objects on it
        screen.fill((255,255,255))


        # Update and draw all sprites
        allSprites.update()
        allSprites.draw(screen)

        # Keep score
        score = player.headcount
        scoreString = str(score)
        scoreboard = scoreFont.render("score: " + scoreString, 1, (0, 0, 0))
        screen.blit(scoreboard, (25,25))

        # Enemy counter for boss fight

        if not playerSprite.has(player): # Check if player has died
            allSprites.empty() # Clear all sprites
            gameover = gameoverFont.render("Game Over", 1, (0, 0, 0)) # Print game over
            screen.blit(gameover, (300,300))

        # Update the display
        pygame.display.update()


if __name__ == '__main__':
    main() # Run the main class
