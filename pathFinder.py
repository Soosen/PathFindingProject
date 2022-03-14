from multiprocessing.sharedctypes import Value
import numpy
from collections import deque
WALL = 0
EMPTY_CELL = 1

class PathFinder:

    #init the pathfinder
    def __init__(self, maze):
        self.maze = maze
        self.maze_size = self.maze[0].size

    #check if visited includes cell
    def isVisited(self, cell, visited):
        for i in range (visited.size):
            if(visited[i].x == cell.x and visited[i].y == cell.y):
                return True

        return False

    #check if visitedNodes include Node
    def isNodeVisited(self, node, visited):
        for i in range (visited.size):
            if(visited[i].cell.x == node.cell.x and visited[i].cell.y == node.cell.y):
                return True

        return False

    #check if arrayStart includes any element of arrayEnd, if so return both Nodes
    def bidirectional_isVisited(self, arrayStart, arrayEnd):
        for a in arrayStart:
            for b in arrayEnd:
                if(a.cell.x == b.cell.x and a.cell.y == b.cell.y):
                    return a, b

        return None, None

    #check if a cell is a wall
    def isWall(self, cell):
        return cell.x < 0 or cell.x > self.maze_size -1 or cell.x < 0 or cell.y > self.maze_size - 1 or self.maze[cell.x][cell.y] == WALL

    #calculate the manhattan metric between two cells
    def manhattanMetric(self, cellA, cellB):
        return abs(cellA.x - cellB.x) + abs(cellA.y - cellB.y)

    #get the index of a node with lowest heuristic
    def lowestHeuristicIndex(self, array):
        smallestIndex = 0
        for i in range (array.size):
            if(array[i].heuristic < array[smallestIndex].heuristic):
                smallestIndex = i

        return smallestIndex

    #breadth first search
    def breadth_first_search(self):

        startCell = Cell(0, 0)
        endCell = Cell(self.maze_size - 1, self.maze_size - 1)
        q = deque([])
        visited = numpy.array([])
        root = Node(startCell, numpy.array([]), 0)
        visited = numpy.append(visited, root.cell)
        q.append(root)

        while q:
            currentNode = q.popleft()            
            
            if(currentNode.cell.x == endCell.x and currentNode.cell.y == endCell.y):
                return currentNode.path, visited

            neighbours = currentNode.getNeighbours(self.maze_size)

            for i in range (neighbours.size):
                if(not self.isVisited(neighbours[i].cell, visited) and not self.isWall(neighbours[i].cell)):
                    visited = numpy.append(visited, neighbours[i].cell)
                    q.append(neighbours[i])


    #depth first search
    def depth_first_search(self, maxDepth):

        startCell = Cell(0, 0)
        endCell = Cell(self.maze_size - 1, self.maze_size - 1)

        visited = numpy.array([])
        q = deque([])
        root = Node(startCell, numpy.array([]), 0)
        visited = numpy.append(visited, root.cell)
        q.append(root)

        while q:
            currentNode = q.pop()
            visited = numpy.append(visited, currentNode.cell)
            if(currentNode.cell.x == endCell.x and currentNode.cell.y == endCell.y):
                return currentNode.path, visited

            if(currentNode.depth != maxDepth):

                neighbours = currentNode.getNeighbours(self.maze_size)

                for i in range (neighbours.size): 
                        if(not self.isVisited(neighbours[i].cell, visited) and not self.isWall(neighbours[i].cell)):
                            q.append(neighbours[i])

    #iterative depth first search
    def iterative_depth_first_search(self, currentMaxDepth, maxDepth):

        print("Current Max Depth = ", currentMaxDepth)
        startCell = Cell(0, 0)
        endCell = Cell(self.maze_size - 1, self.maze_size - 1)

        visited = numpy.array([])
        q = deque([])
        root = Node(startCell, numpy.array([]), 0)
        visited = numpy.append(visited, root.cell)
        q.append(root)

        while q:
            currentNode = q.pop()
            visited = numpy.append(visited, currentNode.cell)
            if(currentNode.cell.x == endCell.x and currentNode.cell.y == endCell.y):
                return currentNode.path, visited

            if(currentNode.depth != currentMaxDepth):

                neighbours = currentNode.getNeighbours(self.maze_size)

                for i in range (neighbours.size): 
                        if(not self.isVisited(neighbours[i].cell, visited) and not self.isWall(neighbours[i].cell)):
                            q.append(neighbours[i])
        
        if(currentMaxDepth != maxDepth):
            return self.iterative_depth_first_search(currentMaxDepth + 1, maxDepth)

    #A*
    def AStar(self):

        startCell = Cell(0, 0)
        endCell = Cell(self.maze_size - 1, self.maze_size - 1)

        visited = numpy.array([])
        queue = numpy.array([])
        root = Node(startCell, numpy.array([]), 0)
        root.addHeuristic(self.manhattanMetric(startCell, endCell))
        visited = numpy.append(visited, root.cell)
        queue = numpy.append(queue, root)

        while queue.size != 0:
            currentNode = queue[self.lowestHeuristicIndex(queue)]
            queue = numpy.delete(queue, self.lowestHeuristicIndex(queue))

            visited = numpy.append(visited, currentNode.cell)
            if(currentNode.cell.x == endCell.x and currentNode.cell.y == endCell.y):
                return currentNode.path, visited

            neighbours = currentNode.getNeighbours(self.maze_size)

            for i in range (neighbours.size): 
                    if(not self.isVisited(neighbours[i].cell, visited) and not self.isWall(neighbours[i].cell)):
                        neighbours[i].addHeuristic(self.manhattanMetric(neighbours[i].cell, endCell))
                        queue = numpy.append(queue, neighbours[i])

    #bidirectional breadht first search
    def bidirectional_breadth_first_search(self):

        startCell = Cell(0, 0)
        endCell = Cell(self.maze_size - 1, self.maze_size - 1)
        q = deque([])
        visitedStart = numpy.array([])
        visitedEnd = numpy.array([])
        root = Node(startCell, numpy.array([]), 0)
        tail = Node(endCell, numpy.array([]), 0)
        root.addDirection(0)
        tail.addDirection(1)
        visitedStart = numpy.append(visitedStart, root)
        visitedEnd = numpy.append(visitedEnd, tail)
        q.append(root)
        q.append(tail)

        while q:
            currentNode = q.popleft()            
            
            NodeA, NodeB = self.bidirectional_isVisited(visitedStart, visitedEnd)
            if(NodeA is not None and NodeB is not None):
                path = numpy.array(NodeA.path) 
                path = numpy.append(path, NodeB.path)
                visited = numpy.array([])

                while(visitedStart.size != 0 or visitedEnd.size != 0):
                    if(visitedStart.size != 0):
                        visited = numpy.append(visited, visitedStart[0].cell)
                        visitedStart = numpy.delete(visitedStart, 0)

                    if(visitedEnd.size != 0):
                        visited = numpy.append(visited, visitedEnd[0].cell)
                        visitedEnd = numpy.delete(visitedEnd, 0)

                return path, visited

            neighbours = currentNode.getNeighbours(self.maze_size)

            for i in range (neighbours.size):
                if(currentNode.direction == 0):
                     if(not self.isNodeVisited(neighbours[i], visitedStart) and not self.isWall(neighbours[i].cell)):
                        neighbours[i].addDirection(currentNode.direction)
                        visitedStart = numpy.append(visitedStart, neighbours[i])
                        q.append(neighbours[i])
                else:
                    if(not self.isNodeVisited(neighbours[i], visitedEnd) and not self.isWall(neighbours[i].cell)):
                        neighbours[i].addDirection(currentNode.direction)
                        visitedEnd = numpy.append(visitedEnd, neighbours[i])
                        q.append(neighbours[i])
                   

            
           
#leaf of a searching tree containing cell, path, depth, heuristic, diretion
class Node(): 
    def __init__(self, cell, p, d):
        self.cell = cell
        self.path = numpy.append(p, self.cell)
        self.depth = d
        self.heuristic = -1
        self.direction = -1

    def addHeuristic(self, h):
        self.heuristic = h

    def addDirection(self, dir):
        self.direction = dir

    def getNeighbours(self, maze_size):
        neigh = numpy.array([])

        if(self.cell.x + 1 <= maze_size):
            neigh = numpy.append(neigh, Node(Cell(self.cell.x + 1, self.cell.y), self.path , self.depth + 1))
        
        if(self.cell.x - 1 >= 0):
            neigh = numpy.append(neigh, Node(Cell(self.cell.x - 1, self.cell.y), self.path, self.depth + 1))

        if(self.cell.y + 1 <= maze_size):
            neigh = numpy.append(neigh, Node(Cell(self.cell.x, self.cell.y + 1), self.path, self.depth + 1))

        if(self.cell.y - 1 >= 0):
            neigh = numpy.append(neigh, Node(Cell(self.cell.x, self.cell.y - 1), self.path, self.depth + 1))

        return neigh

class Cell(): 
    def __init__(self, x, y):
        self.x = x
        self.y = y   
