import random
import math
import time


def evaluateSolution(data, solution):
    lengthTravel = 0
    for i in range(len(solution)):
        lengthTravel += data[solution[i - 1]][solution[i]]
    return lengthTravel

def getNeighbor(solution, data):
    ##Get the neighbors
    neighbors = []
    l=len(solution)
    for i in range(l):
        for j in range(i+1, l):
            n = solution.copy()
            n[i] = solution[j]
            n[j] = solution[i]
            neighbors.append(n)

    ##Get a random neighbor
    neighbor=neighbors[random.randint(0, len(neighbors) - 1)]
    lengthTravel = evaluateSolution(data, neighbor)

    return neighbor, lengthTravel

def simAnnealing(data,t0):
    t=t0
    l=len(data)
    ##Generate a random solution
    cities = list(range(l))
    solution = []
    for i in range(l):
        ciudad = cities[random.randint(0, len(cities) - 1)]
        solution.append(ciudad)
        cities.remove(ciudad)
    lengthTravel = evaluateSolution(data, solution)
    #print("Length of the route: ", lengthTravel)
    #print("Temperature: ", t)

    it=0
    while t > 0.05: #CHANGE THIS AS WE WANT
        ##Get a random neighbor
        neighbor = getNeighbor(solution, data)
        increment = neighbor[1]-lengthTravel

        if increment < 0:
            lengthTravel = neighbor[1]
            solution = neighbor[0]
        elif random.random() < math.exp(-abs(increment) / t):
            lengthTravel = neighbor[1]
            solution = neighbor[0]

        it+=1
        #Cooling function CHANGE THIS AS WE WANT
        alpha = 0.99 #Cooling rate, CHANGE THIS AS WE WANT
        # t = alpha*t
        # t = (alpha*t0) / log(it+1)
        t = (alpha**it) * t0

        #print("Length of the route: ", lengthTravel)
    print("Temperature: ", t)
    return solution, lengthTravel

def main():

    data = []

    # EACH DATASET HAS AN OPTIMAL SOLUTION
    # five_d.txt = 19 || p01_d.txt= 291 || dantzig42_d.txt = 699 || fri26_d.txt = 937 || gr17_d.txt = 2085 || att48_d.txt = 33523

    optimalCost = 291 # CHANGE THIS FOR EACH DATASET

    # Read the data from a file filled with float numbers
    with open("Datasets/p01_d.txt", "r") as f:
        for line in f:
            data.append([int(x) for x in line.split()])

    t0=10  # CHANGE THIS AS WE WANT

    iterations = 10
    optimalSol = 0

    for i in range(iterations):

        print("--------------")

        start_time = time.time()
        s = simAnnealing(data, t0)

        print("Final solution: ", s[0])
        print("Final route length: ", s[1])

        print("Runtime: %s seconds" % (time.time() - start_time))

        if (s[1] == optimalCost):
            print("Optimal solution found")
            optimalSol += 1
            break
        print("--------------\n")

    print("Number of optimal solutions found: ", optimalSol, " / ", i + 1)

if __name__ == "__main__":
    main()
