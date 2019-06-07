import defaults
import random
import threshold

from choices import Gender
from collections import namedtuple

Person = namedtuple('Person', ['agility', 'strength', 'intelligence', 'health'])


def is_strong_enough(individual, strength=defaults.Threshold.STRENGTH):
    return individual.strength > strength

def categorise_aggression(first, second):
    # NOTE(Manish): Equality of Aggression needs to be addressed.
    return (first, second) if first.aggression > second.aggression else (second, first)

def fight(first, second):
    strong, weak = categorise_aggression(first, second)
    strong.attack(weak)

    return strong

def choose_female(female_population):
    for female in female_population:
        if female.is_alive and not female.is_pregnant:
            return female

def reproduce(male, female):
    male.strength -= defaults.Cost.REPRODUCTION
    male.happiness += defaults.Cost.HAPPINESS

    female.happiness += defaults.Cost.HAPPINESS
    female.strength -= defaults.Cost.REPRODUCTION

    if male.is_fertile and female.is_fertile:
        female.is_pregnent = True
        return Individual()

class Individual:
    def __init__(self, **kwargs):
        self.age = 0  # NOTE(Manish): Genetic Algo. tries to optimize this criteria
        self.is_alive = True
        self.ego = kwargs['ego'] or random.choice(range(0, 100, 5))
        self.health = kwargs['health'] or random.choice(range(0, 100, 5))
        self.strength = kwargs['strength'] or random.choice(range(0, 100, 5))
        self.happiness = kwargs['happiness'] or random.choice(range(0, 100, 5))
        self.intelligence = kwargs['intelligence'] or random.choice(range(0, 100, 5))
    
    def grow_old(self):
        self.age += 1
        self.intelligence += defaults.Cost.INTELLIGENCE
        self.strength -= defaults.Cost.STRENGTH
    
    @property
    def aggression(self):
        return self.health + self.strength + self.ego - self.intelligence

    def kill(self, opponent):
        self.ego += opponent.ego
        self.strength -= defaults.Cost.STRENGTH
        self.health -= defaults.Cost.HEALTH
        self.happiness += defaults.Cost.HAPPINESS
        self.intelligence += defaults.Cost.INTELLIGENCE
        
        opponent.is_alive = False


class Female(Individual):
    def __init__(self, **kwargs):
        self.gender = Gender.FEMALE
        self.is_fertile = kwargs.pop('is_fertile ') if 'is_fertile' in kwargs.keys() else random.choice((True, False))
        self.is_pregnent = False
        super().__init__(**kwargs)


class Male(Individual):
    def __init__(self, **kwargs):
        self.gender = Gender.MALE
        self.is_fertile = kwargs.pop('is_fertile ') if 'is_fertile' in kwargs.keys() else random.choice((True, False))
        super().__init__(**kwargs)


class Nature:
    def __init__(self, *args, **kwargs):
        self.male_population = (Male(gender=Gender.MALE) for i in range(100))
        self.female_population = (Female(gender=Gender.FEMALE) for i in range(100))

    def check_male_fitness(self):
        while True:
            chosen_male = random.choices(self.male_population, k=2)
            alive_male = fight(*chosen_male)

            reproduce(alive_male, )
    
    def select(self):
        pass
    
    def terminate(self):
        pass
 