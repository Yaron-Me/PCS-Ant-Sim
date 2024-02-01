# This script plots the average time taken to reach each criteria for different ant colony sizes

import matplotlib.pyplot as plt
import numpy as np

plt.rc('font', size=18)

antamounts = ["10", "25", "50", "100", "500", "1000"]

# Create subplots for totals, firstfood, and differences
fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)

maze_sizes = ["10x10", "15x15", "20x20"]

for idx, (ax, data_type) in enumerate(zip(axes, ["Total time to gather all food", "Total time to find first piece of food", "Time to gather all food after finding it"])):
    for mazesize in maze_sizes:
        data_list = []

        for antsize in antamounts:
            filename = f"results/{antsize}_{mazesize}.txt"

            with open(filename, "r") as f:
                data = []
                lines = f.readlines()
                for line in lines:
                    [total, firstfood, difference] = map(float, line.split(" "))
                    if data_type == "Total time to gather all food":
                        data.append(total)
                    elif data_type == "Total time to find first piece of food":
                        data.append(firstfood)
                    elif data_type == "Time to gather all food after finding it":
                        data.append(difference)

                data_list.append(data)

        data_array = np.array(data_list)
        # convert from seconds to hours
        data_array /= 3600
        avg_data = np.average(data_array, axis=1)
        std_dev = np.std(data_array, axis=1)

        # Create line plot with error bars for each maze size and data type
        ant_sizes = np.arange(1, len(antamounts) + 1)
        ax.errorbar(ant_sizes, avg_data, yerr=std_dev, label=f"Maze Size: {mazesize}", marker='o', capsize=5)

    # Set labels and title for each subplot
    ax.set_xticks(ant_sizes)
    ax.set_xticklabels(antamounts)
    ax.set_xlabel("Ant Colony Size")
    ax.set_ylabel("Time in hours")
    ax.set_title(f"{data_type.capitalize()}")
    ax.legend()

# Adjust layout
plt.tight_layout()
plt.show()
