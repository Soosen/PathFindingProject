import arcade
class Maze:
    def __init__(self, maze, width):
        self.original_maze = maze
        self.maze = maze
        self.maze_size = self.maze[0].size
        self.maze_width = width
        self.tile_size = self.maze_width / (self.maze_size + 2)



    def updateMaze(self, maze):
        self.maze = maze

    def resetMaze(self):
        self.maze = self.original_maze

    def drawRect(self, x , y, color):
        arcade.draw_rectangle_filled(3*self.tile_size/2 + x * self.tile_size, 3*self.tile_size/2 + y * self.tile_size, self.tile_size, self.tile_size, color)

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
                if(self.maze[i][j] == 0):
                    self.drawRect(i, j, arcade.color.BLACK)
                elif(self.maze[i][j] == 2):
                    self.drawRect(i, j, arcade.color.BLUE)
                elif(self.maze[i][j] == 3):
                    self.drawRect(i, j, arcade.color.GREEN)

        #draw starting and ending point
        self.drawRect(0, 0, arcade.color.RED)
        self.drawRect(self.maze_size - 1, self.maze_size - 1, arcade.color.RED)
                    

    def drawPath(self, path):
        for i in range(path.size):
            self.maze[path[i].x][path[i].y] = 2