import random
import csv
import time


def evaluateSolution(solution, prices, weights, maxWeight, evaluate):
    price = 0
    weight = 0
    for i in range(len(solution)):
        price += prices[i] * solution[i]
        weight += weights[i] * solution[i]

    # for invalid solutions comment this if statement and just return the price
    if evaluate == True:
        if weight > maxWeight:
            return 0
        else:
            return price
    if evaluate == False:
        return price

def HUX(parent1, parent2):
    child1 = []
    child2 = []
    for i in range(len(parent1)):
        if parent1[i] == parent2[i]:
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            if random.randint(1, 100) <= 50:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])
    return child1, child2


def applyGeneticOperator(population, k, cProb, mProb, elitismOpt, crossoverOpt, mutationOpt):
    elitism = elitismOpt
    crossover = crossoverOpt
    mutation = mutationOpt
    parents = []

    #####Tournament selection
    # Select parents through a tournament of size k
    # Select two random parents from the population
    parent1 = population[random.randint(0, len(population) - 1)]
    parent2 = population[random.randint(0, len(population) - 1)]
    parents.append(parent1)
    parents.append(parent2)


    #####Crossover
    if crossover == 1:  # Cross parents with a probability cProb using HUX
        if random.randint(1, 100) <= cProb:
            child1, child2 = HUX(parent1, parent2)

    elif crossover == 2:  # Cross parents with a probability cProb using single-point crossover
        if random.randint(1, 100) <= cProb:
            # Select a random crossover point
            point = random.randint(1, len(parent1) - 1)
            # Create the children by swapping the genes
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]

    elif crossover == 3:  # Cross parents with a probability cProb using uniform crossover
        if random.random() < cProb:
            child1 = []
            child2 = []
            for i in range(len(parents[0])):
                if random.random() < 0.5:
                    child1.append(parents[0][i])
                    child2.append(parents[1][i])
                else:
                    child1.append(parents[1][i])
                    child2.append(parents[0][i])

    #####Mutation
    if mutation == 1:  # Mutate children with a probability mProb
        if random.randint(1, 100) <= mProb:
            # Select a random bit
            bit1 = random.randint(0, len(child1) - 1)
            bit2 = random.randint(0, len(child2) - 1)
            # Flip the bit
            if child1[bit1] == 0:
                child1[bit1] = 1
            else:
                child1[bit1] = 0

            if child2[bit2] == 0:
                child2[bit2] = 1
            else:
                child2[bit2] = 0

            population.append(child1)
            population.append(child2)

        elif mutation == 2:  # Mutate childs with a probability mProb using bit flip mutation
            if random.randint(1, 100) <= mProb:
                # Select a random bit
                bit1 = random.randint(0, len(child1) - 1)
                bit2 = random.randint(0, len(child2) - 1)
                # Reset the bit to a random value
                child1[bit1] = random.randint(0, 1)
                child2[bit2] = random.randint(0, 1)

            population.append(child1)
            population.append(child2)

    #####Elitism
    if elitism:
        # Find the best solution in the population
        best = population[0]
        for solution in population:
            if solution[1] > best[1]:
                best = solution
        # Remove the worst solution from the population
        population.remove(min(population, key=lambda x: x[1]))
        # Add the best solution to the population
        population.append(best)

    return population


def main():
    # Dataset Organziation: Optimal Solution (Chosen or not) | Profits | Weights
    datasetList = ["5.txt", "6.txt", "7a.txt", "7b.txt", "8.txt", "10.txt", "15.txt", "24.txt"]
    capacityList = [26, 190, 50, 170, 104, 165, 750, 6404180]
    OptimalCosts = [51, 150, 109, 1735, 837, 309, 1458, 13549094]

    nSolutionsList = [10, 25, 50]
    maxGenerationsList = [10, 50, 100]
    kList = [2, 3, 5]
    cProbList = [0.5, 0.7, 0.9]
    mProbList = [0.05, 0.1, 0.2]

    with open("results.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Dataset", "Capacity", "PopSize", "maxGenerations", "k", "cProb", "mProb", "Elitism", "Crossover", "Mutation", "Best Solution", "Runtime", "OptimalFound"])

        for datasetIndex in range(len(datasetList)):
            dataset = datasetList[datasetIndex]
            capacity = capacityList[datasetIndex]

            with open(dataset, "r") as file:
                lines = file.readlines()
                prices = []
                weights = []
                for line in lines:
                    line = line.split()
                    prices.append(int(line[1]))
                    weights.append(int(line[2]))

            #For elitism true and false
            for elitism in [True, False]:
                for evaluation in [True, False]:
                    for crossover in [1, 2, 3]:
                        for mutation in [1, 2]:
                            for nSolutions in nSolutionsList:
                                for maxGenerations in maxGenerationsList:
                                    for k in kList:
                                        for cProb in cProbList:
                                            for mProb in mProbList:
                                                # Generate initial population
                                                l = len(weights)
                                                population = []
                                                for i in range(nSolutions):
                                                    objects = list(range(l))
                                                    solution = []
                                                    weight = 0
                                                    while weight < capacity:
                                                        object = objects[random.randint(0, len(objects) - 1)]
                                                        weight += weights[object]
                                                        if weight <= capacity:
                                                            solution.append(object)
                                                            objects.remove(object)

                                                    s = []
                                                    for i in range(l):
                                                        s.append(0)
                                                    for i in solution:
                                                        s[i] = 1
                                                    if evaluation == True:
                                                        population.append([s, evaluateSolution(s, prices, weights, capacity, True)])
                                                    else:
                                                        population.append([s, evaluateSolution(s, prices, weights, capacity, False)])
                                                # Run genetic algorithm
                                                start_time = time.time()
                                                for it in range(maxGenerations):
                                                    population = applyGeneticOperator(population, k, cProb, mProb, elitism, crossover, mutation)
                                                end_time = time.time()
                                                runtime = end_time - start_time

                                                # Find best solution
                                                best = population[0]
                                                for solution in population:
                                                    if solution[1] > best[1]:
                                                        best = solution

                                                # write results
                                                if best[1] == OptimalCosts[datasetIndex]:
                                                    optimalFound = 1
                                                else:
                                                    optimalFound = 0
                                                result = [dataset, capacity, nSolutions, maxGenerations, k, cProb, mProb, elitism, crossover, mutation, best[1], runtime, optimalFound]
                                                writer.writerow(result)
                                                ############################


if __name__ == "__main__":
    main()
