# Ant simulation
A simple ant simulation in a maze.

## Introduction

## Usage
### Executing the simulation
`python3 simualtion.py <number of ants> <maze size>`
### Example
`python3 simualtion.py 100 10`

### Generate your own maze
Go to [this](https://mazegenerator.net) site and download the generated maze.

## Parameters
The parameters used:
-  Ant colony size
-  Walking speed of ants
-  Pheromone decay rate (different terrains)
-  Maze difficulty (size of maze)

## Tests
The tests run on the simulation:
- **Tests are run on mazes of sizes:** 10x10, 15x15, 20x20
- **Tests are run with different number of total ants:** 10, 50, 100, 500, 1000
- **Every test case is run 100 times**

### Collected Data
- Average time for the first ant to discover the food.
- Average time for all the food to be brought back to the nest.
- Average time between the first ant discovering the food and the last ant bringing the food back to the nest.
- Average number of ants that discover the food and bring it back to the nest.
