import subprocess
import threading

RUNS = 14
AVAILABLE_THREADS = 10
outputfile = "output.txt"

def run_simulation():
    output = subprocess.run(["python3", "simulation.py", "100", "10"], capture_output=True)
    decoded_output = output.stdout.decode("utf-8")
    # Write output to file
    with open(outputfile, "a") as f:
        f.write(decoded_output)

if __name__ == "__main__":
    inactive_threads = []
    active_threads = []
    for i in range(RUNS):
        thread = threading.Thread(target=run_simulation)
        thread.daemon = True
        inactive_threads.append((thread, i))


    while True:
        if len(active_threads) < AVAILABLE_THREADS and len(inactive_threads) > 0:
            (thread, i) = inactive_threads.pop(0)
            active_threads.append((thread, i))
            thread.start()
            print(f"Started simulation {i + 1}")
        else:
            for (thread, i) in active_threads:
                if not thread.is_alive():
                    active_threads.remove((thread, i))
                    print(f"Finished simulation {i + 1}")
                    break

        if len(inactive_threads) == 0 and len(active_threads) == 0:
            break