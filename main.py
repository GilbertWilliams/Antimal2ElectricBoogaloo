__author__ = 'as117001364'
import pygame
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Space Shooter")
screen = pygame.display.set_mode((800, 600))
pygame.mouse.set_visible(0)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources/hotshotgg.png')
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0

    def moveX(self, vel):
        self.dx = vel

    def moveY(self, vel):
        self.dy = vel

    def update(self):
        self.x += self.dx
        self.y += self.dy

        self.rect.x = self.x
        self.rect.y = self.y



def main():
    global player
    player = Player(50, 50)

    playerSprite = pygame.sprite.RenderPlain()
    playerSprite.add(player)

    #Set Clock
    clock = pygame.time.Clock()
    keepGoing = True
    counter = 0

    #Main Loop
    while keepGoing:
        clock.tick(30)
        #input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.moveX(-2)
                elif event.key == pygame.K_RIGHT:
                    player.moveX(2)
                elif event.key == pygame.K_UP:
                    player.moveY(-2)
                elif event.key == pygame.K_DOWN:
                    player.moveY(2)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.moveX(0)
                elif event.key == pygame.K_RIGHT:
                    player.moveX(0)
                elif event.key == pygame.K_UP:
                    player.moveY(0)
                elif event.key == pygame.K_DOWN:
                    player.moveY(0)
        screen.fill((255,255,255))
        playerSprite.update()
        playerSprite.draw(screen)
        pygame.display.update()

if __name__ == '__main__':
    main()