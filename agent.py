import numpy as np

class Agent:
    def __init__(self, name, position, current_map):
        self.name = name #a name to differenciate ennemies
        self.position = position #position in the map
        self.current_map = current_map#pour les obstacles seulement
        self.foodsensors = self.init_foodsensors()
        self.enemysensors = self.init_enemysensors()
        self.obstaclesensors = self.init_obstaclesensors()
        #print(self.enemysensors)
        self.energy = 40

    def update(self, current_state, neightboors):#Fonction qui décide comment bouger
        (x, y) = current_state[self.name]
        #print("Je suis", self.name, self.position,"\n Voici mes voisins", neightboors)
        self.update_sensors(current_state)
        P = np.zeros(4)
        for i in range(len(neightboors)):
            if neightboors[i] == (-1, -1):#obstacle or out of bounds
                P[i] = 0
            else:
                P[i] = 1

        ##print("Je suis ", self.name, "\n P", P)       
        som = np.sum(P)
        A = P/som
        ##print("Je suis ", self.name, "\n A", A)  
        choice = np.random.choice([0, 1, 2, 3], p=A)
        ##print(choice)
        if choice == 0:#east
            #print("Je vais à l'est")
            self.position = (x, y+1)
            current_state[self.name] = (x, y+1)
        elif choice == 1:#south
            #print("Je vais au sud")
            self.position = (x+1, y)
            current_state[self.name] = (x+1, y)
        elif choice == 2:#west
            #print("Je vais à l'ouest")
            self.position = (x, y-1)
            current_state[self.name] = (x, y-1)
        elif choice == 3:#north
            #print("Je vais au nord")
            self.position = (x-1, y)
            current_state[self.name] = (x-1, y)
        self.energy -= 1
        available_food = []
        for elem in current_state:
            if elem.startswith("F"):
                available_food.append(current_state[elem])
        if(current_state[self.name] in available_food):#si la case contient de la nourriture
            current_state = self.eat_food(current_state)
        print(self.energy)
        return current_state
        
    def toString(self):
        return "Je suis "+self.name+" et je me situe en (",self.position[0], self.position[1],")"
    
    def eat_food(self, current_state):
        (x,y) = current_state[self.name]
        self.energy += 15 #Value given by eating

        return {key:val for key, val in current_state.items() if(not (val == (x,y) and key.startswith("F")))}

        
    def update_sensors(self, current_state):
        self.update_foodsensors(current_state)
        self.update_enemysensors(current_state)
        self.update_obstaclesensors(self.current_map)

        self.update_obstaclesensors(self.current_map)

    def update_foodsensors(self, current_state):
        self.update_Xsensors(current_state, "food")
        self.update_Osensors(current_state, "food")
        self.update_Ysensors(current_state, "food")
    
    def update_enemysensors(self, current_state):
        self.update_Xsensors(current_state, "enemy")
        self.update_Osensors(current_state, "enemy")
    
    
    def update_obstaclesensors(self, current_map):
        obstaclesens = [(0,1),(1,0),(0,-1),(-1,0),(0,2),(1,1),(2,0),(1,-1),(0,-2),(-1,-1),(-2,0),(-1,1),(0,3),(1,2),(2,1),(3,0),(2,-1),(1,-2),(0,-3),(-1,-2),(-2,-1),(-3,0),(-2,1),(-1,2),(0,4),(1,3),(2,2),(3,1),(4,0),(3,-1),(2,-2),(1,-3),(0,-4),(-1,-3),(-2,-2),(-3,-1),(-4,0),(-3,1),(-2,2),(-1,3)]
        obstacles = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,19),(0,20),(0,21),(0,22),(0,23),(0,24),(1,0),(1,24),(2,0),(2,3),(2,4),(2,8),(2,9),(2,11),(2,12),(2,13),(2,15),(2,16),(2,20),(2,21),(2,24),(3,0),(3,2),(3,3),(3,4),(3,8),(3,9),(3,11),(3,13),(3,15),(3,16),(3,20),(3,21),(3,22),(3,24),(4,0),(4,2),(4,3),(4,4),(4,20),(4,21),(4,22),(4,24),(5,0),(5,24),(8,2),(8,3),(8,8),(8,9),(8,10),(8,11),(8,13),(8,14),(8,15),(8,16),(8,21),(8,22),(9,2),(9,3),(9,8),(9,9),(9,10),(9,14),(9,15),(9,16),(9,21),(9,22),(10,8),(10,9),(10,15),(10,16),(11,2),(11,3),(11,8),(11,16),(11,21),(11,22),(12,2),(12,12),(12,22),(13,2),(13,3),(13,8),(13,16),(13,21),(13,22),(14,8),(14,9),(14,15),(14,16),(15,2),(15,3),(15,8),(15,9),(15,10),(15,14),(15,15),(15,16),(15,21),(15,22),(16,2),(16,3),(16,8),(16,9),(16,10),(16,11),(16,13),(16,14),(16,15),(16,16),(16,21),(16,22),(19,0),(19,24),(20,0),(20,2),(20,3),(20,4),(20,20),(20,21),(20,22),(20,24),(21,0),(21,2),(21,3),(21,4),(21,8),(21,9),(21,11),(21,13),(21,15),(21,16),(21,20),(21,21),(21,22),(21,24),(22,0),(22,3),(22,4),(22,8),(22,9),(22,11),(22,12),(22,13),(22,15),(22,16),(22,20),(22,21),(22,24),(23,0),(23,24),(24,0),(24,1),(24,2),(24,3),(24,4),(24,5),(24,19),(24,20),(24,21),(24,22),(24,23),(24,24)]
        i = 0
        for sens in obstaclesens:
            if(sens[0]+self.position[0],sens[1]+self.position[1] in obstacles):
                self.obstaclesensors[i] = True
            else:
                self.obstaclesensors[i] = False
            i += 1    
    def update_Xsensors(self, current_state, typesens):
        i = 0
        if typesens == "food":
            foodX = [(0,1),(1,0),(0,-1),(-1,0),(0,2),(1,1),(2,0),(1,-1),(0,-2),(-1,-1),(-2,0),(-1,1)]
            available_food = []
            for elem in current_state:
                if elem.startswith("F"):
                    available_food.append(current_state[elem])
            for sens in foodX:
                if((sens[0]+self.position[0],sens[1]+self.position[1]) in available_food or (sens[0]+self.position[0] + 1,sens[1]+self.position[1]) in available_food or (sens[0]+self.position[0],sens[1]+self.position[1] + 1) in available_food or (sens[0]+self.position[0] - 1,sens[1]+self.position[1]) in available_food or (sens[0]+self.position[0],sens[1]+self.position[1] - 1) in available_food):
                    self.foodsensors[0][i] = True
                else: 
                    self.foodsensors[0][i] = False
                i+=1
        if typesens == "enemy":
            enemiesX = [(0,0),(0,1),(1,0),(0,-1),(-1,0),(0,2),(1,1),(2,0),(1,-1),(0,-2),(-1,-1),(-2,0),(-1,1)]
            available_enemy = []
            for elem in current_state:
                if elem.startswith("E"):
                    available_enemy.append(current_state[elem])
            for sens in enemiesX:
                if((sens[0]+self.position[0],sens[1]+self.position[1]) in available_enemy or (sens[0]+self.position[0] + 1,sens[1]+self.position[1]) in available_enemy or (sens[0]+self.position[0],sens[1]+self.position[1] + 1) in available_enemy or (sens[0]+self.position[0] - 1,sens[1]+self.position[1]) in available_enemy or (sens[0]+self.position[0],sens[1]+self.position[1] - 1) in available_enemy):
                    self.enemysensors[0][i] = True
                else: 
                    self.enemysensors[0][i] = False
                i+=1
    

    def update_Osensors(self, current_state, typesens):
        i = 0
        if typesens == "food":
            foodO = [(0,0),(0,4),(2,2),(4,0),(2,-2),(0,-4),(-2,-2),(-4,0),(-2,2),(0,6),(2,4),(4,2),(6,0),(4,-2),(2,-4),(0,-6),(-2,-4),(-4,-2),(-6,0),(-4,2),(-2,4)]
            available_food = []
            for elem in current_state:
                if elem.startswith("F"):
                    available_food.append(current_state[elem])
            for sens in foodO:
                if((sens[0]+self.position[0],sens[1]+self.position[1]) in available_food or (sens[0]+self.position[0] + 1, sens[1]+self.position[1]) in available_food or (sens[0]+self.position[0],sens[1]+self.position[1] + 1) in available_food or (sens[0]+self.position[0] - 1,sens[1]+self.position[1]) in available_food or (sens[0]+self.position[0],sens[1]+self.position[1] - 1) in available_food or (sens[0]+self.position[0],sens[1]+self.position[1]) in available_food or (sens[0]+self.position[0] - 1,sens[1]+self.position[1] - 1) in available_food or (sens[0]+self.position[0] + 1,sens[1]+self.position[1] + 1) in available_food or (sens[0]+self.position[0] - 1,sens[1]+self.position[1] + 1) in available_food or (sens[0]+self.position[0] + 1,sens[1]+self.position[1] - 1) in available_food):
                    self.foodsensors[1][i] = True
                else: 
                    self.foodsensors[1][i] = False
                i+=1
        if typesens == "enemy":
            enemiesO = [(0,0),(0,4),(2,2),(4,0),(2,-2),(0,-4),(-2,-2),(-4,0),(-2,2),(0,6),(2,4),(4,2),(6,0),(4,-2),(2,-4),(0,-6),(-2,-4),(-4,-2),(-6,0),(-4,2),(-2,4)]
            available_enemy = []
            for elem in current_state:
                if elem.startswith("E"):
                    available_enemy.append(current_state[elem])
            for sens in enemiesO:
                #print(i)
                if((sens[0]+self.position[0],sens[1]+self.position[1]) in available_enemy or (sens[0]+self.position[0] + 1,sens[1]+self.position[1]) in available_enemy or (sens[0]+self.position[0],sens[1]+self.position[1] + 1) in available_enemy or (sens[0]+self.position[0] - 1,sens[1]+self.position[1]) in available_enemy or (sens[0]+self.position[0],sens[1]+self.position[1] - 1) in available_enemy or (sens[0]+self.position[0],sens[1]+self.position[1]) in available_enemy or (sens[0]+self.position[0] - 1,sens[1]+self.position[1] - 1) in available_enemy or (sens[0]+self.position[0] + 1,sens[1]+self.position[1] + 1) in available_enemy or (sens[0]+self.position[0] - 1,sens[1]+self.position[1] + 1) in available_enemy or (sens[0]+self.position[0] + 1,sens[1]+self.position[1] - 1) in available_enemy):
                    self.enemysensors[1][i] = True
                else: 
                    self.enemysensors[1][i] = False
                    
                i+=1
    def update_Ysensors(self, current_state, typesens):
        i = 0
        if typesens == "food":
            foodY = [(0,0),(0,10),(2,8),(4,6),(6,4),(8,2),(10,0),(8,-2),(6,-4),(4,-6),(2,-8),(0,-10),(-2,-8),(-4,-6),(-6,-4),(-8,-2),(-10,0),(-8,2),(-6,4),(-4,6),(-2,8)]
            available_food = []
            for elem in current_state:
                if elem.startswith("F"):
                    available_food.append(current_state[elem])
            for sens in foodY:
                if((sens[0]+self.position[0],sens[1]+self.position[1]) in available_food or (sens[0]+self.position[0] + 1,sens[1]+self.position[1]) in available_food or (sens[0]+self.position[0],sens[1]+self.position[1] + 1) in available_food or (sens[0]+self.position[0] - 1,sens[1]+self.position[1]) in available_food or (sens[0]+self.position[0],sens[1]+self.position[1] - 1) in available_food or (sens[0]+self.position[0],sens[1]+self.position[1]) in available_food or (sens[0]+self.position[0] - 1,sens[1]+self.position[1] - 1) in available_food or (sens[0]+self.position[0] + 1,sens[1]+self.position[1] + 1) in available_food or (sens[0]+self.position[0] - 1,sens[1]+self.position[1] + 1) in available_food or (sens[0]+self.position[0] + 1,sens[1]+self.position[1] - 1) in available_food or (sens[0]+self.position[0] + 2,sens[1]+self.position[1]) in available_food or (sens[0]+self.position[0],sens[1]+self.position[1] + 2) in available_food or (sens[0]+self.position[0] - 2,sens[1]+self.position[1]) in available_food or (sens[0]+self.position[0],sens[1]+self.position[1] - 2) in available_food):
                    self.foodsensors[2][i] = True
                else:
                    self.foodsensors[2][i] = False
                i+=1
    def init_foodsensors(self):
        """
        Three types of sensors : 
        - X : X is activated when there's an object in one of the five nearest tiles 
        food : (0,2),(2,0),(0,-2),(-2,0),(1,1),(-1,-1),(-1,1),(1,-1),(1,0),(0,1),(-1,0),(0,-1) 
        enemies : (0,2),(2,0),(0,-2),(-2,0),(1,1),(-1,-1),(-1,1),(1,-1),(1,0),(0,1),(-1,0),(0,-1)  
        - O : O is activated when there's an object in one of the nine closest tiles
        food : (0,4),(4,0),(0,-4),(-4,0),(2,2),(-2,-2),(-2,2),(2,-2),(6,0),(0,6),(0,-6),(-6,0),(4,2),(2,4),(-4,-2),(-2,-4),(-4,2),(-2,4),(2,-4),(4,-2)
        enemies : (0,4),(4,0),(0,-4),(-4,0),(2,2),(-2,-2),(-2,2),(2,-2),(6,0),(0,6),(0,-6),(-6,0),(4,2),(2,4),(-4,-2),(-2,-4),(-4,2),(-2,4),(2,-4),(4,-2) 
        - Y : Y is activated when there's an object in on of the thirteen closest tiles
        food : (10,0),(-10,0),(0,10),(0,-10),(-8,2),(8,-2),(-8,-2),(8,2),(-2,8),(2,-8),(-2,-8),(2,8),(6,4),(-6,-4),(-6,4),(6,-4),(4,6),(-4,-6),(-4,6),(4,-6)
        
        there's also the obstacle sensor which activates only on the tile it's on, we'll note it s
        obstacles : (0,2),(2,0),(0,-2),(-2,0),(1,1),(-1,-1),(-1,1),(1,-1),(1,0),(0,1),(-1,0),(0,-1),(3,0),(0,3),(-3,0),(0,-3),(2,1),(1,2),(-2,-1),(-1,-2),(-2,1),(-1,2),(1,-2),(2,-1),(0,4),(4,0),(0,-4),(-4,0),(2,2),(1,3),(3,1),(-2,2),(-1,3),(-3,1),(-2,-2),(-1,-3),(-3,-1),(2,-2),(1,-3),(3,-1)
        the dictionnaries contain the position of the sensors (relative to the agent always supposed to be in (0,0)) and a boolean saying if the sensor catches something or not
        """
        foodX = [(0,1),(1,0),(0,-1),(-1,0),(0,2),(1,1),(2,0),(1,-1),(0,-2),(-1,-1),(-2,0),(-1,1)]
        foodO = [(0,4),(2,2),(4,0),(2,-2),(0,-4),(-2,-2),(-4,0),(-2,2),(0,6),(2,4),(4,2),(6,0),(4,-2),(2,-4),(0,-6),(-2,-4),(-4,-2),(-6,0),(-4,2),(-2,4)]
        foodY = [(0,10),(2,8),(4,6),(6,4),(8,2),(10,0),(8,-2),(6,-4),(4,-6),(2,-8),(0,-10),(-2,-8),(-4,-6),(-6,-4),(-8,-2),(-10,0),(-8,2),(-6,4),(-4,6),(-2,8)]
        
        foodsensorX = [False for i in range(len(foodX))]
        foodsensorO = [False for i in range(len(foodO))]
        foodsensorY = [False for i in range(len(foodY))]

        foodsensors = [foodsensorX, foodsensorO, foodsensorY]
        
        return foodsensors
        
    def init_enemysensors(self):
        """
        Three types of sensors : 
        - X : X is activated when there's an object in one of the five nearest tiles 
        food : (0,2),(2,0),(0,-2),(-2,0),(1,1),(-1,-1),(-1,1),(1,-1),(1,0),(0,1),(-1,0),(0,-1) 
        enemies : (0,2),(2,0),(0,-2),(-2,0),(1,1),(-1,-1),(-1,1),(1,-1),(1,0),(0,1),(-1,0),(0,-1)  
        - O : O is activated when there's an object in one of the nine closest tiles
        food : (0,4),(4,0),(0,-4),(-4,0),(2,2),(-2,-2),(-2,2),(2,-2),(6,0),(0,6),(0,-6),(-6,0),(4,2),(2,4),(-4,-2),(-2,-4),(-4,2),(-2,4),(2,-4),(4,-2)
        enemies : (0,4),(4,0),(0,-4),(-4,0),(2,2),(-2,-2),(-2,2),(2,-2),(6,0),(0,6),(0,-6),(-6,0),(4,2),(2,4),(-4,-2),(-2,-4),(-4,2),(-2,4),(2,-4),(4,-2) 
        - Y : Y is activated when there's an object in on of the thirteen closest tiles
        food : (10,0),(-10,0),(0,10),(0,-10),(-8,2),(8,-2),(-8,-2),(8,2),(-2,8),(2,-8),(-2,-8),(2,8),(6,4),(-6,-4),(-6,4),(6,-4),(4,6),(-4,-6),(-4,6),(4,-6)
        
        there's also the obstacle sensor which activates only on the tile it's on, we'll note it s
        obstacles : (0,2),(2,0),(0,-2),(-2,0),(1,1),(-1,-1),(-1,1),(1,-1),(1,0),(0,1),(-1,0),(0,-1),(3,0),(0,3),(-3,0),(0,-3),(2,1),(1,2),(-2,-1),(-1,-2),(-2,1),(-1,2),(1,-2),(2,-1),(0,4),(4,0),(0,-4),(-4,0),(2,2),(1,3),(3,1),(-2,2),(-1,3),(-3,1),(-2,-2),(-1,-3),(-3,-1),(2,-2),(1,-3),(3,-1)
        the dictionnaries contain the position of the sensors (relative to the agent always supposed to be in (0,0)) and a boolean saying if the sensor catches something or not
        """
        
        enemiesX = [(0,1),(1,0),(0,-1),(-1,0),(0,2),(1,1),(2,0),(1,-1),(0,-2),(-1,-1),(-2,0),(-1,1)]
        enemiesO = [(0,4),(2,2),(4,0),(2,-2),(0,-4),(-2,-2),(-4,0),(-2,2),(0,6),(2,4),(4,2),(6,0),(4,-2),(2,-4),(0,-6),(-2,-4),(-4,-2),(-6,0),(-4,2),(-2,4)]
        
        enemysensorX = [False for i in range(len(enemiesX))]
        enemysensorO = [False for i in range(len(enemiesO))]
    
        enemysensors = [enemysensorX, enemysensorO]
        
        
        return enemysensors
    def read_sensor_orientation90(self, sens, nature):
        ret = []
        if sens == "obstacle":
            liste = [1,2,3,0,6,7,8,9,10,11,4,5,15,16,17,18,19,20,21,22,23,12,13,14,28,29,30,31,32,33,34,35,36,37,38,39,24,25,26,27]
        elif sens == "X":
            liste = [1,2,3,0,6,7,8,9,10,11,4,5]
        elif sens == "O":
            liste = [2,3,4,5,6,7,0,1,11,12,13,14,15,16,17,18,19,8,9,10]
        elif sens == "Y":
            liste = [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,0,1,2,3,4]
        for i in liste:
                ret.append(sens[i]) 
        return ret
    def init_obstaclesensors(self):
        """
        Three types of sensors : 
        - X : X is activated when there's an object in one of the five nearest tiles 
        food : (0,2),(2,0),(0,-2),(-2,0),(1,1),(-1,-1),(-1,1),(1,-1),(1,0),(0,1),(-1,0),(0,-1) 
        enemies : (0,2),(2,0),(0,-2),(-2,0),(1,1),(-1,-1),(-1,1),(1,-1),(1,0),(0,1),(-1,0),(0,-1)  
        - O : O is activated when there's an object in one of the nine closest tiles
        food : (0,4),(4,0),(0,-4),(-4,0),(2,2),(-2,-2),(-2,2),(2,-2),(6,0),(0,6),(0,-6),(-6,0),(4,2),(2,4),(-4,-2),(-2,-4),(-4,2),(-2,4),(2,-4),(4,-2)
        enemies : (0,4),(4,0),(0,-4),(-4,0),(2,2),(-2,-2),(-2,2),(2,-2),(6,0),(0,6),(0,-6),(-6,0),(4,2),(2,4),(-4,-2),(-2,-4),(-4,2),(-2,4),(2,-4),(4,-2) 
        - Y : Y is activated when there's an object in on of the thirteen closest tiles
        food : (10,0),(-10,0),(0,10),(0,-10),(-8,2),(8,-2),(-8,-2),(8,2),(-2,8),(2,-8),(-2,-8),(2,8),(6,4),(-6,-4),(-6,4),(6,-4),(4,6),(-4,-6),(-4,6),(4,-6)
        
        there's also the obstacle sensor which activates only on the tile it's on, we'll note it s
        obstacles : (0,2),(2,0),(0,-2),(-2,0),(1,1),(-1,-1),(-1,1),(1,-1),(1,0),(0,1),(-1,0),(0,-1),(3,0),(0,3),(-3,0),(0,-3),(2,1),(1,2),(-2,-1),(-1,-2),(-2,1),(-1,2),(1,-2),(2,-1),(0,4),(4,0),(0,-4),(-4,0),(2,2),(1,3),(3,1),(-2,2),(-1,3),(-3,1),(-2,-2),(-1,-3),(-3,-1),(2,-2),(1,-3),(3,-1)
        the dictionnaries contain the position of the sensors (relative to the agent always supposed to be in (0,0)) and a boolean saying if the sensor catches something or not
        """

        obstacle = [(0,1),(1,0),(0,-1),(-1,0),(0,2),(1,1),(2,0),(1,-1),(0,-2),(-1,-1),(-2,0),(-1,1),(0,3),(1,2),(2,1),(3,0),(2,-1),(1,-2),(0,-3),(-1,-2),(-2,-1),(-3,0),(-2,1),(-1,2),(0,4),(1,3),(2,2),(3,1),(4,0),(3,-1),(2,-2),(1,-3),(0,-4),(-1,-3),(-2,-2),(-3,-1),(-4,0),(-3,1),(-2,2),(-1,3)]#

        obstaclesensors = [False for i in range(len(obstacle))]
        return obstaclesensors

        
        