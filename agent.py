import numpy as np

class Agent:
    def __init__(self, name, position):
        self.name = name #a name to differenciate ennemies
        self.position = position #position in the map

    def update(self, current_state, neightboors):#Fonction qui décide comment bouger
        (x, y) = current_state[self.name]
        print("Je suis", self.name, self.position,"\n Voici mes voisins", neightboors)
        P = np.zeros(4)
        for i in range(len(neightboors)):
            if neightboors[i] == (-1, -1):#obstacle or out of bounds
                P[i] = 0
            else:
                P[i] = 1

        #print("Je suis ", self.name, "\n P", P)       
        som = np.sum(P)
        A = P/som
        #print("Je suis ", self.name, "\n A", A)  
        choice = np.random.choice([0, 1, 2, 3], p=A)
        #print(choice)
        if choice == 0:#east
            print("Je vais à l'est")
            self.position = (x, y+1)
            current_state[self.name] = (x, y+1)
        elif choice == 1:#south
            print("Je vais au sud")
            self.position = (x+1, y)
            current_state[self.name] = (x+1, y)
        elif choice == 2:#west
            print("Je vais à l'ouest")
            self.position = (x, y-1)
            current_state[self.name] = (x, y-1)
        elif choice == 3:#north
            print("Je vais au nord")
            self.position = (x-1, y)
            current_state[self.name] = (x-1, y)
        return current_state
    
        
    def toString(self):
        return "Je suis "+self.name+" et je me situe en (",self.position[0], self.position[1],")"