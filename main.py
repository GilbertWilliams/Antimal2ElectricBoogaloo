
__author__ = 'Austen Stewart, Joey Tarleton, and Robert Wilhelmsen'

# Import pygame and all of it's classes
import pygame, time, sys
from pygame.locals import *
from random import randrange

SCREENWIDTH = 800
SCREENHEIGHT = 600
CENTERX = SCREENWIDTH / 2
CENTERY = SCREENHEIGHT / 2

pygame.init() # Initiate pygame
pygame.display.set_caption("Space Shooter") # Set window title
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) # Set window dimensions
pygame.mouse.set_visible(0) # Cursor


#NOTE: All sprite images (with the exception of bullets) are 50x50

class Player(pygame.sprite.Sprite): # Player Class
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources/protag.png') # Load player sprite image
        self.rect = self.image.get_rect() # Make a rectangle using the image dimensions
        self.rect.x = x # Set top left x coordinate to passed value
        self.rect.y = y # Set top left y coordinate to passed value
        self.dx = 0 # Set default velocity on the x-axis
        self.dy = 0 # Set default velocity on the y-axis
        self.headcount = 0
        self.lives = 3

    def move(self, vel, ax):
        # Check if moving along the x- or y-axis based on passed ax value and change velocity according to vel value
        if ax == 'x':
            self.dx = vel
        elif ax =='y':
            self.dy = vel

    def takeLife(self):
        self.lives -= 1

    def update(self):
        # Change player position
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Set player boundaries
        if self.rect.x >= 800 - self.image.get_width():
            self.rect.x = 800 - self.image.get_width()
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.y >= 600 - self.image.get_height():
            self.rect.y = 600 - self.image.get_height()
        if self.rect.y <= 0:
            self.rect.y = 0

        # Creates collision with enemies and deletes itself
        if pygame.sprite.spritecollide(player, enemySprites, True) or pygame.sprite.spritecollide(player, flierSprites, True):
            if self.lives <= 0:
                self.kill()
            self.takeLife()


class Bullet(pygame.sprite.Sprite): # Projectile Class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Initiate parent class
        self.image = pygame.image.load('resources/disc.png') # Set sprite image
        self.rect = self.image.get_rect() # Get rectangle from sprite image
        self.rect.x = -100
        self.rect.y = -100
        self.vel = -30 # Default velocity

    def update(self):
        self.rect.y += self.vel # Change bullet position
        # Check for collision between bullet and enemies
        if pygame.sprite.groupcollide(bulletSprites, enemySprites, True, True) or pygame.sprite.groupcollide(bulletSprites, flierSprites, True, True):
            player.headcount += 1 # Add to player score if enemy is hit

        # Set boundaries
        if self.rect.y <= -50:

            self.kill()

class flierBullet(Bullet):
    def __init__(self, x, y):
        Bullet.__init__(self)
        self.image = pygame.image.load('resources/worm.png')
        self.rect = self.image.get_rect()
        self.vel = 10
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += self.vel

        # Check for collision between bullet and player
        if pygame.sprite.spritecollide(player, enemyBullets, True):
            player.takeLife()

        # Set boundaries
        if self.rect.y >= 650:
            self.kill()

class Enemy(pygame.sprite.Sprite): # Enemy super class
    def __init__(self, x, y):
        # Default values
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources/missile.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = 0
        self.dy = randrange(10, 17, 1)
        self.fire = 1
    
    def update(self):
        # Change enemy position
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Set enemy boundaries
        if self.rect.x > 800 or self.rect.x < -50:
            self.kill()
        if self.rect.y > 600 or self.rect.y < -50:
            self.kill()


class Flier(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self, x, y)
        self.image = pygame.image.load('resources/ufo.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = 6
        self.dy = 0

    def shoot(self):
        if self.fire == 1:
            ebullet = flierBullet(self.rect.x, self.rect.y)
            enemyBullets.add(ebullet)
            allSprites.add(ebullet)

    def update(self):
        # Change enemy position
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Set enemy boundaries
        if self.rect.x > 800 or self.rect.x < -50 or self.rect.y > 600 or self.rect.y < -50:
            self.kill()

        self.shoot()
        self.fire = randrange(0, 30, 1)

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources/hotshotgg.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 20
        self.dx = 6
        self.bosscounter = 0

    def update(self):
        self.rect.x += self.dx

        if self.rect.x <= 0:
            self.rect.x = 0
            self.dx = 6
        if self.rect.x >= 650:
            self.rect.x = 650
            self.dx = -6
        if pygame.sprite.spritecollide(boss, bulletSprites, True):
            self.health -= 1
        if self.health == 0:
            self.kill()
            bossDead = True

def levelTwo():
    pass

def levelOne():

    global bullet
    global bulletSprites
    global allSprites
    global enemySprites
    global flierSprites
    global score
    global bossSprite
    global enemyBullets
    global bossDead
    global bossSpawn
    global isAlive
    bossDead = False
    bossSpawn = False
    isAlive = True


    # Create an instance of the player at a certain position
    global player
    player = Player(400, 550)

    global enemy
    #Spawns enemies at random X values and offscreen by 50 on the Y axis
    enemy = [Enemy(randrange(0, 750, 10), randrange(-50, 50, 10))]

    flier = [Flier(randrange(-50, 50, 1), randrange(0, 150, 1))]

    # Add more initial enemies
    for x in range(0, 3):
        enemy.append(Enemy(randrange(0, 750, 1), randrange(-50, 50, 1)))

    # Bullet variable for later creation of Bullet object
    global bullet

    # Create boss object
    global boss

    # Define sprite groups
    allSprites = pygame.sprite.RenderPlain()
    playerSprite = pygame.sprite.RenderPlain()
    bulletSprites = pygame.sprite.RenderPlain()
    enemySprites = pygame.sprite.RenderPlain()
    flierSprites = pygame.sprite.RenderPlain()
    bossSprite = pygame.sprite.RenderPlain()
    enemyBullets = pygame.sprite.RenderPlain()

    # Add sprites to appropriate groups
    playerSprite.add(player)
    allSprites.add(player)
    enemySprites.add(enemy)
    allSprites.add(enemy)
    flierSprites.add(flier)
    allSprites.add(flier)

    pVel = 20 # Set default player velocity to pass to Player constructor

    # Create an event to spawn enemies
    enemySpawn = pygame.USEREVENT + 1
    pygame.time.set_timer(enemySpawn, 10)

    flierSpawn = pygame.USEREVENT + 2
    pygame.time.set_timer(flierSpawn, 30)

    # Create an event for the boss to shoot at a given interval
    bossre = pygame.USEREVENT + 3
    pygame.time.set_timer(bossre, 750)

    # Set fonts
    scoreFont = pygame.font.SysFont("courier", 24)
    gameoverFont = pygame.font.SysFont("courier", 48)


    #Set Clock
    clock = pygame.time.Clock()
    keepGoing = True

    #Main Loop
    while keepGoing:
        clock.tick(30)
        #input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
                elif event.key == pygame.K_SPACE and isAlive and not bossDead:
                    bullet = Bullet()
                    bulletSprites.add(bullet)
                    allSprites.add(bullet)
                    bullet.rect.x = player.rect.x
                    bullet.rect.y = player.rect.y

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
                elif event.key == pygame.K_ESCAPE:
                    keepGoing = False
                elif event.key == pygame.K_RETURN and (not isAlive or bossDead):
                    gm = mainMenu()
                    gm.run()

            elif event.type == enemySpawn and not bossSpawn and isAlive:
                newEnemy = Enemy(randrange(10, 750, 10), randrange(-150, -50, 1))
                enemySprites.add(newEnemy)
                allSprites.add(newEnemy)

            elif event.type == flierSpawn and not bossSpawn and isAlive:
                newflier = Flier(randrange(-150, -50, 1), randrange(10, 100, 1))
                flierSprites.add(newflier)
                allSprites.add(newflier)

            elif event.type == bossre and bossSpawn and isAlive:
                bossBullet1 = flierBullet(boss.rect.x, boss.rect.y + 75)
                bossBullet2 = flierBullet(boss.rect.x + 150, boss.rect.y + 75)
                enemyBullets.add(bossBullet1, bossBullet2)
                allSprites.add(bossBullet1, bossBullet2)


        # Create screen surface object and draw objects on it
        screen.fill((255,255,255))

        # Update and draw all sprites
        allSprites.update()
        allSprites.draw(screen)

        # Check if player is alive
        if not playerSprite.has(player):
            isAlive = False

        # Keep score
        score = player.headcount
        scoreString = str(score)
        scoreboard = scoreFont.render("score: " + scoreString, 1, (0, 0, 0))
        screen.blit(scoreboard, (25,25))

        scoreLimit = 50
        # Enemy counter for boss fight
        if score >= scoreLimit and not bossSpawn:
            boss = Boss(325, 50)
            bossSprite.add(boss)
            allSprites.add(boss)
            bossSpawn = True

        # It's game over, man, game over!
        gameover = gameoverFont.render("Game Over", 1, (0, 0, 0)) # Print game over
        gameoverCenterX = gameover.get_width() / 2
        gameoverCenterY = gameover.get_height() / 2
        pressSpace = gameoverFont.render("Press ENTER To Return", 1, (0, 0, 0))
        pressSpaceCenterX = pressSpace.get_width() / 2
        win = gameoverFont.render("You Win", 1, (0, 0, 0))
        winCenterX = win.get_width() / 2
        winCenterY = win.get_height() / 2
        if not isAlive: # Check if player has died
            enemySprites.empty()
            allSprites.empty() # Clear all sprites
            screen.blit(gameover, (CENTERX - gameoverCenterX, CENTERY - gameoverCenterY))
            screen.blit(pressSpace, (CENTERX - pressSpaceCenterX, CENTERY - gameoverCenterY + 100))
        if score >= scoreLimit and not bossSprite.has(boss): # Check if boss has died
            bossDead = True
            allSprites.empty()
            screen.blit(win, (CENTERX - winCenterX, CENTERY - winCenterY))
            screen.blit(pressSpace, (CENTERX - pressSpaceCenterX, CENTERY - winCenterY + 100))

        # Update the display
        pygame.display.update()

    pygame.quit()
    sys.exit()


#Class for the main menu
class menuCursor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont('courier', 48)
        self.color = (255, 255, 255)
        self.image = self.font.render('>', 1, self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class mainMenu():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('courier', 48)
        self.titleFont = pygame.font.SysFont('courier', 53)
        self.directFont = pygame.font.SysFont('courier', 24)
        self.color = (0, 255, 0)
        self.colorSelect = (255, 255, 255)

    def run(self):
        title = self.titleFont.render('Lembalo: Virus Breaker', 1, self.color)
        start = self.font.render('Start', 1, self.color)
        startSelect = self.font.render('Start', 1, self.colorSelect)
        directions = self.directFont.render('ARROW KEYS To Move. SPACE to Shoot. Good Luck.', 1, self.color)
        quitgame = self.font.render('Quit', 1, self.color)
        quitgameSelect = self.font.render('Quit', 1, self.colorSelect)

        titleCenterX = title.get_width() / 2
        titleCenterY = title.get_height() / 2
        startCenterX = start.get_width() / 2
        directionsCenterX = directions.get_width() / 2
        quitgameCenterX = quitgame.get_width() / 2

        cursor = 0
        brace = menuCursor(CENTERX - startCenterX - 50, CENTERY - titleCenterY + 100)
        bracegroup = pygame.sprite.Group()
        bracegroup.add(brace)
        
        mainloop = True
        while mainloop:
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                elif event.type == KEYUP:
                    if event.key == K_DOWN and cursor >= 0 and cursor <= 1:
                        cursor += 1
                        brace.rect.y += 100
                    elif event.key == K_UP and cursor >= 0 and cursor <= 1:
                        cursor -= 1
                        brace.rect.y -= 100
                    elif event.key == K_RETURN:
                        if cursor == 0:
                            levelOne()
                            mainloop = False
                        elif cursor == 1:
                            mainloop = False
                    elif event.key == K_ESCAPE:
                        mainloop = False
                    

            screen.fill((0, 0, 0))
            screen.blit(title, (CENTERX - titleCenterX, CENTERY - titleCenterY))
            if cursor == 0:
                screen.blit(startSelect, (CENTERX - startCenterX, CENTERY - titleCenterY + 100))
                screen.blit(quitgame, (CENTERX - quitgameCenterX, CENTERY - titleCenterY + 200))
            elif cursor == 1:
                screen.blit(start, (CENTERX - startCenterX, CENTERY - titleCenterY + 100))
                screen.blit(quitgameSelect, (CENTERX - quitgameCenterX, CENTERY - titleCenterY + 200))
            screen.blit(directions, (CENTERX - directionsCenterX, 550))
            bracegroup.draw(screen)
            bracegroup.update()
                
                
            pygame.display.update()
            
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    gm = mainMenu()
    gm.run()
    pygame.quit()
    sys.exit()
