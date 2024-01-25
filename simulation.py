import numpy as np
import time
import cv2


# changealbe parameters
NUMBER_OF_ANTS = 100
MAZE = "mazes/maze20x20.png"
PHEROMONE_DECAY_RATE = 800 # in miliseconds
WALKING_SPEED = 0.001

# other parameters
TURN_RADIUS = 20
PHEROMONE_RADIUS = 10
MAP_DIMENSIONS = (500, 500)

# Food is x, y, radius
FOODS = {(120, 240, 5)}
global number_of_foods
global start_number_of_foods
global first_food

Pheromones = []

EMPTY = 0 # white
WALL = 1 # black
FOOD = 2 # green
ANT = 3 # black
PHEROMONE = 4 # black
ANTWITHFOOD = 5 # red

colormap = {
    EMPTY: [255, 255, 255],  # white
    WALL: [0, 0, 0],  # black
    FOOD: [0, 255, 0],  # green
    ANT: [0, 0, 0],  # Black
    PHEROMONE: [255, 0, 0],  # blue
    ANTWITHFOOD: [0, 0, 255]  # red
}

# Copy of the map with just the pheromnes and walls, no ants
mapCopyPheromones = np.zeros((MAP_DIMENSIONS[0], MAP_DIMENSIONS[1], 1), dtype=np.uint8)

# make a 500x500 grid in numpy
mapGrid = np.zeros((MAP_DIMENSIONS[0], MAP_DIMENSIONS[1]))

# This returns a list of points within a circle
def points_in_circle(x, y, radius):
    # Generate a grid of integer points within a bounding box around the circle
    x_range = np.arange(int(x - radius), int(x + radius) + 1)
    y_range = np.arange(int(y - radius), int(y + radius) + 1)

    # Create a meshgrid of all possible combinations of x and y
    x_grid, y_grid = np.meshgrid(x_range, y_range)

    # Calculate the distance from each point to the center of the circle
    distance = np.sqrt((x_grid - x)**2 + (y_grid - y)**2)

    # Use boolean indexing to filter points within the circle
    points_within_circle = np.column_stack((x_grid[distance <= radius].ravel(), y_grid[distance <= radius].ravel()))

    return points_within_circle

def getTile(x, y):
    return mapGrid[x][y]

def setTile(x, y, value):
    mapGrid[x][y] = value

def outOfBounds(x, y):
    if x < 0 or x >= MAP_DIMENSIONS[0] or \
       y < 0 or y >= MAP_DIMENSIONS[1]:
        return True
    return False

# Read file maze.png
maze = cv2.imread(MAZE, cv2.IMREAD_GRAYSCALE)

# Rescale to 500x500
maze = cv2.resize(maze, MAP_DIMENSIONS)

# For each black pixel, set the corresponding grid cell to WALL
for i in range(maze.shape[0]):
    for j in range(maze.shape[1]):
        if maze[i][j] < 255:
            mapGrid[i][j] = WALL

# For each food, set the corresponding grid cells to FOOD
for food in FOODS:
    x, y, r = food
    points = points_in_circle(x, y, r)
    valid_points = points[(points[:, 0] < mapGrid.shape[0]) & (points[:, 1] < mapGrid.shape[1])]
    # Set food where there are no walls
    valid_points = valid_points[mapGrid[valid_points[:, 0], valid_points[:, 1]] != WALL]
    mapGrid[valid_points[:, 0], valid_points[:, 1]] = FOOD
    number_of_foods = len(valid_points)
    start_number_of_foods = number_of_foods


class Simulation:
    def __init__(self, mapDimensions = (500, 500), antAmount=NUMBER_OF_ANTS):
        self.mapDimensions = mapDimensions
        self.pheromones = []
        self.ants = [Ant((5, 240), (5, 240)) for _ in range(antAmount)]
        self.iteration = 0
        self.first_food = 0
        self.dx = 0.001
        self.visualization = False

    def set_iteration(self):
        self.first_food = self.iteration

    def run(self):
        start_time = time.time()
        while True:

            # Make all the ants do an action
            self.updateAnts()
            # lower strength of all pheromones
            self.updatePheromones()

            mapCopy = np.copy(mapGrid)

            # draw pheromones into map (blue circles)
            for pheromone in Pheromones:
                r = int(pheromone.radius * (pheromone.strength / pheromone.startStrength))
                points = points_in_circle(pheromone.x, pheromone.y, r)
                valid_points = points[(points[:, 0] < mapCopy.shape[0]) & (points[:, 1] < mapCopy.shape[1])]
                valid_points = valid_points[mapGrid[valid_points[:, 0], valid_points[:, 1]] != WALL]
                valid_points = valid_points[mapGrid[valid_points[:, 0], valid_points[:, 1]] != FOOD]
                mapCopy[valid_points[:, 0], valid_points[:, 1]] = PHEROMONE

            global mapCopyPheromones
            mapCopyPheromones = np.copy(mapCopy)
            
            if self.visualization == True:
                # Update the screen, so draw ants and draw to screen
                self.updateScreen()
                time.sleep(self.dx)

            self.iteration += 1

            global number_of_foods
            if number_of_foods == 0:
                # realtime
                # total_realtime = (time.time() - start_time)
                # first_food_realtime = (first_food - start_time)
                # realtime_to_bring_food = (total_realtime - first_food_realtime)
                # print("realtime: ", total_realtime, first_food_realtime, realtime_to_bring_food)

                # iterations
                print(round((self.iteration / WALKING_SPEED), 2), round((self.first_food / WALKING_SPEED), 2), round((self.iteration - self.first_food) / WALKING_SPEED, 2))
                exit()

                exit()

    def updateScreen(self):
        mapCopy = np.copy(mapCopyPheromones)


        # Draw ants as 2x2 squares
        for ant in self.ants:
            color = ANT
            if ant.hasFood:
                color = ANTWITHFOOD
            mapCopy[int(ant.x)][int(ant.y)] = color
            if not outOfBounds(int(ant.x) + 1, int(ant.y) + 1):
                mapCopy[int(ant.x) + 1][int(ant.y)] = color
                mapCopy[int(ant.x)][int(ant.y) + 1] = color
                mapCopy[int(ant.x) + 1][int(ant.y) + 1] = color


        # Convert to 3 channel image
        # Change single values to rgb values
        unique_values = np.array(list(colormap.keys()))
        rgb_lookup = np.array([colormap[val] for val in unique_values])
        colored_data = rgb_lookup[np.digitize(mapCopy, unique_values) - 1].astype(np.uint8)

        cv2.imshow("Simulation", colored_data)
        cv2.waitKey(1)

    def updateAnts(self):
        for ant in self.ants:
            ant.doAction()

    def updatePheromones(self):
        for pheromone in Pheromones:
            pheromone.update()

class Ant:
    def __init__(self, coord, nest):
        self.x = coord[0]
        self.y = coord[1]
        self.direction = np.random.randint(0, 360)
        self.path = []
        self.pathIndex = 0
        self.hasFood = False
        self.pathToFood = []
        self.trackedFood = False

    def wander(self):
        # Check if the ant has already been at this location,
        # If so shorten the path it has taken
        try:
            test = self.path.index((int(self.x), int(self.y)))
            self.path = self.path[:test]
        except ValueError:
            self.path.append((int(self.x), int(self.y)))

        newdirection = (self.direction + np.random.randint(-TURN_RADIUS//2, TURN_RADIUS//2)) % 360
        newx = self.x + np.cos(np.radians(newdirection))
        newy = self.y + np.sin(np.radians(newdirection))

        tries = 0
        while outOfBounds(int(newx), int(newy)) or getTile(int(newx), int(newy)) == WALL:
            newdirection = np.random.randint(0, 360)
            newx = self.x + np.cos(np.radians(newdirection))
            newy = self.y + np.sin(np.radians(newdirection))
            tries += 1
            # If ant cannot seem to get out of a wall, backtrack
            if tries > 100:
                self.backTrack()

        self.x = newx
        self.y = newy
        self.direction = newdirection



    def backTrack(self):
        # This makes the ants take its recorded path back
        pathLen = len(self.path)
        if pathLen != self.pathIndex:
            self.pathIndex += 1
            self.x = self.path[pathLen - self.pathIndex][0]
            self.y = self.path[pathLen - self.pathIndex][1]
        else:
            self.path = []
            self.pathIndex = 0
            self.hasFood = False
            # decrease value of number of foods
            global number_of_foods
            number_of_foods -= 1


    def doAction(self):
        # Get all the pheromones that are within the reach of an ant
        nearbyPheromones = []
        if (mapCopyPheromones[int(self.x)][int(self.y)] == PHEROMONE) and not self.hasFood and not self.trackedFood:
            for pheromone in Pheromones:
                r = int(pheromone.radius * (pheromone.strength / pheromone.startStrength))
                if np.sqrt((self.x - pheromone.x)**2 + (self.y - pheromone.y)**2) < r:
                    nearbyPheromones.append(pheromone)

        # Go back to the nest if the ant has food
        if self.hasFood:
            self.backTrack()
            if mapCopyPheromones[int(self.x)][int(self.y)] != PHEROMONE:
                self.dropPheromone()


        if not self.hasFood:
            # If the ant is on a tile with food, pick it up
            if getTile(int(self.x), int(self.y)) == FOOD:
                if number_of_foods == start_number_of_foods:
                    global first_food
                    first_food = time.time()
                    sim.set_iteration()
                self.hasFood = True
                self.trackedFood = False
                self.pathToFood = []
                setTile(int(self.x), int(self.y), EMPTY)
                return

            # If the ant was not following a pheromone, wander or try to find a pheromone
            if self.trackedFood == False:
                if self.pathToFood == [] and len(nearbyPheromones) > 0:
                    self.pathToFood = nearbyPheromones[0].pathToFood
                    self.trackedFood = True
                else:
                    self.wander()
            else:
                # If the ant is following a pheromone, follow it
                if len(self.pathToFood) > 0:
                    self.walkToFood()
                else:
                    self.trackedFood = False
                    self.wander()

    # Follow the path to the food given by a pheromone
    def walkToFood(self):
        (x, y) = self.pathToFood[0]

        distance = np.sqrt((self.x - x)**2 + (self.y - y)**2)

        self.direction = np.degrees(np.arctan2(y - self.y, x - self.x))

        if distance <= 1:
            self.pathToFood.remove((x, y))
            self.x = x
            self.y = y
        else:
            # Move towards food
            stepx = (x - self.x) / distance
            stepy = (y - self.y) / distance
            self.x += stepx
            self.y += stepy

        # Check if the ant has already been at this location, if so shorten the path it has taken
        try:
            test = self.path.index((int(self.x), int(self.y)))
            self.path = self.path[:test]
        except ValueError:
            self.path.append((int(self.x), int(self.y)))

    # Drop a pheromone at the current location
    def dropPheromone(self):
        pathToFood = self.path[len(self.path) - self.pathIndex:]
        pathToBase = []
        Pheromones.append(Pheromone((int(self.x), int(self.y)), pathToFood, pathToBase))

class Pheromone:
    def __init__(self, coord, pathToFood, takeOverPath, radius=PHEROMONE_RADIUS):
        self.x = coord[0]
        self.y = coord[1]
        self.strength = PHEROMONE_DECAY_RATE
        self.startStrength = self.strength
        self.pathToFood = pathToFood

        # Check if wall is within radius
        xrange = np.arange(int(self.x - radius), int(self.x + radius) + 1)
        yrange = np.arange(int(self.y - radius), int(self.y + radius) + 1)

        # make sure it's within bounds
        xrange = xrange[xrange >= 0]
        xrange = xrange[xrange < MAP_DIMENSIONS[0]]
        yrange = yrange[yrange >= 0]
        yrange = yrange[yrange < MAP_DIMENSIONS[1]]

        # Check if wall is within radius
        lowest_radius = PHEROMONE_RADIUS
        for x in xrange:
            for y in yrange:
                if getTile(x, y) == WALL:
                    distance = np.sqrt((self.x - x)**2 + (self.y - y)**2)
                    if distance < lowest_radius:
                        lowest_radius = distance

        # If the space to drop a pheromone is too small, don't drop it
        if lowest_radius < 5:
            self.strength = 0

        self.radius = lowest_radius

    def update(self):
        self.strength -= 1
        if self.strength <= 0:
            Pheromones.remove(self)




sim = Simulation()
sim.run()
