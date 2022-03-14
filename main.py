import arcade
from mazeGenerator import MazeGenerator
from maze import Maze
from pathFinder import PathFinder
import sys
import numpy

SCREEN_WIDTH = 800
SCREEN_HEIGHT = SCREEN_WIDTH
SCREEN_TITLE = "Path Finding Project"


class MyProject(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.GRAY)

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
            #temp
        sys.setrecursionlimit(30000)
        self.set_update_rate(1/60)
        mazeGen = MazeGenerator(30, SCREEN_WIDTH)
        mazeMap = mazeGen.generateMaze()
        self.maze = Maze(mazeMap, SCREEN_WIDTH)
        self.pf = PathFinder(mazeMap)
        self.path, self.visited = self.pf.depth_first_search()        
        pass

    def on_draw(self):
        """
        Render the screen.
        """                             
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()
        arcade.start_render()
        self.maze.draw()
        arcade.finish_render()

        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
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

        if key == arcade.key.R:
            mazeGen = MazeGenerator(30, SCREEN_WIDTH)
            mazeMap = mazeGen.generateMaze()
            self.maze = Maze(mazeMap, SCREEN_WIDTH)
            self.pf = PathFinder(mazeMap)
            self.path, self.visited = self.pf.depth_first_search() 

        pass

def main():
    """ Main function """
    project = MyProject(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    project.setup()

    arcade.run()




if __name__ == "__main__":
    main()