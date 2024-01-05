from Game import * 
import PyAgent 
from WumpSim import *
import copy
import queue 
from Action import *


def MoveToUnvisited(ag, kb, visited): #dfs to new safe room
    initLoc=ag.FindCurrentLocation()
    initLocIndex= 10*(initLoc[0]-1)+initLoc[1]-1

    bfsVisited = [False for i in range(100)] 
    bfsVisited[initLocIndex]=True

    pre = [(-1, -1) for i in range(100)] 

    direction = [(0,-1), (1,0), (0,1), (-1,0)]

    qu = queue.Queue()
    while qu.empty() == False:
        qu.get()
    qu.put(initLoc)

    while qu.empty() == False:
        curLoc = qu.get()
        curLocIndex= 10*(curLoc[0]-1)+curLoc[1]-1

        for i in range(4):
            newLoc= [curLoc[0]+direction[i][0], curLoc[1]+direction[i][1]]
            if newLoc[0]>0 and newLoc[0]<=10 and newLoc[1]>0 and newLoc[1]<=10:
                newLocIndex= 10*(newLoc[0]-1)+ newLoc[1]-1
                if bfsVisited[newLocIndex]==False:
                    if visited[newLocIndex]==True:
                        qu.put(newLoc)
                        bfsVisited[newLocIndex]=True
                        pre[newLocIndex] = (i, curLocIndex)
                    else:
                        tempclauses= kb.getclauses()
                        tempclauses.append({newLocIndex:1, newLocIndex+100*2:1})
                        if DPLLSatisfiable(tempclauses)==False:
                            print('I choose {0} to visit.'.format(newLoc))
                            #Room is safe
                            noWumpus={newLocIndex:-1}
                            noPit={newLocIndex+100*2:-1}
                            kb.AddClause(noWumpus)
                            kb.AddClause(noPit)

                            pre[newLocIndex] = (i, curLocIndex)
                            listAction = []
                            while newLocIndex != initLocIndex:
                                print(newLocIndex // 10 + 1, newLocIndex % 10 + 1)
                                listAction.append(pre[newLocIndex][0])
                                newLocIndex = pre[newLocIndex][1]
                            print(listAction[::-1])
                            for action in listAction[::-1]:
                                ag.TakeAction(action)
                            visited[newLocIndex] = True
                            return True

    return False

def ExitWumpusWorld(ag, kb):
    visited = [False for i in range(100)] #Rooms Visited till now 
    while(ag.GetStatus()[0] == True and ag.GetStatus()[1] == False):
        percept= ag.PerceiveCurrentLocation() 
        print('Percept',percept)

        curPos = ag.FindCurrentLocation()
        curLocIndex= 10*(curPos[0]-1)+ curPos[1]-1
        visited[curLocIndex]=True
        
        breezeClause={}
        stenchClause={}

        if percept['breeze']==True: #breeze
            breezeClause[curLocIndex+100*3]=1
        else:
            breezeClause[curLocIndex+100*3]=-1
        kb.AddClause(breezeClause) #presence/absence of breeze

        if percept['stench']==True: #stench
            stenchClause[curLocIndex+100]=1
        else:
            stenchClause[curLocIndex+100]=-1
        kb.AddClause(stenchClause) #presence/absence of stench
    
        direction = [(0,-1), (1,0), (0,1), (-1,0)]
        
        isMove = MoveToUnvisited(ag, kb, visited)

        if isMove == False:
            for i in range(4):
                newLoc= [curPos[0]+direction[i][0], curPos[1]+direction[i][1]]
                if newLoc[0]>0 and newLoc[0]<=10 and newLoc[1]>0 and newLoc[1]<=10:
                    newLocIndex= 10*(newLoc[0]-1)+ newLoc[1]-1
                    if visited[newLocIndex]==False:
                        ag.TurnDirection(i)
                        ag.TakeAction(SHOOT)
                        curpercept = ag.CurrentPercept()
                        if curpercept['scream'] == True:
                            noWumpus={newLocIndex:-1}
                            noPit={newLocIndex+100*2:-1}
                            kb.AddClause(noWumpus)
                            kb.AddClause(noPit)
                            ag.TakeAction(i)
                            isMove = True
                            break
        
        if isMove == False:
            print('Agent can not decide where to go, current location: {0}'.format(ag.FindCurrentLocation()))
            break
        print('\n')


def main():
    agent = PyAgent.Agent()
    kb = WumpSim.KnowledgeBase()

    game = Game(agent.wumpusWorld)

    game.run()
    ExitWumpusWorld(game, agent, kb)


if __name__ == '__main__':
    main()


