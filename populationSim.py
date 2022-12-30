import random
import time
import matplotlib.pyplot as plt
import math

foodYield = []
year = []
population = []
infantMortalityRates = []
healthcarePop = []
agricultureResearchPop = []
farmerPop = []
agricultureYield = []

peopleDictionary = []

class Person:
    def __init__(self, age):
        self.gender = random.randint(0, 1)
        self.age = age
        self.job = random.randint(0, 100)

def harvest(food, agriculture):
    ablePeople = 0
    workAge = 8
    for person in peopleDictionary:
        if len(peopleDictionary) > 10000: # increase work age irreverable
            workAge = 13
        if person.age > workAge and person.job >= 0 and person.job < 99:
            ablePeople += 1

    food += ablePeople * agriculture

    if food < len(peopleDictionary):
        del peopleDictionary[0:int(len(peopleDictionary) - food)]
        food = 0
    else:
        food -= len(peopleDictionary)
    
    return food

def healthcare(infantMortality):
    ablePeople = 0
    workAge = 8
    for person in peopleDictionary:
        if len(peopleDictionary) > 10000: # increase work age irreverable
            workAge = 13
        if person.age > workAge and person.job == 100:
            ablePeople += 1

    infantMortality *= (pow(0.985, ablePeople))

    return infantMortality

def agricultureResearch(agriculture):
    ablePeople = 0
    workAge = 8
    newAgriculture = 0
    for person in peopleDictionary:
        if len(peopleDictionary) > 10000: # increase work age irreverable
            workAge = 13
        if person.age > workAge and person.job == 99:
            ablePeople += 1

    if ablePeople != 0:
        newAgriculture = ((153*ablePeople**2)/((ablePeople**2)+(100*ablePeople)) + 2) # decreasing slope lim x -> inf f(x) -> 155

    if newAgriculture > agriculture:
        return newAgriculture

    return agriculture

def reproduce(fertilityMin, fertilityMax, infantMortality, birthChance):
    for person in peopleDictionary:
        if person.gender == 1 and person.age < fertilityMax and person.age > fertilityMin:
            if random.randint(0, 100) < birthChance and random.randint(0, 100) > infantMortality:
                peopleDictionary.append(Person(0))

def disaster():
    del peopleDictionary[0:int(random.uniform(0.05, 0.2) * len(peopleDictionary))]

def beginSim(startPopulation):
    for x in range(startPopulation):
        peopleDictionary.append(Person(random.randint(18, 50)))

def runYear(food, agriculture, fertilityMin, fertilityMax, infantMortality, disasterChance, yearDate, birthChance, axs):
    food = harvest(food, agriculture)

    for person in peopleDictionary:
        if person.age > 80:
            peopleDictionary.remove(person)
        else:
            person.age += 1

    # science stuff
    infantMortality = healthcare(infantMortality)
    agriculture = agricultureResearch(agriculture)

    reproduce(fertilityMin, fertilityMax, infantMortality, birthChance)

    if random.randint(0, 100) < disasterChance:
        disaster()

    yearDate += 1
    numHealthcare = 0
    numAgricultureResearch = 0
    numFarmer = 0

    for person in peopleDictionary:
        if person.job == 100:
            numHealthcare += 1
        elif person.job == 99:
            numAgricultureResearch += 1
        else:
            numFarmer += 1

    foodYield.append(food)
    year.append(yearDate)
    population.append(len(peopleDictionary))
    infantMortalityRates.append(infantMortality)
    healthcarePop.append(numHealthcare)
    agricultureResearchPop.append(numAgricultureResearch)
    farmerPop.append(numFarmer)
    agricultureYield.append(agriculture)


    axs[0, 0].cla()
    axs[0, 1].cla()
    axs[1, 0].cla()
    axs[1, 1].cla()
    axs[2, 0].cla()
    axs[2, 1].cla()

    axs[0, 0].plot(year, population)
    axs[0, 0].set_title('Total Population')

    axs[0, 1].plot(year, farmerPop)
    axs[0, 1].set_title('Farmer Population')

    axs[1, 0].plot(year, agricultureResearchPop)
    axs[1, 0].set_title('Agriculture Worker Population')

    axs[1, 1].plot(year, healthcarePop)
    axs[1, 1].set_title('Health Worker Population')

    axs[2, 0].plot(year, agricultureYield)
    axs[2, 0].set_title('Agriculture Yield')

    axs[2, 1].plot(year, infantMortalityRates)
    axs[2, 1].set_title('Infant Mortality')
    #plt.legend(['total population', 'healthcare population', 'agriculture research population', 'farmer population'])
    
    plt.pause(0.05)

    return yearDate, infantMortality, len(peopleDictionary)

def main():
    random.seed(time.time())
    yearDate = 0
    figure, axs = plt.subplots(3, 2)

    startPopulation = 50
    infantMortality = 5
    #youthMortality = 45
    agriculture = 2
    disasterChance = 10
    fertilityMin = 18
    fertilityMax = 35
    food = 0
    birthChance = 20
    totalPopulation = 0

    endPopulation = 100000

    beginSim(startPopulation)
    while len(peopleDictionary) < endPopulation and len(peopleDictionary) > 1:
        yearDate, infantMortality, totalPopulation = runYear(food, agriculture, fertilityMin, fertilityMax, infantMortality, disasterChance, yearDate, birthChance, axs)
    
    if(totalPopulation >= endPopulation):
        print("survive and thrive")
        print("It took:", yearDate, "years")
    else:
        print("dead after:", yearDate, "years")

    plt.show(block = True)

if __name__ == '__main__':
    main()