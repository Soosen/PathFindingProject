import arcade
from mazeGenerator import MazeGenerator
from maze import Maze
from pathFinder import PathFinder
import sys
import numpy
import pyglet

SCREEN_WIDTH = 800
SCREEN_HEIGHT = SCREEN_WIDTH
SCREEN_TITLE = "Path Finding Project"

#Maze is a square with MAZE_SIZE x MAZE_SIZE tiles
MAZE_SIZE = 30
UPDATE_RATE = 1/60

#chosen Monitor
MONITOR_NUM = 0
MONITORS = pyglet.canvas.Display().get_screens()
MONITOR = MONITORS[MONITOR_NUM]


class MyProject(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.GRAY)

    def setup(self):

        #increase recursion limit
        sys.setrecursionlimit(30000)

        #set fps
        self.set_update_rate(UPDATE_RATE)

        #center the window on start
        self.center_on_screen()

        #generate maze
        mazeGen = MazeGenerator(MAZE_SIZE, SCREEN_WIDTH)
        mazeMap = mazeGen.generateMaze()
        self.maze = Maze(mazeMap, SCREEN_WIDTH)

        #init path finder
        self.pf = PathFinder(mazeMap)

        #init self.visited and self.path
        self.visited = numpy.array([])
        self.path = numpy.array([])       
        pass

    def on_draw(self):
        #draw the maze
        self.clear()
        arcade.start_render()
        self.maze.draw()
        arcade.finish_render()


    def on_update(self, delta_time):

        #visualize path and visited cells by setting values of the maze to 3 for visited and 2 for path
        if(self.visited.size >= 2):
            for i in range (2):
                self.maze.maze[self.visited[0].x][self.visited[0].y] = 3
                self.visited = numpy.delete(self.visited, 0)
        else:
            if(self.path.size >= 2):
                self.maze.maze[self.path[1].x][self.path[1].y] = 2
                self.path = numpy.delete(self.path, 0)
        pass

    def on_key_press(self, key, key_modifiers):

        #Key R - generate new maze
        if key == arcade.key.R:
            mazeGen = MazeGenerator(MAZE_SIZE, SCREEN_WIDTH)
            mazeMap = mazeGen.generateMaze()
            self.maze = Maze(mazeMap, SCREEN_WIDTH)
            self.pf = PathFinder(mazeMap)
            self.path = numpy.array([])
            self.visited = numpy.array([])
        elif(key == arcade.key.KEY_1):
            #Key 1 visualize breadth first search
            self.maze.resetMaze()
            self.path, self.visited = self.pf.breadth_first_search()
        elif(key == arcade.key.KEY_2):
            #Key 2 visualize depth first search
            self.maze.resetMaze()
            self.path, self.visited = self.pf.depth_first_search(MAZE_SIZE*MAZE_SIZE)
        elif(key == arcade.key.KEY_3):
            #Key 3 visualize iterative depth first search
            self.maze.resetMaze()
            self.path, self.visited = self.pf.iterative_depth_first_search(MAZE_SIZE, MAZE_SIZE*MAZE_SIZE)
        elif(key == arcade.key.KEY_4):
            #Key 4 visualize A* search
            self.maze.resetMaze()
            self.path, self.visited = self.pf.AStar()
        elif(key == arcade.key.KEY_5):
            #Key 5 visualize bidirectional breadth first search
            self.maze.resetMaze()
            self.path, self.visited = self.pf.bidirectional_breadth_first_search()


        pass

    def center_on_screen(self):
        _left = MONITOR.width // 2 - self.width // 2
        _top = (MONITOR.height // 2 - self.height // 2)
        self.set_location(_left, _top)

def main():
    project = MyProject(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    project.setup()

    arcade.run()




if __name__ == "__main__":
    main()