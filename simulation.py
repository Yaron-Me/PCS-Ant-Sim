import numpy as np
import time
import cv2
from ordered_set import OrderedSet

TURN_RADIUS = 20
PHEROMONE_RADIUS = 10
MAP_DIMENSIONS = (500, 500)
# Food is x, y, radius
FOODS = {(400, 240, 5)}

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

# make a 500x500 grid in numpy
mapGrid = np.zeros((MAP_DIMENSIONS[0], MAP_DIMENSIONS[1]))

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

def integer_points_on_line(x1, y1, x2, y2):
    points = []
    
    # Calculate the differences between the x and y coordinates
    dx = x2 - x1
    dy = y2 - y1

    # Determine the absolute values of the differences
    dx_abs = abs(dx)
    dy_abs = abs(dy)

    # Determine the direction of movement along the x and y axes
    sx = 1 if x1 < x2 else -1 if x1 > x2 else 0
    sy = 1 if y1 < y2 else -1 if y1 > y2 else 0

    # Initialize the decision parameters
    decision = 2 * dy_abs - dx_abs

    # Initial point
    x = x1
    y = y1

    # Add the initial point to the list
    points.append((x, y))

    # Generate intermediate points
    for _ in range(dx_abs):
        if decision >= 0:
            # Increment y for positive decision parameter
            y += sy
            decision -= 2 * dx_abs

        # Increment x and update decision parameter
        x += sx
        decision += 2 * dy_abs

        # Add the point to the list
        points.append((x, y))

    return points

# Read file maze.png
maze = cv2.imread("maze.png", cv2.IMREAD_GRAYSCALE)

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


class Simulation:
    def __init__(self, mapDimensions = (500, 500), nestCoord = (250, 250),
                 foodAmount=10, antAmount=100):
        self.mapDimensions = mapDimensions
        self.pheromones = []
        self.ants = [Ant((5, 240), (5, 240)) for _ in range(antAmount)]
        self.iteration = 0
        self.dx = 0.001

    def run(self):
        print("Running simulation")
        while True:
            
            start = time.time()
            self.updateAnts()
            self.updatePheromones()
            
            self.updateScreen()
            
            self.iteration += 1
            print(time.time() - start, self.iteration, len(Pheromones))
            time.sleep(self.dx)

    def updateScreen(self):
        mapCopy = np.copy(mapGrid)


        for pheromone in Pheromones:
            r = int(pheromone.radius * (pheromone.strength / pheromone.startStrength))
            points = points_in_circle(pheromone.x, pheromone.y, r)
            valid_points = points[(points[:, 0] < mapCopy.shape[0]) & (points[:, 1] < mapCopy.shape[1])]
            valid_points = valid_points[mapGrid[valid_points[:, 0], valid_points[:, 1]] != WALL]
            valid_points = valid_points[mapGrid[valid_points[:, 0], valid_points[:, 1]] != FOOD]
            mapCopy[valid_points[:, 0], valid_points[:, 1]] = PHEROMONE

        # Draw ants thicc
        for ant in self.ants:
            color = ANT
            if ant.hasFood:
                color = ANTWITHFOOD
                # self.dx = 0.1
            mapCopy[int(ant.x)][int(ant.y)] = color
            if not outOfBounds(int(ant.x) + 1, int(ant.y) + 1):
                mapCopy[int(ant.x) + 1][int(ant.y)] = color
                mapCopy[int(ant.x)][int(ant.y) + 1] = color
                mapCopy[int(ant.x) + 1][int(ant.y) + 1] = color


        # Convert to 3 channel image
        # unique_values = np.unique(mapCopy)
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
        self.path.insert(0, (int(self.x), int(self.y)))

        newdirection = (self.direction + np.random.randint(-TURN_RADIUS//2, TURN_RADIUS//2)) % 360
        newx = self.x + np.cos(np.radians(newdirection))
        newy = self.y + np.sin(np.radians(newdirection))

        tries = 0
        while outOfBounds(int(newx), int(newy)) or getTile(int(newx), int(newy)) == WALL:
            newdirection = np.random.randint(0, 360)
            newx = self.x + np.cos(np.radians(newdirection))
            newy = self.y + np.sin(np.radians(newdirection))
            tries += 1
            if tries > 100:
                self.backTrack()

        self.x = newx
        self.y = newy
        self.direction = newdirection

        

    def backTrack(self):
        pathLen = len(self.path)
        if pathLen != self.pathIndex:
            self.x = self.path[self.pathIndex][0]
            self.y = self.path[self.pathIndex][1]
            self.pathIndex += 1
        else:
            self.path = []
            self.pathIndex = 0
            self.hasFood = False

    def doAction(self):
        nearbyPheromones = []
        for pheromone in Pheromones:
            r = int(pheromone.radius * (pheromone.strength / pheromone.startStrength))
            if np.sqrt((self.x - pheromone.x)**2 + (self.y - pheromone.y)**2) < r:
                nearbyPheromones.append(pheromone)

        if self.hasFood:
            self.backTrack()
            if len(nearbyPheromones) == 0:
                self.dropPheromone()

        if not self.hasFood:
            if getTile(int(self.x), int(self.y)) == FOOD:
                self.hasFood = True
                self.trackedFood = False
                self.pathToFood = []
                setTile(int(self.x), int(self.y), EMPTY)
                return
            
            if self.trackedFood == False:
                if self.pathToFood == [] and len(nearbyPheromones) > 0:
                    self.pathToFood = nearbyPheromones[0].pathToFood
                    # self.path = nearbyPheromones[0].takeOverPath
                    self.trackedFood = True
                else:
                    self.wander()
            else:
                if len(self.pathToFood) > 0:
                    self.walkToFood()
                else:
                    self.trackedFood = False
                    self.wander()

    def walkToFood(self):
        (x, y) = self.pathToFood[0]

        # print("pathToFood: ", self.pathToFood)

        distance = np.sqrt((self.x - x)**2 + (self.y - y)**2)

        # print("Current: ", (self.x, self.y))
        # print("Target: ", (x, y))
        # print("Distance: ", distance)

        self.direction = np.degrees(np.arctan2(y - self.y, x - self.x))
        
        if distance <= 1:
            # print("Reached point!")
            self.pathToFood.remove((x, y))
            self.x = x
            self.y = y
        else:
            # Move towards food
            stepx = (x - self.x) / distance
            stepy = (y - self.y) / distance
            self.x += stepx
            self.y += stepy

        self.path.insert(0, (int(self.x), int(self.y)))

    def dropPheromone(self):
        pathToBase = self.path[self.pathIndex:]

        pathToFood = self.path[0:self.pathIndex]
        pathToFood.reverse()
        Pheromones.append(Pheromone((int(self.x), int(self.y)), pathToFood, pathToBase))

class Pheromone:
    def __init__(self, coord, pathToFood, takeOverPath, radius=PHEROMONE_RADIUS):
        self.x = coord[0]
        self.y = coord[1]
        self.strength = 800
        self.startStrength = self.strength
        self.pathToFood = pathToFood
        # self.takeOverPath = takeOverPath

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

        if lowest_radius < 5:
            self.strength = 0

        self.radius = lowest_radius

    def update(self):
        self.strength -= 1
        if self.strength <= 0:
            Pheromones.remove(self)




sim = Simulation()
sim.run()