import uuid

import defaults
import random

from choices import Gender
from collections import namedtuple

class Individual:
    def __str__(self):
        return self.name if self.name else str(self.id)

    def __init__(self, parents=(), **kwargs):
        # for logging and debugging
        self.id = uuid.uuid4()
        self.age = 0
        self.gender = kwargs.get('gender') or random.choice(Gender.CHOICES)
        self.ego = kwargs.get('ego') or random.choice(range(0, 100, 5))
        self.health = kwargs.get('health') or random.choice(range(20, 100, 5))
        self.happiness = kwargs.get('happiness') or random.choice(range(0, 100, 5))
        self.intelligence = kwargs.get('intelligence') or random.choice(range(0, 100, 5))
        self.parents = parents
        self.name = kwargs.get('name') or ''
        if parents and len(parents) == 2:
            # Index 0 is for father
            parents[0].children.append(self)

            # Index 1 is for mother
            parents[1].children.append(self)
        self.children = []

    def grow_old(self):
        self.age += 1
        self.intelligence += defaults.Cost.INTELLIGENCE
        if self.age < 40:
            self.strength += defaults.Cost.STRENGTH
        else:
            self.strength -= defaults.Cost.STRENGTH
        if type(self) == Female:
            self.is_pregnent = False

    @property
    def aggression(self):
        return self.health + self.strength + self.ego - self.intelligence
    
    @property
    def fitness(self):
        return self.health + self.strength + self.happiness + self.intelligence + self.ego

    def attack(self, opponent):
        self.ego += opponent.ego
        self.strength -= defaults.Cost.STRENGTH
        self.health -= 5
        opponent.health -= 10
        self.happiness += defaults.Cost.HAPPINESS
        self.intelligence += defaults.Cost.INTELLIGENCE



class Female(Individual):
    def __init__(self, **kwargs):
        self.is_fertile = kwargs.pop('is_fertile ') if 'is_fertile' in kwargs.keys() else random.choice((True, False))
        self.strength = kwargs.get('strength') or random.choice(range(20, 50, 5))
        self.is_pregnent = False
        self.feminity = random.choice(range(0, 100, 5))  # NOTE(Manish): determins sex of off-spring
        super().__init__(gender=Gender.FEMALE, **kwargs)


class Male(Individual):
    def __init__(self, **kwargs):
        self.is_fertile = kwargs.pop('is_fertile ') if 'is_fertile' in kwargs.keys() else random.choice((True, False))
        self.strength = kwargs.get('strength') or random.choice(range(50, 100, 5))
        self.masculinity = random.choice(range(0, 100, 5)) # NOTE(Manish): determins sex of off-spring
        super().__init__(gender=Gender.MALE, **kwargs)
