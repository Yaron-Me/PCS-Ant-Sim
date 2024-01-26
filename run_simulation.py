import subprocess
import threading
import playsound

RUNS = 0
AVAILABLE_THREADS = 15
MAZE_SIZE = "10"
ANT_AMOUNT = "10"
OUTPUT_FILE = ANT_AMOUNT + "_" + MAZE_SIZE + "x" + MAZE_SIZE + ".txt"

def run_simulation():
    output = subprocess.run(["python3", "simulation.py", ANT_AMOUNT, MAZE_SIZE], capture_output=True)
    decoded_output = output.stdout.decode("utf-8")
    # Write output to file
    with open(OUTPUT_FILE, "a") as f:
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

    # Play a sound to notify that the simulation is done
    playsound.playsound("alarm.mp3")