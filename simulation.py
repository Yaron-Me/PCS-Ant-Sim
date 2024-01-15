import numpy as np
import tkinter as tk
import time

MAP_DIMENSIONS = (500, 500)

class Ant:
    # Constructor
    def __init__(self):
        self.x = MAP_DIMENSIONS[0] // 2
        self.y = MAP_DIMENSIONS[1] // 2
        self.direction = np.random.randint(0, 360)
        self.hasFood = False
        self.foodLocation = None
        self.smelledPheromone = False

    # Wander
    def wander(self):
        if not self.hasFood:
            if self.smelledPheromone:
                # calculate direction to food
                self.direction = np.degrees(np.arctan2(self.foodLocation[1] - self.y, self.foodLocation[0] - self.x))
            else:
                self.direction += np.random.randint(-5, 5)
                self.direction %= 360

            self.x += np.cos(np.radians(self.direction))
            self.y += np.sin(np.radians(self.direction))

            while self.outOfBounds():
                self.direction += 180
                self.direction %= 360

                self.x += np.cos(np.radians(self.direction))
                self.y += np.sin(np.radians(self.direction))

            # Check if ant is on food
            for i in range(len(Foods)):
                if (self.x - Foods[i].x) ** 2 + (self.y - Foods[i].y) ** 2 <= Foods[i].amount ** 2:
                    self.hasFood = True
                    self.smelledPheromone = False
                    self.foodLocation = (Foods[i].x, Foods[i].y)
                    Foods[i].amount -= 1
                    if Foods[i].amount <= 0:
                        # Remove food
                        Foods.pop(i)
                        break

            # Check if ant is on foodLocation
            if self.foodLocation is not None and not self.hasFood:
                if (self.x - self.foodLocation[0]) ** 2 + (self.y - self.foodLocation[1]) ** 2 <= 10 ** 2:
                    self.hasFood = False
                    self.smelledPheromone = False
                    self.foodLocation = None

        else:
            # Check if ant is close to other ants
            for i in range(len(Ants)):
                if not Ants[i].smelledPheromone and not Ants[i].hasFood and (self.x - Ants[i].x) ** 2 + (self.y - Ants[i].y) ** 2 <= 10 ** 2:
                    Ants[i].smelledPheromone = True
                    Ants[i].foodLocation = self.foodLocation
                    break

            # calculate direction to nest
            self.direction = np.degrees(np.arctan2(Nest[1] - self.y, Nest[0] - self.x))
            # Move towards nest
            self.x += np.cos(np.radians(self.direction))
            self.y += np.sin(np.radians(self.direction))

            # Check if ant is on nest
            if (self.x - Nest[0]) ** 2 + (self.y - Nest[1]) ** 2 <= 10 ** 2:
                self.hasFood = False
                self.smelledPheromone = False
                self.foodLocation = None


    def outOfBounds(self):
        if self.x < 0 or self.x > 500 or self.y < 0 or self.y > 500:
            return True
        else:
            return False

class Food:
    def __init__(self):
        self.x = np.random.randint(0, 500)
        self.y = np.random.randint(0, 500)
        self.amount = np.random.randint(1, 10)




Nest = (250, 250)
Ants = [Ant() for i in range(100)]
Foods = [Food() for i in range(10)]

root = tk.Tk()

map = tk.Canvas(root, width=500, height=500)
map.pack()

for i in range(100):
    map.create_rectangle(Ants[i].x, Ants[i].y, Ants[i].x + 1, Ants[i].y + 1, fill="black")


while True:
    map.delete("all")
    for i in range(100):
        Ants[i].wander()
        map.create_rectangle(Ants[i].x, Ants[i].y, Ants[i].x + 1, Ants[i].y + 1, fill="black")
        if (Ants[i].hasFood):
            # Draw oval with opacity 0.5
            map.create_oval(Ants[i].x - 5, Ants[i].y - 5, Ants[i].x + 5, Ants[i].y + 5, fill="black", outline="", stipple="gray50")

    for i in range(len(Foods)):
        map.create_oval(Foods[i].x - Foods[i].amount, Foods[i].y - Foods[i].amount, Foods[i].x + Foods[i].amount, Foods[i].y + Foods[i].amount, fill="green")
    # Draw nest
    map.create_oval(Nest[0] - 10, Nest[1] - 10, Nest[0] + 10, Nest[1] + 10, fill="red")

    root.update()
    time.sleep(0.01)