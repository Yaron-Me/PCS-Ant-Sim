import matplotlib
import matplotlib.pyplot as plt
import numpy as np

plt.rc('font', size=20)

filenames = []

antamounts = ["10", "25", "50", "100", "500", "1000"]

# Create subplots for each maze size
fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

maze_sizes = ["10x10", "15x15", "20x20"]

for idx, mazesize in enumerate(maze_sizes):
    totalstimes = []

    for antsize in antamounts:
        filename = "results/" + antsize + "_" + mazesize + ".txt"

        with open(filename, "r") as f:
            totals = []

            lines = f.readlines()
            for line in lines:
                [total, _, _] = line.split(" ")
                totals.append(float(total))

            totals = np.array(totals)

            totalstimes.append(totals)

    totalstimes = np.array(totalstimes)
    # convert from seconds to hours
    totalstimes /= 3600
    avgtimes = np.average(totalstimes, axis=1)
    print(mazesize, avgtimes)
    std_err = np.std(totalstimes, axis=1) / np.sqrt(totalstimes.shape[1])

    # Create violin plot on each subplot
    axes[idx].violinplot(totalstimes.T, showmeans=True)
    axes[idx].set_xticks(np.arange(1, len(antamounts) + 1))
    axes[idx].set_xticklabels(antamounts)
    axes[idx].set_xlabel("Ant Colony Size")
    axes[idx].set_ylabel("Time in hours")
    axes[idx].set_title(f"Maze Size: {mazesize}")

    # Add error bars for standard error
    for i, (avg, err) in enumerate(zip(avgtimes, std_err)):
        axes[idx].errorbar(i + 1, avg, yerr=err, fmt='none', color='black', capsize=5)

# Adjust layout
plt.tight_layout()
plt.suptitle("Violin Plots of Average Time with Standard Error for Different Maze Sizes", y=1.05)
plt.show()
