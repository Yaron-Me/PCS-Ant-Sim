file_names = ["20x20.txt"]  

def calculate_average_time(file_name):
    total_time_1 = 0
    total_time_2 = 0
    total_time_3 = 0
    count = 0

    try:
        with open(file_name, 'r') as file:
            for line in file:
                try:
                    values = line.strip().split()
                    if len(values) != 3:
                        raise ValueError("Too much columns")

                    column1 = float(values[0])
                    column2 = float(values[1])
                    column3 = float(values[2])

                    total_time_1 += column1
                    total_time_2 += column2
                    total_time_3 += column3

                    count += 1
                except ValueError as e:
                    print(f"Skipping invalid line: {line.strip()}. Error: {e}")

        if count > 0:
            average_column1 = total_time_1 / count
            average_column2 = total_time_2 / count
            average_column3 = total_time_3 / count

            # Round the averages to 3 decimal places
            average_column1 = round(average_column1, 3)
            average_column2 = round(average_column2, 3)
            average_column3 = round(average_column3, 3)

            # Print the averages with appropriate labels
            print(f"Results of {file_name}:")
            print(f"Average time total food retrieval: {average_column1} seconds")
            print(f"Average time first ant found food: {average_column2} seconds")
            print(f"Average time total food retrieval after found is found: {average_column3} seconds")
        else:
            print("No valid time values found in the file.")

    except FileNotFoundError:
        print(f"File not found: {file_name}")

# Calculate and print average times for each file
for file_name in file_names:
    calculate_average_time(file_name)
