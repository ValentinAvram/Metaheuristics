import random
import math

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
    print("Length of the route: ", lengthTravel)
    print("Temperature: ", t)

    it=0
    while t > 0.05:
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
        t=0.99*t
        print("Length of the route: ", lengthTravel)
        print("Temperature: ", t)
    return solution, lengthTravel

def main():
    data = [
        [0, 400, 500, 300],
        [400, 0, 300, 500],
        [500, 300, 0, 400],
        [300, 500, 400, 0]
    ]
    t0=10

    s=simAnnealing(data,t0)
    print("--------------")
    print("Final solution: ",s[0])
    print("Length of the final route: ",s[1])

if __name__ == "__main__":
    main()
