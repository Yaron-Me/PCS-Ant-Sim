import subprocess

#Number of simulations
N = 2

for i in range(N):
    subprocess.run(["python3", "simulation.py"], stdout=open("20x20.txt", "a"))

print(f"{N} simulations completed.")
