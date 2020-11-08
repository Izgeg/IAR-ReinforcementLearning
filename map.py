import sys
import pygame
#import random
#Les différentes cases
O = 0 #Obstacle
F = 1 #Food
L = 2 #Land
P = 3 #Player
E = 4 #Ennemy

elems = [O, F, L, P, E]
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

# MAP SIZES
TILESIZE = 25
MAPWIDTH = 25
MAPHEIGHT = 25

#Création de la map A REMPLACER PAR UNE GENERATION ALEATOIRE

map_artcile = [[O, O, O, O, O, O, L, L, L, L, L, L, L, L, L, L, L, L, L, O, O, O, O, O, O],
[O, L, L, L, L, L, L, L, L, L, L, L, E, L, L, L, L, L, L, L, L, L, L, L, O],
[O, L, L, O, O, L, L, L, O, O, L, O, O, O, L, O, O, L, L, L, O, O, L, L, O],
[O, L, O, O, O, L, L, L, O, O, L, O, L, O, L, O, O, L, L, L, O, O, O, L, O],
[O, L, O, O, O, L, L, L, L, F, L, L, L, L, L, L, L, L, L, F, O, O, O, L, O],
[O, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, F, L, L, L, O],
[L, L, L, L, L, L, E, L, L, L, L, L, E, L, L, L, L, L, E, L, L, L, L, L, L],
[L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L],
[L, L, O, O, L, L, L, L, O, O, O, O, L, O, O, O, O, L, L, L, L, O, O, L, L],
[L, L, O, O, L, L, L, L, O, O, O, L, L, L, O, O, O, L, L, L, L, O, O, L, L],
[L, L, L, L, L, L, L, L, O, O, L, L, L, L, F, O, O, F, L, L, L, L, F, L, L],
[F, L, O, O, L, L, L, L, O, L, L, L, L, L, L, L, O, L, L, L, L, O, O, L, L],
[L, L, O, L, L, L, L, L, L, L, L, L, O, L, L, L, L, L, L, L, L, L, O, L, L],
[F, L, O, O, L, L, L, L, O, L, L, L, L, L, F, L, O, L, L, L, L, O, O, L, L],
[L, L, F, L, F, L, L, L, O, O, L, L, F, L, L, O, O, F, L, L, L, L, L, L, L],
[L, L, O, O, L, L, L, L, O, O, O, L, L, L, O, O, O, L, L, L, L, O, O, L, L],
[L, L, O, O, L, L, L, L, O, O, O, O, L, O, O, O, O, L, L, L, L, O, O, L, L],
[L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L],
[L, L, L, L, L, L, L, L, L, L, L, L, P, L, L, L, L, L, L, L, L, L, L, L, L],
[O, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, O],
[O, L, O, O, O, F, L, L, L, L, L, L, L, L, L, L, L, L, L, L, O, O, O, L, O],
[O, L, O, O, O, L, L, L, O, O, L, O, L, O, L, O, O, L, L, L, O, O, O, L, O],
[O, L, L, O, O, L, L, L, O, O, L, O, O, O, L, O, O, L, L, L, O, O, L, L, O],
[O, F, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, F, F, O],
[O, O, O, O, O, O, L, L, L, L, L, L, L, L, L, L, L, L, L, O, O, O, O, O, O]]

print(map_artcile[1][12])
"""
RANDOM MAP

for i in range(MAPWIDTH):
    map1.append([])
    for j in range(MAPHEIGHT):
        map1[i].append(random.choice(elems))
"""

#Map Sizes (Pour l'affichage)

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
                TileColor[map_artcile[row][col]],
                (col*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))

    pygame.display.update()