from pickle import FALSE, TRUE
import numpy
import random

WALL = 0
EMPTY_CELL = 1

class MazeGenerator():

    #init the maze generator 
    def __init__(self, size, maze_width):
        #maze size is self.maze_size x self.maze_size
        self.maze_size = size
        
        #set maze to a new 2d maze_size x maze_size array filled with zeros
        self.maze = numpy.zeros(shape = (self.maze_size, self.maze_size))

        #generate a new maze and assign self.maze to it
        self.generateMaze()
   
    def generateMaze(self):
        #set visited to an empty array
        visited = numpy.array([])

        #generate the maze
        self.depth_first_search_with_backtracking(self.maze, Cell(0,0), visited)

        #I always set the endCell in the rigth top corner, so i want to make sure it is always connected to the rest of the maze
        counter = self.maze_size - 1
        while(self.maze[counter][self.maze_size - 1] == 0):
            self.maze[counter][self.maze_size - 1] = 1
            counter = counter - 1

        return self.maze

    #check if the visited list includes the cell
    def isVisited(self, cell, visited):
        for i in range (visited.size):
            if(visited[i].x == cell.x and visited[i].y == cell.y):
                return True

        return False

    #depth first search with backtracking used to create a maze
    def depth_first_search_with_backtracking(self, maze, cell, visited):

        #remove wall from the cell
        maze[cell.x][cell.y] = EMPTY_CELL

        #add the cell to visited
        visited = numpy.append(visited, cell)

        #get all neighbours of the cell
        neighbours = cell.getNeighbours(self.maze_size)

        #for all neighbours
        while neighbours.size != 0:

            #pick random neighbour
            index = random.randint(0, neighbours.size - 1)

            #if chosen neighbour was not visited
            if(not self.isVisited(neighbours[index], visited)):

                #if the neighbour has at least 3 walls around itself recursivly call depth first search with backtracking from the neighbour
                if(self.countWalls(neighbours[index]) >= 3):
                    visited = self.depth_first_search_with_backtracking(maze, neighbours[index], visited)
               
            #delete the neighbour from neighbours arary
            neighbours = numpy.delete(neighbours, index)    
                
        return visited

        #count how many walls there are around the cell
    def countWalls(self, cell):
        counter = 0

        if(cell.x + 1 <= self.maze_size - 1 and self.maze[cell.x + 1][cell.y] == 0):
            counter = counter + 1
        
        if(cell.x - 1 >= 0 and self.maze[cell.x - 1][cell.y] == 0):
            counter = counter + 1
        
        if(cell.y + 1 <= self.maze_size - 1 and self.maze[cell.x][cell.y + 1] == 0):
            counter = counter + 1

        if(cell.y - 1 >= 0 and self.maze[cell.x][cell.y - 1] == 0):
            counter = counter + 1

        if(cell.x == 0 or cell.x == self.maze_size - 1 or cell.y == 0 or cell.y == self.maze_size - 1):
            counter = counter + 1

        if((cell.x == 0 and cell.y == 0) or (cell.x == self.maze_size - 1 and cell.y == self.maze_size - 1)):
            counter = counter + 1

        return counter

#tuple of x and y coordinates in the maze
class Cell(): 
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getNeighbours(self, maze_size):
        neigh = numpy.array([])

        if(self.x + 1 <= maze_size - 1):
            neigh = numpy.append(neigh, Cell(self.x + 1, self.y))
        
        if(self.x - 1 >= 0):
            neigh = numpy.append(neigh, Cell(self.x - 1, self.y))

        if(self.y + 1 <= maze_size - 1):
            neigh = numpy.append(neigh, Cell(self.x, self.y + 1))

        if(self.y - 1 >= 0):
            neigh = numpy.append(neigh, Cell(self.x, self.y - 1))

        return neigh