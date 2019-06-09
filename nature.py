import random
from choices import Gender
from defaults import Cost, Threshold
from individual import Female, Male

class Nature:
    def __init__(self, *args, **kwargs):
        self.male_population = [Male(gender=Gender.MALE) for i in range(100)]
        self.female_population = [Female(gender=Gender.FEMALE) for i in range(50)]
    
    @property
    def total_population(self):
        return len(self.male_population) + len(self.female_population)

    @staticmethod
    def categorise_aggression(first, second):
        # NOTE(Manish): Equality of Aggression needs to be addressed.
        return (first, second) if first.aggression > second.aggression else (second, first)

    @staticmethod
    def fight(first, second, self):
        strong, weak = Nature.categorise_aggression(first, second)
        strong.attack(weak)
        if weak.health <= 0:
            self.male_population.remove(weak)
        return strong

    @staticmethod
    def choose_female(female_population):
        for female in female_population:
            if not female.is_pregnent and not female.strength < 0:
                return female

    @staticmethod
    def choose_alive_male(male_population):
        # NOTE(Manish): Try using concepts of Streams from Java
        if len(male_population) < 2:
            choosen_male = male_population[0]
        else:
            choosen_male = random.choices(male_population, k=2)
        return choosen_male

    def getFertileMalePop(self):
        malepop = 0
        for male in self.male_population:
            if male.is_fertile:
                malepop = malepop + 1
        return malepop

    def getFertileFemalePop(self):
        femalepop = 0
        for female in self.female_population:
            if female.is_fertile:
                femalepop = femalepop + 1
        return femalepop

    def showFertilePopulation(self):
        print(f'Fertile Male: {self.getFertileMalePop()}')
        print(f'Fertile Female: {self.getFertileFemalePop()}')

    def enforce_darwinism(self):
        while True:
            choosen_male = Nature.choose_alive_male(self.male_population)

            if not type(choosen_male) == list:
                stronger_male = choosen_male
            else:
                stronger_male = Nature.fight(choosen_male[0], choosen_male[1], self)

            available_female =  Nature.choose_female(self.female_population)
            
            if not available_female or (not type(choosen_male) == list and not choosen_male.is_fertile):
                # NOTE(Manish): If no female are available for reproduction
                # the selection stops
                return

            individual = self.reproduce(stronger_male, available_female)
            
            if individual:
                if individual.gender == Gender.MALE:
                    self.male_population.append(individual)
                else:
                    self.female_population.append(individual)

    def reproduce(self, male, female):
        male.strength -= Cost.REPRODUCTION
        male.happiness += Cost.HAPPINESS

        female.happiness += Cost.HAPPINESS
        female.strength -= Cost.REPRODUCTION

        if male.is_fertile and female.is_fertile:
            female.is_pregnent = True
            # NOTE(Manish): Offspring will have dominant parents gender
            #print('Child Added')
            return Male(gender=Gender.MALE) if male.masculinity > female.feminity else Female(gender=Gender.FEMALE)

    def select(self):
        self.male_population = [male for male in self.male_population]
        self.female_population = [female for female in self.female_population]

    def age(self):
        for individual in self.male_population + self.female_population:
                individual.grow_old()
