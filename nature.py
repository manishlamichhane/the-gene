import random


from choices import Gender
from defaults import Cost, Threshold, Ancestors
from individual import Female, Male, Individual
from mixins import Family


class Nature(Family):
    def __init__(self, *args, **kwargs):
        # Define number of original ancestors
        orig_male_ancestors_pop = int((Ancestors.MALE_PCT*Ancestors.ORIG_POP)/100)
        orig_female_ancestors_pop = Ancestors.ORIG_POP - orig_male_ancestors_pop

        # Create original population
        orig_male_ancestors = [Male() for _ in range(orig_male_ancestors_pop)]
        orig_female_ancestors = [Female() for _ in range(orig_male_ancestors_pop +
                                                                             orig_female_ancestors_pop)]

        # Define initial population numbers, direct descendants of the original population
        initial_male_pop = int((Ancestors.INITIAL_POP * Ancestors.MALE_PCT) / 100)
        initial_female_pop = Ancestors.INITIAL_POP - initial_male_pop

        # Create lists for the initial population
        male_offsprings: [Male] = []
        female_offsprings: [Female] = []

        # make it so that male is produced Ancestors.MALE_PCT% of the time
        distribution = [1 for _ in range(initial_male_pop)] +\
                       [0 for _ in range(initial_male_pop, initial_male_pop + initial_female_pop)]

        random.shuffle(distribution)
        # random breed
        while distribution:
            random_male_ancestor = random.choice(orig_male_ancestors)
            random_female_ancestor = random.choice(orig_female_ancestors)

            if distribution.pop() % 2 == 1:
                child = Male(parents=(random_male_ancestor, random_female_ancestor))
                male_offsprings.append(child)
            else:
                child = Female(parents=(random_male_ancestor, random_female_ancestor))
                female_offsprings.append(child)

        self.male_population = male_offsprings
        self.female_population = female_offsprings
        # self.male_population = [Male(gender=Gender.MALE) for i in range(100)]
        # self.female_population = [Female(gender=Gender.FEMALE) for i in range(50)]

    @property
    def total_population(self):
        return len(self.male_population) + len(self.female_population)

    @staticmethod
    def categorise_aggression(first, second):
        # NOTE(Manish): Equality of Aggression needs to be addressed.
        return (first, second) if first.aggression > second.aggression else (second, first)

    @staticmethod
    def choose_female(female_population):
        for female in female_population:
            if not female.is_pregnent and not female.strength < 0:
                return female

    @staticmethod
    def choose_alive_male(male_population):
        # NOTE(Manish): Try using concepts of Streams from Java
        if len(male_population) < 2:
            return list(male_population[0])
        return random.sample(male_population, k=2)
    
    @staticmethod
    def reproduce(male, female):
        male.strength -= Cost.REPRODUCTION
        male.happiness += Cost.HAPPINESS

        female.happiness += Cost.HAPPINESS
        female.strength -= Cost.REPRODUCTION

        if male.is_fertile and female.is_fertile:
            female.is_pregnent = True
            # NOTE(Manish): Offspring will have dominant parents gender
            return Male(parents=(male, female)) if male.masculinity > female.feminity else Female(parents=(male, female))
    
    def fight(self, first, second):
        strong, weak = Nature.categorise_aggression(first, second)
        strong.attack(weak)
        
        if weak.health <= 0:
            self.male_population.remove(weak)
        
        if strong.health <= 0:
            self.male_population.remove(strong)
            return 
        
        return strong

    def enforce_darwinism(self):
        while True:
            choosen_male = Nature.choose_alive_male(self.male_population)

            # Small Integers are cached, we can use is here. More readable
            stronger_male = choosen_male[0] if len(choosen_male) is 1 else self.fight(*choosen_male)
            
            if stronger_male is None:
                return

            available_female =  Family.chose_female_no_inbreed(stronger_male, self.female_population)

            # NOTE(Manish): Terminate if no fertile female
            # or the last male alive is infertile 
            if not available_female or (len(choosen_male) is 1 and not choosen_male[0].is_fertile):
                return

            offspring = self.reproduce(stronger_male, available_female)

            if not offspring:
                continue

            self.male_population.append(offspring) if offspring.is_male else self.female_population.append(offspring)
            
    def select(self):
        self.male_population = [male for male in self.male_population]
        self.female_population = [female for female in self.female_population]

    def age(self):
        for individual in self.male_population + self.female_population:
                individual.grow_old()
