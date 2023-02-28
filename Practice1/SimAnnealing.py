import random
import math
import time
import matplotlib.pyplot as plt

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

def simAnnealing(data,t0, cf):
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

        it+=1 # Nº of iterations

        #Cooling function CHANGE THIS AS WE WANT
        alpha = 0.99 #Cooling rate, CHANGE THIS AS WE WANT
        if (cf == 1):
            t = alpha*t
        elif (cf == 2):
            t = t0/(1+alpha*it)
        elif (cf == 3):
            t = (alpha**it) * t0


        #print("Length of the route: ", lengthTravel)
    print("Final Temperature: ", t)
    return solution, lengthTravel


def main():
    data = []

    # EACH DATASET HAS AN OPTIMAL SOLUTION
    # five_d.txt = 19 || p01_d.txt= 291 || dantzig42_d.txt = 699 || fri26_d.txt = 937 || gr17_d.txt = 2085 || att48_d.txt = 33523
    optimalCost = 699  # CHANGE THIS
    datasetName = "dantzig42_d.txt"  # CHANGE THIS
    with open("Datasets/" + datasetName, "r") as f:
        for line in f:
            data.append([int(x) for x in line.split()])

    iterations = [10,100,1000]

    for iters in iterations:
        print("Number of iterations: ", iters)
        iters = iters

        for l in range(3):
            coolingFunction = l+1
            print("Cooling function: ", coolingFunction)

            for k in range (3):
                myList = [5,10,50]
                temp = myList[k]

                for j in range(5):

                    optimalSol = 0
                    total_start_time = time.time();
                    runtime = []
                    allSols = []
                    for i in range(iters):

                        start_time = time.time()
                        s = simAnnealing(data, temp, coolingFunction)

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
                    plt.title('Runtime per iteration dataset ' + datasetName)
                    plt.ylabel('Runtime')
                    plt.xlabel('Iteration')
                    plt.savefig('images/Runtime_dataset3_iterations'+ str(iters) + '_try' + str(j+1) + '_cf' + str(coolingFunction) + '_t0' + str(temp) + '.png')
                    plt.close()

                    plt.plot(allSols)
                    plt.title('Route length per iteration dataset ' + datasetName)
                    plt.ylabel('Route length')
                    plt.xlabel('Iteration')
                    plt.savefig('images/RouteLength_dataset3_iterations'+ str(iters) + '_try' + str(j+1) + '.png')
                    plt.close()

                    # Save the data to a csv file, whitout overwriting the previous data
                    with open('SimAnnealingData.csv', 'a') as f:
                        # Save the dataset name, number of iterations, total time, average time, optimal solutions
                        f.write(datasetName + "," + str(i+1) + "," + str(time.time() - total_start_time) + "," + str(
                            (time.time() - total_start_time) / iters) + "," + str(optimalSol) + "," + str(temp) + "," + str(coolingFunction) + "\n")
                    ####

if __name__ == "__main__":
    main()
