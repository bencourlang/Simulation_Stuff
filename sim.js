// Simulation Stuff

function print(text){
    console.log(text);
}

var foodYield = []
var year = []
var population = []
var infantMortalityRates = []
var healthcarePop = []
var agricultureResearchPop = []
var farmerPop = []
var agricultureYield = []

var peopleDictionary = []

class Person{
    constructor(age){
        this.gender = (Math.floor(Math.random() * 2));  // 0 or 1
        this.age = age;
        this.job = (Math.floor(Math.random() * 100));   // 0 - 99
    }
}

function harvest(food, agriculture){
    var ablePeople = 0;
    var workAge = 8;    // add work age as param for consistency??????
    for(var i in peopleDictionary){
        if(peopleDictionary.length > 10000){ // increase work age irreverable
            workAge = 13;
        }
        if(peopleDictionary[i].age > workAge && peopleDictionary[i].job < 98){
            ablePeople++;
        }
    }

    food += ablePeople * agriculture;

    if(food < peopleDictionary.length){
        for(var i = Math.floor(Math.random(0, peopleDictionary.length)); i < peopleDictionary.length - food; i = Math.floor(Math.random(0, peopleDictionary.length))){
            peopleDictionary.splice(i, 1);
        }
        food = 0;
    }
    else{
        food -= peopleDictionary.length;
    }

    return food;
}

function healthcare(infantMortality){
    var ablePeople = 0;
    var workAge = 8;
    for(var i in peopleDictionary){
        if(peopleDictionary.length > 10000){ // increase work age irreverable
            workAge = 13;
        }
        if(peopleDictionary[i].age > workAge && peopleDictionary[i].job < 98){
            ablePeople++;
        }
    }

    infantMortality = Math.pow(0.985, ablePeople);

    return infantMortality;
}

function agricultureResearch(agriculture){
    var ablePeople = 0;
    var workAge = 8;
    var newAgriculture = 0;
    for(var i in peopleDictionary){
        if(peopleDictionary.length > 10000){ // increase work age irreverable
            workAge = 13;
        }
        if(peopleDictionary[i].age > workAge && peopleDictionary[i].job < 98){
            ablePeople++;
        }
    }

    if(ablePeople != 0){
        newAgriculture = ((153*ablePeople**2)/((ablePeople**2)+(100*ablePeople)) + 2) // decreasing slope lim x -> inf f(x) -> 155, (153x^2/(x^2 + 100x)) + 2
    }

    if(newAgriculture > agriculture){
        return newAgriculture;
    }

    return agriculture;
}

function reproduce(fertilityMin, fertilityMax, infantMortality, birthChance){
    for(var i in peopleDictionary){
        if(peopleDictionary[i].gender == 1 && peopleDictionary[i].age > fertilityMin && peopleDictionary[i].age < fertilityMax){   // make 1 if???
            if(Math.floor(Math.random() * 100) < birthChance && Math.floor(Math.random() * 100) > infantMortality){ // make 1 if???
                peopleDictionary.push(new Person(0));
            }
        }
    }
}

function disaster(){    // kill 5% - 20% of population, **** FIX ****
    for(var i = Math.floor(Math.random(0, peopleDictionary.length)); i < peopleDictionary.length - Math.floor(Math.random() * 20); i = Math.floor(Math.random(0, peopleDictionary.length))){
        peopleDictionary.splice(i, 1);
    }
}

function beginSim(startPopulation){
    for(var i = 0; i < startPopulation; i++){
        peopleDictionary.push(new Person(Math.floor(Math.random() * 32) + 18))

    }
}

function runYear(food, agriculture, fertilityMin, fertilityMax, infantMortality, disasterChance, yearDate, birthChance, oldAgeDeath){
    food = harvest(food, agriculture);

    for(i in peopleDictionary){
        if(peopleDictionary[i].age > oldAgeDeath){
            peopleDictionary.splice(i, 1);
        }
        else{
            peopleDictionary[i].age++;
        }
    }

    // science stuff
    infantMortality = healthcare(infantMortality);
    agriculture = agricultureResearch(agriculture);

    reproduce(fertilityMin, fertilityMax, infantMortality, birthChance);

    /*if(Math.floor(Math.random() * 100) < disasterChance){ // change disaster to % decrease
        print("disaster");
        disaster();
    }*/

    yearDate++;

    /*var numHealthcare = 0;    // graph stuff
    var numAgricultureResearch = 0;
    var numFarmer = 0;

    for(i in peopleDictionary){
        if(peopleDictionary[i].job == 99){
            numHealthcare++;
        }
        else if(peopleDictionary[i].job == 98){
            numAgricultureResearch++;
        }
        else{
            numFarmer++;
        }
    }

    foodYield.push(food);
    year.push(yearDate);
    population.push(peopleDictionary.length);
    infantMortalityRates.push(infantMortality);
    healthcarePop.push(numHealthcare);
    agricultureResearchPop.push(numAgricultureResearch);
    farmerPop.push(numFarmer);
    agricultureYield.push(agriculture);*/

    print("year: " + yearDate + " infantMortality: " + infantMortality + " population: " + peopleDictionary.length);

    return [yearDate, infantMortality, peopleDictionary.length];
}

function main(){
    //random.seed(time.time())  // check if Math.random is good or if I should make my own
    var yearDate = 0;

    var startPopulation = 50;
    var infantMortality = 5;
    //youthMortality = 45   //impliment youth death?
    var agriculture = 2;
    var disasterChance = 10;
    var fertilityMin = 18;
    var fertilityMax = 35;
    var food = 0;
    var birthChance = 20;
    var totalPopulation = 0;
    var oldAgeDeath = 80;

    var endPopulation = 10000;

    beginSim(startPopulation)
    while(peopleDictionary.length < endPopulation && peopleDictionary.length > 1){
        temp = runYear(food, agriculture, fertilityMin, fertilityMax, infantMortality, disasterChance, yearDate, birthChance, oldAgeDeath);

        yearDate = temp[0];
        infantMortality = temp[1];
        totalPopulation = temp[2];
    }
    
    if(totalPopulation >= endPopulation){
        print("It took: " + yearDate + " years to reach " + endPopulation);
    }
    else{
        print("dead after: " + yearDate + " years");
    }
}

function test(){
    var startTime = performance.now()

    for(var i = 0; i < 100000; i++){
        print(i);
    }

    var endTime = performance.now()

    console.log(`Call to doSomething took ${(endTime - startTime)/1000} seconds`)
}

if(typeof require !== 'undefined' && require.main === module){
    test();
}