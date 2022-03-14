import numpy
import queue
import arcade

class PathFinder:

    def __init__(self, maze):
        self.maze = maze
        self.maze_size = self.maze[0].size

    def isVisited(self, cell, visited):
        for i in range (visited.size):
            if(visited[i].x == cell.x and visited[i].y == cell.y):
                return True

        return False
    
    def isWall(self, cell):
        return cell.x < 0 or cell.x > self.maze_size -1 or cell.x < 0 or cell.y > self.maze_size - 1 or self.maze[cell.x][cell.y] == 0

    def depth_first_search(self):

        startCell = Cell(0, 0)
        endCell = Cell(self.maze_size - 1, self.maze_size - 1)
        q = queue.Queue()
        visited = numpy.array([])
        root = Node(startCell, numpy.array([]))
        visited = numpy.append(visited, root.cell)
        q.put(root)

        while q.qsize() != 0:
            currentNode = q.get()            
            
            if(currentNode.cell.x == endCell.x and currentNode.cell.y == endCell.y):
                return currentNode.path, visited

            neighbours = currentNode.getNeighbours(self.maze_size)

            for i in range (neighbours.size):
                if(not self.isVisited(neighbours[i].cell, visited) and not self.isWall(neighbours[i].cell)):
                    visited = numpy.append(visited, neighbours[i].cell)
                    q.put(neighbours[i])

            


class Node(): 
    def __init__(self, cell, p):
        self.cell = cell
        self.path = numpy.append(p, self.cell)

    def getNeighbours(self, maze_size):
        neigh = numpy.array([])

        if(self.cell.x + 1 <= maze_size):
            neigh = numpy.append(neigh, Node(Cell(self.cell.x + 1, self.cell.y), self.path))
        
        if(self.cell.x - 1 >= 0):
            neigh = numpy.append(neigh, Node(Cell(self.cell.x - 1, self.cell.y), self.path))

        if(self.cell.y + 1 <= maze_size):
            neigh = numpy.append(neigh, Node(Cell(self.cell.x, self.cell.y + 1), self.path))

        if(self.cell.y - 1 >= 0):
            neigh = numpy.append(neigh, Node(Cell(self.cell.x, self.cell.y - 1), self.path))

        return neigh

class Cell(): 
    def __init__(self, x, y):
        self.x = x
        self.y = y   
