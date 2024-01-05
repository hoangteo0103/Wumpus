#!/usr/bin/env python3
from PyAgent import * # See the Agent.py file
import copy
numberOfCalls=0

class KnowledgeBase:
    #clause[i]=-1 represents the presence of negative literal represented by i
    #clause[i]=1 represents the presence of positive literal represented by i
    #values 0 to 99 represents W(1,1) to W(100,100)
    #values 100 to 199 represents S(1,1) to S(100,100)
    #values 200 to 299 represents P(1,1) to P(100,100)
    #values 300 to 399 represents B(1,1) to B(100,100)
    def __init__(self, x , y):
        self.clauses= []

        #clauses for atleast 1 Wumpus and 1 Pit
        atleast1Wumpus= {}
        for i in range (100):
            atleast1Wumpus[i]=1
        self.clauses.append(atleast1Wumpus)

        #Stench-Wumpus bijection clauses
        for i in range(100):
            stenchWumpusClause={}
            stenchWumpusClause[i+100]=-1
            if (i+10)//10 < 10:
                stenchWumpusClause[i+10]=1
                stenchClause={}
                stenchClause[i+100]=1
                stenchClause[i+10]=-1
                self.clauses.append(stenchClause)
            if(i-10)//10 >= 0:
                stenchWumpusClause[i-10]=1
                stenchClause={}
                stenchClause[i+100]=1
                stenchClause[i-10]=-1
                self.clauses.append(stenchClause)
            if i//10 == (i+1)//10:
                stenchWumpusClause[i+1]=1
                stenchClause={}
                stenchClause[i+100]=1
                stenchClause[i+1]=-1
                self.clauses.append(stenchClause)
            if i//10 == (i-1)//10:
                stenchWumpusClause[i-1]=1
                stenchClause={}
                stenchClause[i+100]=1
                stenchClause[i-1]=-1
                self.clauses.append(stenchClause)
            self.clauses.append(stenchWumpusClause)
        
        #Breeze-Pit Bijection Clauses
        for i in range(100):
            breezePitClause={}
            breezePitClause[i+100*3]=-1
            if(i+10)//10 < 10:
                breezePitClause[i+10+100*2]=1
                pitClause={}
                pitClause[i+100*3]=1
                pitClause[i+10+100*2]=-1
                self.clauses.append(pitClause)
            if(i-10)//10 >= 0:
                breezePitClause[i-10+100*2]=1
                pitClause={}
                pitClause[i+100*3]=1
                pitClause[i-10+100*2]=-1
                self.clauses.append(pitClause)
            if i//10 == (i+1)//10:
                breezePitClause[i+1+100*2]=1
                pitClause={}
                pitClause[i+100*3]=1
                pitClause[i+1+100*2]=-1
                self.clauses.append(pitClause)
            if i//10 == (i-1)//10:
                breezePitClause[i-1+100*2]=1
                pitClause={}
                pitClause[i+100*3]=1
                pitClause[i-1+100*2]=-1
                self.clauses.append(pitClause)
            self.clauses.append(breezePitClause)

        #No wumpus and pit at [1, 1]
        noWumpusStart={ (x-1) * 10 + y - 1 :-1}
        noPitStart={ (x-1) * 10 + y -1 :-1}
        self.clauses.append(noWumpusStart)
        self.clauses.append(noPitStart)

    def AddClause(self, clause): #adding a clause to knowledge base
        self.clauses.append(clause)
    
    def getclauses(self): #return Wumpus clauses
        return copy.deepcopy(self.clauses)
    

def FindPureSymbol(clauses, symbols):
    for symbol in symbols:
        positive=0
        negative=0
        for clause in clauses:
            if symbol in clause:
                if clause[symbol]==1:
                    positive= positive+1
                else:
                    negative= negative+1
        if negative==0:
            return symbol, 1
        elif positive==0:
            return symbol, -1
    return -1, 0

def FindUnitClause(clauses):
    for clause in clauses:
        if len(clause)==1:
            for symbol in clause:
                return symbol, clause[symbol]
    return -1, 0

def selectSymbol(clauses, symbols):
    count={}
    positive={}
    negative={}
    for clause in clauses:
        for literal in clause:
            if literal not in count:
                count[literal]=0
                positive[literal]=0
                negative[literal]=0

            count[literal]= count[literal]+1
            if clause[literal]==1:
                positive[literal]=positive[literal]+1
            else:
                negative[literal]=negative[literal]+1
    
    maxLiteral= list(symbols.keys())[0]
    maxCount=0
    for literal in count:
        if count[literal]>maxCount:
            maxLiteral= literal
            maxCount= count[literal]

    if positive[maxLiteral]>negative[maxLiteral]:
        return maxLiteral, 1
    return maxLiteral, -1

def DPLL(clauses, symbols, model):
    global numberOfCalls
    numberOfCalls= numberOfCalls+1
    removeClauses=[]
    for clause in clauses:
        valueUnknown=True
        deleteLiterals=[]
        for literal in clause.keys():
            if literal in model.keys():
                if model[literal]==clause[literal]: #clause is true
                    removeClauses.append(clause)
                    valueUnknown=False
                    break
                else:
                    deleteLiterals.append(literal)
        
        for literal in deleteLiterals:
            del clause[literal]
        if valueUnknown==True and not bool(clause): #clause is false
            return False

    clauses= [ x for x in clauses if x not in removeClauses]

    if len(clauses)==0: #all clauses are true
        return True

    pureSymbol, value = FindPureSymbol(clauses, symbols)
    if value!=0:
        del symbols[pureSymbol]
        model[pureSymbol]=value
        return DPLL(clauses, symbols, model)
    
    unitSymbol, value = FindUnitClause(clauses)
    if value!=0:
        del symbols[unitSymbol]
        model[unitSymbol]=value
        return DPLL(clauses, symbols, model)

    symbol, value= selectSymbol(clauses, symbols)
    del symbols[symbol]
    model[symbol]= value

    if DPLL(copy.deepcopy(clauses), copy.deepcopy(symbols), copy.deepcopy(model)):
        return True
    
    model[symbol]= -value
    return DPLL(clauses, symbols, model)


def DPLLSatisfiable(clauses):
    symbols={}
    for clause in clauses:
        for literal in clause:
            symbols[literal]=True
    
    model={}
    return DPLL(clauses, symbols, model)

def MoveToUnvisited(ag, visited, goalLoc, dfsVisited): #dfs to new safe room
    curPos=ag.FindCurrentLocation()
    curLoc= 10*(curPos[0]-1)+curPos[1]-1
    if(curLoc==goalLoc):
        return True
    dfsVisited[curLoc]=True
    
    if curPos[1]+1 <=10 and (visited[curLoc+1]==True or (curLoc+1)==goalLoc) and dfsVisited[curLoc+1]==False:
        ag.TakeAction('Up')
        roomReachable= MoveToUnvisited(ag, visited, goalLoc, dfsVisited)
        if roomReachable:
            return True
        ag.TakeAction('Down')

    if curPos[0]+1 <=10 and (visited[curLoc+10]==True or (curLoc+10)==goalLoc) and dfsVisited[curLoc+10]==False:
        ag.TakeAction('Right')
        roomReachable= MoveToUnvisited(ag, visited, goalLoc, dfsVisited)
        if roomReachable:
            return True
        ag.TakeAction('Left')

    if curPos[0]-1 >0 and (visited[curLoc-10]==True or (curLoc-10)==goalLoc) and dfsVisited[curLoc-10]==False:
        ag.TakeAction('Left')
        roomReachable= MoveToUnvisited(ag, visited, goalLoc, dfsVisited)
        if roomReachable:
            return True
        ag.TakeAction('Right')

    if curPos[1]-1 >0 and (visited[curLoc-1]==True or (curLoc-1)==goalLoc) and dfsVisited[curLoc-1]==False:
        ag.TakeAction('Down')
        roomReachable= MoveToUnvisited(ag, visited, goalLoc, dfsVisited)
        if roomReachable:
            return True
        ag.TakeAction('Up')

    return False

def ExitWumpusWorld(ag, kb):
    visited = [False for i in range(100)] #Rooms Visited till now 
    while(ag.FindCurrentLocation()!=[10, 10]):
        percept= ag.PerceiveCurrentLocation() 
        print('Percept',ag.PerceiveCurrentLocation())
        curPos = ag.FindCurrentLocation()
        curLocIndex= 10*(curPos[0]-1)+ curPos[1]-1
        curDirection= ag.FindCurrentDirection()
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
    
        direction = [(-1,0), (0,-1), (1,0), (0,1)]


        for i in range(4): 
            newLoc= [curPos[0]+direction[i][0], curPos[1]+direction[i][1]]
            if newLoc[0]>0 and newLoc[0]<=10 and newLoc[1]>0 and newLoc[1]<=10:
                newLocIndex= 10*(newLoc[0]-1)+ newLoc[1]-1
                if visited[newLocIndex]==False:
                    tempclauses= kb.getclauses()
                    tempclauses.append({newLocIndex:1, newLocIndex+100*2:1})
                    if DPLLSatisfiable(tempclauses)==False:
                        #Room is safe
                        noWumpus={newLocIndex:-1}
                        noPit={newLocIndex+100*2:-1}
                        kb.AddClause(noWumpus)
                        kb.AddClause(noPit)
                        ag.TakeAction(3 - i)

        for newLoc in range(100):
            if visited[newLoc]==False:
                tempclauses= kb.getclauses()
                checkClause={newLoc:1, newLoc+100*2:1}  
                tempclauses.append(checkClause)
                if DPLLSatisfiable(tempclauses)==False:
                    #Room is safe
                    noWumpus={newLoc:-1}
                    noPit={newLoc+100*2:-1}
                    kb.AddClause(noWumpus)
                    kb.AddClause(noPit)
                    dfsVisited = [False for i in range(100)] 
                    roomReachable=MoveToUnvisited(ag, visited, newLoc, dfsVisited) #dfs to new safe Room
                    if roomReachable:
                        break

def main():
    ag = Agent()
    kb= KnowledgeBase(ag.FindCurrentLocation()[0], ag.FindCurrentLocation()[1])
    print('Start Location: {0}'.format(ag.FindCurrentLocation()))
    ExitWumpusWorld(ag, kb)
    print('{0} reached. Exiting the Wumpus World.'.format(ag.FindCurrentLocation()))
    print('Total number of times DPLL function is called: {0}'.format(numberOfCalls))


if __name__=='__main__':
    main()
