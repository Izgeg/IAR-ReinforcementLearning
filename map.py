import sys
import pygame
import enemy
import agent
import time
import copy
#import random
#Les différentes cases
O = 0 #Obstacle
F = 1 #Food
L = 2 #Land
P = 3 #Player
E = 4 #Ennemy

elems = [O, F, L, P, E]
#Les Sprites des cases A REMPLACER PAR DES SPRITES

OBSTACLE = pygame.image.load("C://Users//Nadym\Downloads\IAR\IAR-ReinforcementLearning-main\images\obstacle.png")

FOOD = pygame.image.load("C://Users//Nadym\Downloads\IAR\IAR-ReinforcementLearning-main\images//food.png")

LAND = pygame.image.load("C://Users//Nadym\Downloads\IAR\IAR-ReinforcementLearning-main\images//grass.png")

PLAYER = pygame.image.load("C://Users//Nadym\Downloads\IAR\IAR-ReinforcementLearning-main\images//player.png")

ENNEMY = pygame.image.load("C://Users//Nadym\Downloads\IAR\IAR-ReinforcementLearning-main\images//vilain.png")

TileColor = {
O : OBSTACLE,
F : FOOD,
L : LAND,
P : PLAYER,
E : ENNEMY
}

#Map Sizes (Pour l'affichage)
TILESIZE = 25
MAPWIDTH = 25
MAPHEIGHT = 25

#Création de la map de l'article

blank_map = [
[O, O, O, O, O, O, L, L, L, L, L, L, L, L, L, L, L, L, L, O, O, O, O, O, O],
[O, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, O],
[O, L, L, O, O, L, L, L, O, O, L, O, O, O, L, O, O, L, L, L, O, O, L, L, O],
[O, L, O, O, O, L, L, L, O, O, L, O, L, O, L, O, O, L, L, L, O, O, O, L, O],
[O, L, O, O, O, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, O, O, O, L, O],
[O, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, O],
[L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L],
[L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L],
[L, L, O, O, L, L, L, L, O, O, O, O, L, O, O, O, O, L, L, L, L, O, O, L, L],
[L, L, O, O, L, L, L, L, O, O, O, L, L, L, O, O, O, L, L, L, L, O, O, L, L],
[L, L, L, L, L, L, L, L, O, O, L, L, L, L, L, O, O, L, L, L, L, L, L, L, L],
[L, L, O, O, L, L, L, L, O, L, L, L, L, L, L, L, O, L, L, L, L, O, O, L, L],
[L, L, O, L, L, L, L, L, L, L, L, L, O, L, L, L, L, L, L, L, L, L, O, L, L],
[L, L, O, O, L, L, L, L, O, L, L, L, L, L, L, L, O, L, L, L, L, O, O, L, L],
[L, L, L, L, L, L, L, L, O, O, L, L, L, L, L, O, O, L, L, L, L, L, L, L, L],
[L, L, O, O, L, L, L, L, O, O, O, L, L, L, O, O, O, L, L, L, L, O, O, L, L],
[L, L, O, O, L, L, L, L, O, O, O, O, L, O, O, O, O, L, L, L, L, O, O, L, L],
[L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L],
[L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L],
[O, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, O],
[O, L, O, O, O, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, O, O, O, L, O],
[O, L, O, O, O, L, L, L, O, O, L, O, L, O, L, O, O, L, L, L, O, O, O, L, O],
[O, L, L, O, O, L, L, L, O, O, L, O, O, O, L, O, O, L, L, L, O, O, L, L, O],
[O, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, L, O],
[O, O, O, O, O, O, L, L, L, L, L, L, L, L, L, L, L, L, L, O, O, O, O, O, O]
]
map_article = [
[O, O, O, O, O, O, L, L, L, L, L, L, L, L, L, L, L, L, L, O, O, O, O, O, O],
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
[O, O, O, O, O, O, L, L, L, L, L, L, L, L, L, L, L, L, L, O, O, O, O, O, O]
]

#print(map_article)

current_state = { 
"Food1" : (4, 9),
"Food2" : (4, 19),
"Food3" : (5, 20),
"Food4" : (10, 14),
"Food5" : (10, 17),
"Food6" : (10, 22),
"Food7" : (11, 0),
"Food8" : (13, 0),
"Food9" : (13, 14),
"Food10": (14, 2),
"Food11": (14, 4),
"Food12": (14, 12),
"Food13": (14, 17),
"Food14": (20, 5),
"Food15": (23, 1),
"Food16": (23, 22),
"Food17": (23, 23),
"Player" : (18, 12),
"Enemy1" : (1,12),
"Enemy2" : (6, 6),
"Enemy3" : (6, 12),
"Enemy4" : (6, 18)
}



def map_fusion(current_state, blank_map):
    #Fonction qui vise à générer une nouvelle map qui est remplie des nouvelles choses qui sont arrivés pendant ce tour
    map_vide = copy.deepcopy(blank_map)
    for elem in current_state:
        if elem.startswith("F"):
            map_vide[current_state[elem][0]][current_state[elem][1]] = F
        elif elem.startswith("E"):
            map_vide[current_state[elem][0]][current_state[elem][1]] = E
        elif elem.startswith("P"):
            map_vide[current_state[elem][0]][current_state[elem][1]] = P
    return map_vide

def neightboors(x,y, blank_map):
    ret = []
    if y < 24 and blank_map[x][y+1] != O :
        ret.append((x,y+1))#east
    else:
        ret.append((-1,-1))
    if x < 24 and blank_map[x+1][y] != O :
        ret.append((x+1,y))#south
    else:
        ret.append((-1, -1))
    if y > 0 and blank_map[x][y-1] != O :
        ret.append((x,y-1))#west
    else:
        ret.append((-1, -1))
    if x > 0 and blank_map[x-1][y] != O :
        ret.append((x-1,y))#north
    else:
        ret.append((-1, -1))

    return ret

def update_states(current_state, enemies, player, blank_map, compteur):
    if(compteur%5 != 0):
        for enemy in enemies:
            current_state = enemy.update(current_state, neightboors(enemy.position[0], enemy.position[1], blank_map))
    current_state = player.update(current_state, neightboors(player.position[0], player.position[1], blank_map))
    return current_state
pygame.init()
DISPLAY = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))

#Creation des ennemis
enemies = []
for elem in current_state:
    if elem.startswith("E"):
        enemies.append(enemy.Enemy(elem, (current_state[elem][0], current_state[elem][1])))
player = agent.Agent("Player", (current_state["Player"][0], current_state["Player"][1]), map_article)

#print([enemy.toString() for enemy in enemies])
#for enemy in enemies:
#    current_state = enemy.update(current_state, neightboors(enemy.position[0], enemy.position[1]))

#print([enemy.toString() for enemy in enemies])

#CREATE DISPLAY (affichage)
def update_disp(current_map):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    #Drawing map
    for row in range(MAPHEIGHT):
        for col in range(MAPWIDTH):
             
            DISPLAY.blit(
                TileColor[current_map[row][col]],
                (col*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))

#La plupart des trucs ici sont à commenter pour pour l'entrainement
compteur = 0
while True:
    
    update_disp(map_fusion(current_state, blank_map))     
    pygame.display.update()
    current_state = update_states(current_state, enemies, player, blank_map, compteur)
    time.sleep(0.01)
    compteur += 1
