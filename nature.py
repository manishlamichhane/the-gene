import random
from choices import Gender
from defaults import Cost, Threshold
from individual import Female, Male

class Nature:
    def __init__(self, *args, **kwargs):
        self.male_population = [Male(gender=Gender.MALE) for i in range(30)]
        self.female_population = [Female(gender=Gender.FEMALE) for i in range(30)]
    
    @property
    def total_population(self):
        return len(self.male_population) + len(self.female_population)

    @staticmethod
    def categorise_aggression(first, second):
        # NOTE(Manish): Equality of Aggression needs to be addressed.
        return (first, second) if first.aggression > second.aggression else (second, first)

    @staticmethod
    def fight(first, second):
        strong, weak = Nature.categorise_aggression(first, second)
        strong.attack(weak)

        return strong

    @staticmethod
    def choose_female(female_population):
        for female in female_population:
            if female.is_alive and not female.is_pregnent:
                return female

    @staticmethod
    def choose_alive_male(male_population):
        # NOTE(Manish): Try using concepts of Streams from Java
        choosen_male = random.choices(male_population, k=2)
        if not (choosen_male[0].is_alive and choosen_male[1].is_alive):
            # NOTE(Manish): Can lead to infinite recursion if all male are dead
            Nature.choose_alive_male(male_population)
        print(choosen_male[0].is_alive, choosen_male[1].is_alive)
        return choosen_male


    def enforce_darwinism(self):
        while True:
            choosen_male = Nature.choose_alive_male(self.male_population)
            stronger_male = Nature.fight(*choosen_male)
            available_female =  Nature.choose_female(self.female_population)
            
            if not available_female:
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
        male.health += Cost.HEALTH

        female.strength -= Cost.REPRODUCTION
        female.happiness += Cost.HAPPINESS
        female.health += Cost.HEALTH

        if male.is_fertile and female.is_fertile:
            female.is_pregnent = True
            # NOTE(Manish): Offspring will have dominant parents gender
            print('Child Added')
            return Male(gender=Gender.MALE) if male.masculinity > female.feminity else Female(gender=Gender.FEMALE)

    def select(self):
        self.male_population = [male for male in self.male_population if male.is_alive is True]
        self.female_population = [female for female in self.female_population if female.is_alive is True]

    def age(self):
        for individual in self.male_population + self.female_population:
            if individual.is_alive:
                individual.grow_old()
