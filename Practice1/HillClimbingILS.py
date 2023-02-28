import random
import time
import matplotlib.pyplot as plt

def evaluateSolution(data, solution):
    routeLength = 0
    for i in range(len(solution)):
        routeLength += data[solution[i - 1]][solution[i]]
    return routeLength


def getBestNeighbor(solution, data):
    ##Get the neighbors
    neighbors = []
    l = len(solution)
    for i in range(l):
        for j in range(i + 1, l):
            n = solution.copy()
            n[i] = solution[j]
            n[j] = solution[i]
            neighbors.append(n)

    ##Get the best neighbor
    bestNeighbor = neighbors[0]
    bestLength = evaluateSolution(data, bestNeighbor)
    for neighbor in neighbors:
        routeLength = evaluateSolution(data, neighbor)
        if routeLength < bestLength:
            bestLength = routeLength
            bestNeighbor = neighbor
    return bestNeighbor, bestLength


def hillClimbing(data):
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
    neighbor = getBestNeighbor(solution, data)
    while neighbor[1] < routeLength:
        solution = neighbor[0]
        routeLength = neighbor[1]
        # print("Route length: ", routeLength)
        neighbor = getBestNeighbor(solution, data)

    return solution, routeLength


def main():
    data = []

    # EACH DATASET HAS AN OPTIMAL SOLUTION
    # five_d.txt = 19 || p01_d.txt= 291 || dantzig42_d.txt = 699 || fri26_d.txt = 937 || gr17_d.txt = 2085 || att48_d.txt = 33523
    optimalCost = 33523  # CHANGE THIS
    datasetName = "att48_d.txt"  # CHANGE THIS
    with open("Datasets/" + datasetName, "r") as f:
        for line in f:
            data.append([int(x) for x in line.split()])

    iterations = 1000  # CHANGE THIS

    runtime = []
    allSols = []

    for j in range(5):
        optimalSol = 0
        total_start_time = time.time();
        for i in range(iterations):

            start_time = time.time()
            s = hillClimbing(data)
            print("--------------")
            print("Final solution: ", s[0])
            print("Final route length: ", s[1])
            allSols.append(s[1])

            # Print runtime per iteration
            print("Runtime: %s seconds" % (time.time() - start_time))
            runtime.append(time.time() - start_time)

            if (s[1] == optimalCost):
                print("Optimal solution found")
                optimalSol += 1
            else:
                print("Optimal solution not found")
            print("--------------\n")

        print("Number of optimal solutions found: ", optimalSol, " / ", i + 1)
        print("Total Runtime: %s seconds" % (time.time() - total_start_time))

        plt.plot(runtime)
        plt.title('Runtime per iteration dataset att48_d.txt')
        plt.ylabel('Runtime')
        plt.xlabel('Iteration')
        plt.savefig('images/Runtime_dataset6_iterations'+ str(iterations) + '_try' + str(j) + '.png')
        plt.close()

        plt.plot(allSols)
        plt.title('Route length per iteration dataset att48_d.txt')
        plt.ylabel('Route length')
        plt.xlabel('Iteration')
        plt.savefig('images/RouteLength_dataset6_iterations'+ str(iterations) + '_try' + str(j) + '.png')
        plt.close()

        # Save the data to a csv file, whitout overwriting the previous data
        with open('ILSData.csv', 'a') as f:
            # Save the dataset name, number of iterations, total time, average time, optimal solutions
            f.write(datasetName + "," + str(iterations) + "," + str(time.time() - total_start_time) + "," + str(
                (time.time() - total_start_time) / iterations) + "," + str(optimalSol) + "\n")



if __name__ == "__main__":
    main()