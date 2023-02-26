import random
import time

def perturbSolution(solution):
    n = len(solution)
    i = random.randint(0, n - 1)
    j = random.randint(0, n - 1)
    solution[i], solution[j] = solution[j], solution[i]
    return solution

def evaluateSolution(data, solution):
    lengthTravel = 0
    for i in range(len(solution)):
        lengthTravel += data[solution[i - 1]][solution[i]]
    return lengthTravel

def localSearch(initialSolution, data):
    routeLength = evaluateSolution(data, initialSolution)
    solution = initialSolution
    neighbor = getBestNeighborLS(solution, data)
    while neighbor[1] < routeLength:
        solution = neighbor[0]
        routeLength = neighbor[1]
        neighbor = getBestNeighborLS(solution, data)
    return solution, routeLength

def getBestNeighborLS(solution, data):
    bestLength = evaluateSolution(data, solution)
    bestNeighbor = solution
    nIter = 100  # number of local search iterations
    for i in range(nIter):
        neighbor = perturbSolution(solution.copy())
        neighbor = localSearch(neighbor, data)
        neighborLength = evaluateSolution(data, neighbor)
        if neighborLength < bestLength:
            bestLength = neighborLength
            bestNeighbor = neighbor
    return bestNeighbor, bestLength


def hillClimbingILS(data):
    l = len(data)
    ##Create a random solution
    cities = list(range(l))
    solution = []
    for i in range(l):
        city = cities[random.randint(0, len(cities) - 1)]
        solution.append(city)
        cities.remove(city)
    routeLength = evaluateSolution(data, solution)

    # print("Route length: ", routeLength)
    ##Get the best neighbor till no better neighbors can be obtained
    neighbor = getBestNeighborLS(solution, data)
    while neighbor[1] < routeLength:
        solution = neighbor[0]
        routeLength = neighbor[1]
        # print("Route length: ", routeLength)
        neighbor = getBestNeighborLS(solution, data)

    return solution, routeLength

def main():

    data = []

    #EACH DATASET HAS AN OPTIMAL SOLUTION
    # five_d.txt = 19 || p01_d.txt= 291 || dantzig42_d.txt = 699 || fri26_d.txt = 937 || gr17_d.txt = 2085 || att48_d.txt = 33523

    optimalCost = 2085  # CHANGE THIS

    with open("Datasets/gr17_d.txt", "r") as f:
        for line in f:
            data.append([int(x) for x in line.split()])

    iterations=1000 #CHANGE THIS
    nOptimalSols=0

    for i in range(iterations):
        start_time = time.time()
        s=hillClimbingILS(data)
        print("--------------")
        print("Final solution: ",s[0])
        print("Final route length: ",s[1])

        #Print runtime per iteration
        print("Runtime: %s seconds" % (time.time() - start_time))

        if(s[1]==optimalCost):
            print("Optimal solution found")
            nOptimalSols = 1
            break
        print("--------------\n")

    print("Number of optimal solutions found: ", nOptimalSols, "/", i + 1)

if __name__ == "__main__":
    main()
