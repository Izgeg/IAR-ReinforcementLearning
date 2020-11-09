import numpy as np

class Enemy:
    def __init__(self, name, position):
        self.name = name #a name to differenciate ennemies
        self.position = position #position in the map

    def update(self, current_state, neightboors):#Fonction qui décide comment bouger
        (x1, y1) = current_state[self.name] 
        (x2, y2) = current_state["Player"] 
        """
        n1 = np.sqrt(x1*x1+y1*y1)
        n2 = np.sqrt(x2*x2+y2*y2)
        angle = np.arccos((x1*x2+y1*y2)/(n1*n2)) * 180 / np.pi
        dist = np.sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1))
        """
        #print("Je suis ", self.name, "\n Angle :", angle, "\nDistance :", dist)
        P = np.zeros(4)#Probabilities to go East, South, West, North in that order
        print("Je suis", self.name, self.position,"\n Voici mes voisins", neightboors)
        for i in range(len(neightboors)):
            if neightboors[i] == (-1, -1):#obstacle or out of bounds
                P[i] = 0
            else:
                (x3, y3) = neightboors[i]
                u = (x3-x1, y3-y1)#vecteur entre la position de l'ennemi et sa position actuelle
                v = (x2-x1, y2-y1)#vecteur entre l'ennemi et le player
                uv = u[0]*v[0] + u[1]*u[1]
                normu = u[0]*u[0] + u[1]*u[1]
                normv = v[0]*v[0] + v[1]*v[1]
                if normu == 0 or normv == 0:
                    angle = 0
                else:
                    angle = np.arccos(uv/(normu*normv))
                dist = abs(x1-x3) + abs(y1-y3)
                P[i] = np.exp(0.33*self.W(angle)*self.T(dist))

        print("Je suis ", self.name, "\n P", P)       
        som = np.sum(P)
        A = P/som
        print("Je suis ", self.name, "\n A", A)  
        choice = np.random.choice([0, 1, 2, 3], p=A)
        #print(choice)
        if choice == 0:#east
            print("Je vais à l'est")
            self.position = (x1, y1+1)
            current_state[self.name] = (x1, y1+1)
        elif choice == 1:#south
            print("Je vais au sud")
            self.position = (x1+1, y1)
            current_state[self.name] = (x1+1, y1)
        elif choice == 2:#west
            print("Je vais à l'ouest")
            self.position = (x1, y1-1)
            current_state[self.name] = (x1, y1-1)
        elif choice == 3:#north
            print("Je vais au nord")
            self.position = (x1-1, y1)
            current_state[self.name] = (x1-1, y1)
        return current_state
    
    def W(self, angle):
        #function from article
        return (180 - np.abs(angle))/180
    
    def T(self, dist):
        #function from article
        if dist <= 4:
            return 15-dist
        elif dist <= 15:
            return 9-dist/2
        else:
            return 1
        
    def toString(self):
        return "Je suis "+self.name+" et je me situe en (",self.position[0], self.position[1],")"