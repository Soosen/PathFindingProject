from pickle import FALSE, TRUE
import numpy
import random


class MazeGenerator():

    def __init__(self, size, maze_width):
        self.maze_size = size
        self.maze_width = maze_width
        self.tile_size = self.maze_width / (self.maze_size + 2)
        self.maze = numpy.zeros(shape = (self.maze_size, self.maze_size))
        self.generateMaze()
   
    def generateMaze(self):
        visited = numpy.array([])
        self.depth_first_search_with_backtracking(self.maze, Cell(0,0), visited)

        counter = self.maze_size - 1
        while(self.maze[counter][self.maze_size - 1] == 0):
            self.maze[counter][self.maze_size - 1] = 1
            counter = counter - 1

        return self.maze


    def isVisited(self, cell, visited):
        for i in range (visited.size):
            if(visited[i].x == cell.x and visited[i].y == cell.y):
                return True

        return False

    def depth_first_search_with_backtracking(self, maze, cell, visited):

        maze[cell.x][cell.y] = 1
        visited = numpy.append(visited, cell)
        neighbours = cell.getNeighbours(self.maze_size)

        while neighbours.size != 0:
            index = random.randint(0, neighbours.size - 1)
            if(not self.isVisited(neighbours[index], visited)):
                if(self.countWalls(neighbours[index]) >= 3):
                    visited = self.depth_first_search_with_backtracking(maze, neighbours[index], visited)
               

            neighbours = numpy.delete(neighbours, index)    
                
        return visited
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