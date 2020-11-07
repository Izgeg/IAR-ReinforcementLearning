import pygame
import sys

#Les différentes cases
O = 0 #Obstacle
F = 1 #Food
L = 2 #Land
P = 3 #Player
E = 4 #Ennemy


#Les Sprites des cases A REMPLACER PAR DES SPRITES

OBSTACLE = pygame.image.load("images/obstacle.png")

FOOD = pygame.image.load("images/food.png")

LAND = pygame.image.load("images/grass.png")

PLAYER = pygame.image.load("images/player.png")

ENNEMY = pygame.image.load("images/vilain.png")
TileColor = { 
0 : OBSTACLE,
F : FOOD, 
L : LAND,
P : PLAYER,
E : ENNEMY }


#Création de la map A REMPLACER PAR UNE GENERATION ALEATOIRE

map1 = [[O, O, O, O, O, O, O, O, O, O, O, O],
        [O, L, L, L, L, L, L, L, L, L, L, O],
        [O, L, F, L, L, L, L, L, L, L, L, O],
        [O, L, L, L, L, L, L, L, L, E, L, O],
        [O, L, L, E, L, L, L, L, L, L, L, O],
        [O, L, L, L, L, F, L, L, L, L, L, O],
        [O, F, L, L, L, L, L, L, F, L, L, O],
        [O, L, L, E, L, L, L, L, L, E, L, O],
        [O, L, L, L, L, F, L, L, L, L, L, O],
        [O, L, L, L, L, L, L, L, L, L, L, O],
        [O, L, L, L, L, P, L, L, L, L, L, O],
        [O, O, O, O, O, O, O, O, O, O, O, O]]


#Map Sizes (Pour l'affichage)

TILESIZE = 40
MAPWIDTH = 12
MAPHEIGHT = 12


#CREATE DISPLAY (affichage)

pygame.init()
DISPLAY = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))

#User Interface (à ne pas garder normalement)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    #Drawing map
    for row in range(MAPHEIGHT):
        for col in range(MAPWIDTH):
            DISPLAY.blit(
                TileColor[map1[row][col]],
                (col*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))

    pygame.display.update()
