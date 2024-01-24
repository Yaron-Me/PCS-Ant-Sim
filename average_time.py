file_names = ["20x20.txt"]  

def calculate_average_time(file_name):
    total_time = 0
    count = 0

    try:
        with open(file_name, 'r') as file:
            for line in file:
                try:
                    time_in_seconds = float(line.strip())
                    total_time += time_in_seconds
                    count += 1
                except ValueError:
                    print(f"Skipping invalid line in {file_name}: {line.strip()}")

        if count > 0:
            average_time = total_time / count
            average_time = round(average_time, 3)
            print(f"{file_name} has average time: {average_time} seconds")
        else:
            print(f"No valid time values found in {file_name}")
    except FileNotFoundError:
        print(f"File not found: {file_name}")

# Calculate and print average times for each file
for file_name in file_names:
    calculate_average_time(file_name)
