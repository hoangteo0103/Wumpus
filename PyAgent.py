from Action import *
class Agent:
    def loadFile(self, input_file):
        with open(input_file, 'r') as file:
            lines = file.read().splitlines()

        # Extract map size and map data
        map_size = int(lines[0])
        map_data = lines[1:]

        # Initialize the map with empty rooms
        game_map = [['-' for _ in range(map_size)] for _ in range(map_size)]

        # Update the map based on input data
        for i in range(map_size):
            room_info = map_data[i].split('.')
            for j, info in enumerate(room_info):
                if info != '-':
                    game_map[i][j] = info
                if info == 'A':
                    self.__curLoc = [i+1, j+1]
        self.__wumpusWorld = game_map

    def __init__(self):
        self.__curLoc = [1,1]
        self.__isAlive = True
        self.__hasExited = False
        self.__direction = RIGHT
        self.__wumpusWorld = [['-' for _ in range(10)] for _ in range(10)]
        self.score = 0
        self.percept = {'breeze':False,'stench':False, 'bump':False, 'scream':False}
        self.loadFile('map1.txt')

    def __CheckForPitWumpus(self):
        ww = self.__wumpusWorld
        i,j = self.__curLoc[0]-1,self.__curLoc[1]-1
        if 'P' in ww[i][j] or 'W' in ww[i][j]:
            self.__isAlive = False
            print('Agent is DEAD.')
        return self.__isAlive

    def TakeAction(self,action): # The function takes an action and returns whether the Agent is alive
                                # after taking the action.
        validActions = ['Left', 'Down', 'Right', 'Up', 'Shoot']
        # assert action in validActions, 'Invalid Action.'
        if self.__isAlive == False:
            print('Action cannot be performed. Agent is DEAD. Location:{0}'.format(self.__curLoc))
            return False
        if self.__hasExited == True:
            print('Action cannot be performed. Agent has exited the Wumpus world.'.format(self.__curLoc))
            return False
        ww = self.__wumpusWorld
        if action == SHOOT:
            self.score -= 100
            print('Agent has shot an arrow, direction: {0}'.format(validActions[self.__direction]))

            if self.__direction == UP:
                if ww[self.__curLoc[0]-1-1][self.__curLoc[1]-1] == 'W':
                    self.__wumpusWorld[self.__curLoc[0]-1-1][self.__curLoc[1]-1] = '-'
                    self.percept['scream'] = True
                    print('Wumpus killed.')
            if self.__direction == DOWN:
                if ww[self.__curLoc[0]-1+1][self.__curLoc[1]-1] == 'W':
                    self.__wumpusWorld[self.__curLoc[0]-1+1][self.__curLoc[1]-1] = '-'
                    self.percept['scream'] = True
                    print('Wumpus killed.')
            if self.__direction == LEFT:
                if ww[self.__curLoc[0]-1][self.__curLoc[1]-1-1] == 'W':
                    self.__wumpusWorld[self.__curLoc[0]-1][self.__curLoc[1]-1-1] = '-'
                    self.percept['scream'] = True
                    print('Wumpus killed.')
            if self.__direction == RIGHT:
                if ww[self.__curLoc[0]-1][self.__curLoc[1]-1+1] == 'W':
                    self.__wumpusWorld[self.__curLoc[0]-1][self.__curLoc[1]-1+1] = '-'
                    self.percept['scream'] = True
                    print('Wumpus killed.')

        if action == UP:
            self.score -= 10
            self.__direction = UP
            if self.__curLoc[0] == 1:
                self.percept['bump'] = True
                print('Agent has bumped into a wall.')
            else:
                self.__curLoc[0] -= 1
                print('Agent move up to {0}.'.format(self.__curLoc))
        if action == DOWN:
            self.score -= 10
            self.__direction = DOWN
            if self.__curLoc[0] == 10:
                self.percept['bump'] = True
                print('Agent has bumped into a wall.')
            else:
                self.__curLoc[0] += 1
                print('Agent move down to {0}.'.format(self.__curLoc))
        if action == LEFT:
            self.score -= 10
            self.__direction = LEFT
            if self.__curLoc[1] == 1:
                self.percept['bump'] = True
                print('Agent has bumped into a wall.')
            else:
                self.__curLoc[1] -= 1
                print('Agent move left to {0}.'.format(self.__curLoc))
        if action == RIGHT:
            self.score -= 10
            self.__direction = RIGHT
            if self.__curLoc[1] == 10:
                self.percept['bump'] = True
                print('Agent has bumped into a wall.')
            else:
                self.__curLoc[1] += 1
                print('Agent move right to {0}.'.format(self.__curLoc))

        if self.__curLoc == [10,1]:
            self.__hasExited = True
            print('Agent has exited the Wumpus World.')
        if ww[self.__curLoc[0]-1][self.__curLoc[1]-1] == 'G':
            self.score += 1000
            print('Agent has found the Gold.')
            self.__wumpusWorld[self.__curLoc[0]-1][self.__curLoc[1]-1] = '-'
        return self.__CheckForPitWumpus()
    
    def __FindAdjacentRooms(self):
        cLoc = self.__curLoc
        validMoves = [[0,1],[0,-1],[-1,0],[1,0]]
        adjRooms = []
        for vM in validMoves:
            room = []
            valid = True
            for v, inc in zip(cLoc,vM):
                z = v + inc
                if z<1 or z>10:
                    valid = False
                    break
                else:
                    room.append(z)
            if valid==True:
                adjRooms.append(room)
        return adjRooms
                
        
    def PerceiveCurrentLocation(self): #This function perceives the current location. 
                                        #It tells whether breeze and stench are present in the current location.
        ww = self.__wumpusWorld
        if self.__isAlive == False:
            print('Agent cannot perceive. Agent is DEAD. Location:{0}'.format(self.__curLoc))
            return [None,None]
        if self.__hasExited == True:
            print('Agent cannot perceive. Agent has exited the Wumpus World.'.format(self.__curLoc))
            return [None,None]

        adjRooms = self.__FindAdjacentRooms()
        for room in adjRooms:
            i,j = room[0]-1,room[1]-1
            if 'P' in ww[i][j]:
                self.percept['breeze'] = True
            if 'W' in ww[i][j]:
                self.percept['stench'] = True
        self.percept['bump'] = False
        self.percept['scream'] = False
        return self.percept
    
    def CurrentPercept(self):
        return self.percept
    
    def FindCurrentLocation(self):
        return self.__curLoc
    def FindCurrentDirection(self):
        return self.__direction
    def TurnDirection(self, direction):
        self.__direction = direction

    def GetStatus(self):
        return (self.__isAlive, self.__hasExited)

def main():
    ag = Agent()
    print('curLoc',ag.FindCurrentLocation())
    print('Percept [breeze, stench] :',ag.PerceiveCurrentLocation())
    ag.TakeAction('Right')
    print('Percept',ag.PerceiveCurrentLocation())
    ag.TakeAction('Right')
    print('Percept',ag.PerceiveCurrentLocation())
    ag.TakeAction('Right')
    print('Percept',ag.PerceiveCurrentLocation())
    ag.TakeAction('Up')
    print('Percept',ag.PerceiveCurrentLocation())
    ag.TakeAction('Up')
    print('Percept',ag.PerceiveCurrentLocation())
    ag.TakeAction('Up')
    print('Percept',ag.PerceiveCurrentLocation())


if __name__=='__main__':
    main()
