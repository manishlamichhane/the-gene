import defaults
import random

from choices import Gender
from collections import namedtuple


class Individual:
    def __init__(self, **kwargs):
        self.age = 0
        self.is_alive = True
        self.gender = kwargs.get('gender') or random.choice(Gender.CHOICES)
        self.is_fertile = True
        self.ego = kwargs.get('ego') or random.choice(range(0, 100, 5))
        self.health = kwargs.get('health') or random.choice(range(20, 100, 5))
        self.strength = kwargs.get('strength') or random.choice(range(20, 100, 5))
        self.happiness = kwargs.get('happiness') or random.choice(range(0, 100, 5))
        self.intelligence = kwargs.get('intelligence') or random.choice(range(0, 100, 5))
    
    def grow_old(self):
        self.age += 1
        self.health += defaults.Cost.HEALTH
        self.strength += defaults.Cost.STRENGTH
        self.intelligence += defaults.Cost.INTELLIGENCE
    
    @property
    def aggression(self):
        return  (self.strength + self.ego) * self.health - self.intelligence
    
    @property
    def fitness(self):
        return self.health + self.strength + self.happiness + self.intelligence + self.ego

    def attack(self, opponent):
        self.ego += opponent.ego
        self.health -= defaults.Cost.HEALTH
        self.strength -= defaults.Cost.STRENGTH
        self.happiness += defaults.Cost.HAPPINESS
        self.intelligence += defaults.Cost.INTELLIGENCE
        
        opponent.is_alive = False
        print(f'Self: {self.is_alive} Opponent: {opponent.is_alive}')


class Female(Individual):
    def __init__(self, **kwargs):
        #self.is_fertile = kwargs.pop('is_fertile ') if 'is_fertile' in kwargs.keys() else random.choice((True, False))
        self.is_pregnent = False
        self.feminity = random.choice(range(0, 100, 5))  # NOTE(Manish): determins sex of off-spring
        super().__init__(**kwargs)


class Male(Individual):
    def __init__(self, **kwargs):
        #self.is_fertile = kwargs.pop('is_fertile ') if 'is_fertile' in kwargs.keys() else random.choice((True, False))
        self.masculinity = random.choice(range(0, 100, 5)) # NOTE(Manish): determins sex of off-spring
        super().__init__(**kwargs)
