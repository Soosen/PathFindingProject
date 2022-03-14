import arcade
import numpy

WALL = 0
EMPTY_CELL = 1
PATH = 2
VISITED = 3


class Maze:
    #init the maze
    def __init__(self, maze, width):
        #save the original maze to be able to reset it
        self.original_maze = numpy.copy(maze)

        #current maze state
        self.maze = maze

        #maze size
        self.maze_size = self.maze[0].size

        #width of the maze in pixels
        self.maze_width = width

        #size of one maze tile
        self.tile_size = self.maze_width / (self.maze_size + 2)


    #set maze state to another maze state
    def updateMaze(self, maze):
        self.maze = numpy.copy(maze)

    #set maze to the original maze
    def resetMaze(self):
        self.maze = numpy.copy(self.original_maze)

    #draw function wraper so you can draw a rectangle on a tile x, y    
    def drawRect(self, x , y, color):
        arcade.draw_rectangle_filled(3*self.tile_size/2 + x * self.tile_size, 3*self.tile_size/2 + y * self.tile_size, self.tile_size, self.tile_size, color)

    #draw the maze
    def draw(self):
        #generate outlines of the maze
        for i in range(self.maze_size + 2):
            #Horizontal
            self.drawRect(-1, i - 1, arcade.color.BLACK)
            self.drawRect(self.maze_size, i - 1, arcade.color.BLACK)

            #Vertical
            self.drawRect(i -1, -1, arcade.color.BLACK)
            self.drawRect(i - 1, self.maze_size, arcade.color.BLACK)

        #draw walls
        for i in range(self.maze_size):
            for j in range(self.maze_size):
                if(self.maze[i][j] == WALL):
                    self.drawRect(i, j, arcade.color.BLACK)
                elif(self.maze[i][j] == PATH):
                    self.drawRect(i, j, arcade.color.BLUE)
                elif(self.maze[i][j] == VISITED):
                    self.drawRect(i, j, arcade.color.GREEN)

        #draw starting and ending point
        self.drawRect(0, 0, arcade.color.RED)
        self.drawRect(self.maze_size - 1, self.maze_size - 1, arcade.color.RED)
                    
    #insert path to the maze
    def insertPath(self, path):
        for i in range(path.size):
            self.maze[path[i].x][path[i].y] = 2