import numpy as np

class enemy:
    def __init__(self, name, position):
        self.name = name #a name to differenciate ennemies
        self. position = position #position in the map

    def update(self, current_state, neightboors):#Fonction qui décide comment bouger
        (x1, y1) = current_state[self.name] 
        (x2, y2) = current_state["Player"] 
        n1 = np.sqrt(x1*x1+y1*y1) 
        n2 = np.sqrt(x2*x2+y2*y2)
        angle = np.acos((x1*x2+y1*y2)/(n1*n2)) * 180 / np.pi
        dist = np.sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1))
        P = np.zeros(4)#Probabilities to go East, South, West, North in that order
        for i in range(len(neightboors)):
            if neightboors[i] == 0:#obstacle
                P[i] = 0
            else:
                P[i] = np.exp(0.33*self.W(angle)*self.T(dist))
        som = np.sum(P)
        A = P/som

        choice = np.random.choice([0, 1, 2, 3], p=A)[0]
        if choice == 0:#east
            current_state[self.name] = (x1, y1+1)
        elif choice == 1:#south
            current_state[self.name] = (x1+1, y1)
        elif choice == 2:#west
            current_state[self.name] = (x1, y1-1)
        elif choice == 3:#north
            current_state[self.name] = (x1-1, y1)
    
    def W(self, angle):
        #function from article
        return (180 - np.abs(angle)/180)
    
    def T(self, dist):
        #function from article
        if dist <= 4:
            return 15-dist
        elif dist <= 15:
            return 9-dist/2
        else:
            return 1
        
