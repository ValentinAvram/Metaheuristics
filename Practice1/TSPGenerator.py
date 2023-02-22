import random

def generator(nCities):
    tsp = []
    for i in range(nCities):
        distances = []
        for j in range(nCities):
            if j == i:
                distances.append(0)
            elif j < i:
                distances.append(tsp[j][i])
            else:
                distances.append(random.randint(10, 1000))
        tsp.append(distances)
    return tsp

def main():
    tsp = generator(10)
    for i in tsp:
        print(i)

if __name__ == "__main__":
    main()
