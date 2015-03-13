__author__ = 'Austen Stewart, Joey Tarleton, and Robert Wilhelmsen'

# Import pygame and all of it's classes
import pygame, time, sys
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
        self.image = pygame.image.load('resources\protag.png') # Load player sprite image
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
        if self.rect.x >= 800 - self.image.get_width():
            self.rect.x = 800 - self.image.get_width()
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.y >= 600 - self.image.get_height():
            self.rect.y = 600 - self.image.get_height()
        if self.rect.y <= 0:
            self.rect.y = 0

        # Creates collision with enemies and deletes itself
        if pygame.sprite.spritecollide(player, enemySprites, True) or pygame.sprite.spritecollide(player, flyerSprites, True):
            self.kill()


class Bullet(pygame.sprite.Sprite): # Projectile Class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Initiate parent class
        self.image = pygame.image.load('resources\disc.png') # Set sprite image
        self.rect = self.image.get_rect() # Get rectangle from sprite image
        self.rect.x = -100
        self.rect.y = -100
        self.vel = -20 # Default velocity

    def update(self):
        self.rect.y += self.vel # Change bullet position
        # Check for collision between bullet and enemies
        if pygame.sprite.groupcollide(bulletSprites, enemySprites, True, True) or pygame.sprite.groupcollide(bulletSprites, flyerSprites, True, True): 
            player.headcount += 1 # Add to player score if enemy is hit

        # Set boundaries
        if self.rect.y <= -100:

            self.kill()

class enemyBullet(Bullet):
    def __init__(self, x, y):
        Bullet.__init__(self)
        self.image = pygame.image.load('resources\kha.png')
        self.vel = 10
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += self.vel

        # Check for collision between bullet and player
        if pygame.sprite.spritecollide(player, enemyBullets, True):
            player.kill()

        # Set boundaries
        if self.rect.y >= 650:
            self.kill()

class Enemy(pygame.sprite.Sprite): # Enemy super class
    def __init__(self, x, y):
        # Default values
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources\missile.png')
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
        self.image = pygame.image.load('resources/ufo.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = 3
        self.dy = 0

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources\hotshotgg.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 10
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
            hasDied = True

def main():

    global bullet
    global bulletSprites
    global allSprites
    global enemySprites
    global flyerSprites
    global score
    global bossSprite
    global enemyBullets
    global hasDied
    hasDied = False


    # Create an instance of the player at a certain position
    global player
    player = Player(400, 550)

    global enemy
    #Spawns enemies at random X values and offscreen by 50 on the Y axis
    enemy = [Enemy(randrange(0, 750, 1), randrange(-50, 50, 1))]

    flyer = [secretEnemy(randrange(-50, 50, 1), randrange(0, 300, 1))]

    # Add more initial enemies
    for x in range(0, 3):
        enemy.append(Enemy(randrange(0, 750, 1), randrange(-50, 50, 1)))

    # Bullet variable for later creation of Bullet object
    global bullet
    global flyerBullet

    # Create boss object
    global boss
    boss = Boss(325, 50)
    
    # Define sprite groups
    allSprites = pygame.sprite.RenderPlain()
    playerSprite = pygame.sprite.RenderPlain()
    bulletSprites = pygame.sprite.RenderPlain()
    enemySprites = pygame.sprite.RenderPlain()
    flyerSprites = pygame.sprite.RenderPlain()
    bossSprite = pygame.sprite.RenderPlain()
    enemyBullets = pygame.sprite.RenderPlain()

    # Add sprites to appropriate groups
    playerSprite.add(player)
    allSprites.add(player)
    enemySprites.add(enemy)
    allSprites.add(enemy)
    flyerSprites.add(flyer)
    allSprites.add(flyer)

    pVel = 20 # Set default player velocity to pass to Player constructor

    reloadspeed = 1000
    reloadEvent = pygame.USEREVENT + 1
    Reloaded = True

    bossReload = True
    bossrs = 750
    bossre = pygame.USEREVENT + 2
    
    # Set fonts
    scoreFont = pygame.font.SysFont("courier", 24)
    gameoverFont = pygame.font.SysFont("courier", 48)


    #Set Clock
    clock = pygame.time.Clock()
    keepGoing = True
    hasSpawned = False
    counter = 0


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
                elif event.key == pygame.K_SPACE:
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
                elif event.key == pygame.K_SPACE and not playerSprite.has(player):
                    gm = mainMenu()
                    gm.run()
                elif score >= scoreLimit and not bossSprite.has(boss):
                    gm = mainMenu()
                    gm.run()

            elif event.type == reloadEvent:
                for flyer in flyerSprites:
                    Reloaded = True
                    reloadspeed += randrange(0, 500, 100)
                    flyerBullet = enemyBullet(flyer.rect.x, flyer.rect.y)
                    enemyBullets.add(flyerBullet)
                    allSprites.add(flyerBullet)
                    pygame.time.set_timer(reloadEvent, 0)

            elif event.type == bossre:
                bossReload = True
                bossBullet1 = enemyBullet(boss.rect.x, boss.rect.y + 75)
                bossBullet2 = enemyBullet(boss.rect.x + 150, boss.rect.y + 75)
                enemyBullets.add(bossBullet1, bossBullet2)
                allSprites.add(bossBullet1, bossBullet2)
                pygame.time.set_timer(reloadEvent, 0)
                    

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

        scoreLimit = 3
        # Enemy counter for boss fight
        if score >= scoreLimit and not hasSpawned:
            bossSprite.add(boss)
            allSprites.add(boss)
            hasSpawned = True

        
        # Infinitely Spawn Enemies until player has died or boss has spawned
        if playerSprite.has(player) and not hasSpawned:
            if enemySprites.__len__() <= 10:
                newEnemy = Enemy(randrange(0, 750, 1), randrange(-150, -50, 1))
                enemySprites.add(newEnemy)
                allSprites.add(newEnemy)
            if flyerSprites.__len__() <= 3:
                newFlyer = secretEnemy(randrange(-150, -50, 1), randrange(0, 100, 1))
                flyerSprites.add(newFlyer)
                allSprites.add(newFlyer)

        if Reloaded and playerSprite.has(player): # Check if player is alive and enemies can shoot
            Reloaded = False # Expend shot
            pygame.time.set_timer(reloadEvent, reloadspeed) # Repeat

        if bossReload and playerSprite.has(player) and hasSpawned: # Repeat for when boss spawns
            bossReload = False
            pygame.time.set_timer(bossre, bossrs)

        # It's game over, man, game over!
        gameover = gameoverFont.render("Game Over", 1, (0, 0, 0)) # Print game over
        pressSpace = gameoverFont.render("Press Space To Return", 1, (0, 0, 0))
        win = gameoverFont.render("You Win", 1, (0, 0, 0))
        if not playerSprite.has(player): # Check if player has died
            enemySprites.empty()
            allSprites.empty() # Clear all sprites
            screen.blit(gameover, (250,300))
            screen.blit(pressSpace, (150, 500))
        if score >= scoreLimit and not bossSprite.has(boss): # Check if boss has died
            allSprites.empty()
            screen.blit(win, (250, 300))
            screen.blit(pressSpace, (150, 500))

        # Update the display
        pygame.display.update()
    pygame.quit()

class menuCursor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont('courier', 48)
        self.color = (0, 255, 0)
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

    def run(self):
        title = self.titleFont.render('Lembalo: Virus Breaker', 1, self.color)
        start = self.font.render('Start', 1, self.color)
        directions = self.directFont.render('Arrow Keys To Move. Space to Shoot. Good Luck.', 1, self.color)
        quitgame = self.font.render('Quit', 1, self.color)
        
        cursor = 0
        brace = menuCursor(50, 300)
        bracegroup = pygame.sprite.Group()
        bracegroup.add(brace)
        
        mainloop = True
        while mainloop:
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                elif event.type == KEYUP:
                    if event.key == K_DOWN and cursor == 0:
                        cursor = 1
                        brace.rect.y = 400
                    elif event.key == K_UP and cursor == 1:
                        cursor = 0
                        brace.rect.y = 300
                    elif event.key == K_SPACE or event.key == K_RETURN:
                        if cursor == 0:
                            mainloop = False
                            main()
                        elif cursor == 1:
                            mainloop = False
                    elif event.key == K_ESCAPE:
                        mainloop = False
                    

            screen.fill((0, 0, 0))
            screen.blit(title, (50, 50))
            screen.blit(start, (100, 300))
            screen.blit(quitgame, (100, 400))
            screen.blit(directions, (50, 550))
            bracegroup.draw(screen)
            bracegroup.update()
                
                
            pygame.display.update()
        pygame.quit()


if __name__ == '__main__':
    gm = mainMenu()
    gm.run()
