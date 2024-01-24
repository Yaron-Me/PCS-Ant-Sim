import matplotlib.pyplot as plt

# 1) Total time, 2) First ant found food time, 3) Retrieval time after first food is found
# Still need to fill in values manually, can make it automatic
file_data = [
    ("20x20", 48.123, 15.678, 33.890), 
    ("15x15", 40.456, 12.765, 28.012),  
]

file_names = [data[0] for data in file_data]
total_times = [data[1] for data in file_data]
first_ant_times = [data[2] for data in file_data]
retrieval_times = [data[3] for data in file_data]

bar_width = 0.2
index = range(len(file_names))

plt.figure(figsize=(12, 6))
plt.bar(index, total_times, bar_width, label='Total Time', color='skyblue')
plt.bar([i + bar_width for i in index], first_ant_times, bar_width, label='First Ant Found Time', color='lightcoral')
plt.bar([i + 2 * bar_width for i in index], retrieval_times, bar_width, label='Retrieval Time After Food Found Time', color='lightgreen')

plt.xlabel('Maze size')
plt.ylabel('Time (seconds)')
plt.title('Ant colony food retrieval')
plt.xticks([i + bar_width for i in index], file_names)
plt.legend()

plt.tight_layout()
plt.show()
