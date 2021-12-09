from __future__ import print_function
import heapq
import copy
import sys

class Puzzle:
    #class to represent puzzle transition model
    #takes in goal array and initial node
    def __init__(self, goal, initial):
        self.goal = goal
        self.state = initial

    def setState(self, state):
        self.state = copy.deepcopy(state)
    
    def getState(self):
        return self.state
    
    #return string with possible movements from state
    def getMoves(self):
        x = 0
        y = 0
        for r in range(0,3):
            for c in range(0,4): 
                if self.state[r][c] == '0':
                    x = r
                    y = c
        moves = ""
        
        if x != 2 :
            moves += 'D'
        if x != 0 :
            moves += 'U'
        if y != 0 :
            moves += 'L'
        if y != 3 :
            moves += 'R'
        
        return moves

    #adjust on move (L, R, D, U)
    def moveTile(self, move):
        x = 0
        y = 0
        for r in range(0,3):
            for c in range(0,4): 
                if(self.state[r][c] == '0'):
                    x = r
                    y = c
        #swap blank tiles with valued tiles
        if move == 'L':
            self.state[x][y], self.state[x][y - 1] = self.state[x][y - 1], self.state[x][y]
        elif move == 'R':
            self.state[x][y], self.state[x][y + 1] = self.state[x][y + 1], self.state[x][y]
        elif move == 'U':
            self.state[x][y], self.state[x - 1][y] = self.state[x - 1][y], self.state[x][y]
        elif move == 'D':
            self.state[x][y], self.state[x + 1][y] = self.state[x + 1][y], self.state[x][y]
        else:
            return

    def heuristic(self):
        h = 0
        #find manhattan distance
        for r in range(0,3):
            for c in range(0,4): 
                #disregarding 0 value in array
                if self.state[r][c] != self.goal[r][c] and self.state[r][c] != '0':
                    #iterate through goal node to find matching tile
                    for gr in range(0,3):
                        for gc in range(0,4): 
                            if self.state[r][c] == self.goal[gr][gc]:
                                #add manhattan distance to distance sum
                                h += (abs(r-gr) + abs(c-gc))
        return h

    def printState(self):
        print('\n'.join([''.join(['{:3}'.format(item) for item in row]) 
        for row in self.state]))

    def done(self):
        for r in range(0,3):
            for c in range(0,4): 
                if self.state[r][c] != self.goal[r][c]: 
                    return False
        return True

#represents a configuration of puzzle
class Node:
    def __init__(self, parent, state, g, h, w, move=None):
        self.parent = parent
        self.state = copy.deepcopy(state) #board
        self.move = move #movement from parent
        self.g = g #depth
        self.h = h #sum of manhattan dist
        self.w = w #weight
        self.f = self.g + (self.w * self.h)
        self.hash = hash(str(self.state))

    def __lt__(self, other):
        return self.f < other.f    

    def __gt__(self, other):
        return self.f > other.f
    
    def __le__(self, other):
        return self.f <= other.f
    
    def __ge__(self, other):
        return self.f >= other.f

#function to run search
#parameters are initial state and environment
def astarSearch(start_node, board, w):
    
    #function to reverse traverse solution node to get path
    def traverse(node, path=[]):
        path.append(node)
        if node.parent != None:
            return traverse(node.parent, path)
        else:
            path.reverse()
            return path
    
    frontier = [start_node] #fifo queue
    totalNodes = 0 
    nodeHist = {} # expanded nodes
    done = False

    #generate children until goal found    
    while not done:
        
        #expand least cost node
        parent = heapq.heappop(frontier)    

        #check if duplicated state, change f value if f is lower than dupe
        if nodeHist.get(parent.hash, float("inf")) > parent.f:
            nodeHist[parent.hash] = parent.f
        else:
            continue
        
        board.setState(parent.state)
    
        if board.done():
            return traverse(parent), totalNodes

        #generate children of parent
        moves = board.getMoves()
        for move in moves:
            board.moveTile(move)
            heapq.heappush(frontier, Node(parent, board.getState(), 1 + parent.g, board.heuristic(), w, move))    
            totalNodes += 1
            board.setState(parent.state) #reset board state


def main():
    inputFile = "input3.txt"
    outputFile = "test.txt"

    #read initial and goal states from file
    with open(inputFile) as textFile:
        nodes = [line.split() for line in textFile]
        initial = nodes[0:3]
        goal = nodes[4:7]
    
    #get weight value from user
    w = input("Please enter weight: ")

    board = Puzzle(goal, initial) # initialize puzzle
    initNode = Node(None, board.getState(), 0, board.heuristic(), w, initial) # create initial node
    solution = astarSearch(initNode, board, w) # run search 
    toFile(goal, initial, w, solution, outputFile) # output to file

    
#function to output to file
def toFile(goal, initial, w, solution, outputFile):
    with open(outputFile, 'w') as outputFile:
        sys.stdout = outputFile # std out is output file 
        
        path = solution[0] 

        #print initial and goal boards
        print('\n'.join([''.join(['{:3}'.format(item) for item in row]) 
        for row in initial]))

        print()

        print('\n'.join([''.join(['{:3}'.format(item) for item in row]) 
        for row in goal]))

        print()

        print(w) #weight
        print(len(path) - 1) #depth
        print(solution[1]) #total number of nodes
        
        # Print the list of moves in order
        for node in path[1:]:
            print(node.move, end=" ")
        print()
        
        # Print the f(n) values in order
        for node in path:
            print(node.f, end=" ")
        print()
    
    # Reset stdout
    sys.stdout = sys.__stdout__


#run script
main()
