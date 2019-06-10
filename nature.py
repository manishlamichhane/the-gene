import random
from choices import Gender
from defaults import Cost, Threshold, Ancestors
from individual import Female, Male, Individual




class Nature:
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
    def fight(first, second, self):
        strong, weak = Nature.categorise_aggression(first, second)
        strong.attack(weak)
        if weak.health <= 0:
            self.male_population.remove(weak)
        return strong

    @staticmethod
    def direct_descendants(descendants, individual):
        """ Checks if individual is one of the descendants, or a descendant of descendants' children"""

        if not descendants:
            return False
        else:
            if individual in descendants:
                return True
            else:
                for descendant in descendants:
                    if Nature.direct_descendants(descendant.children, individual):
                        return True

    @staticmethod
    def breedable(male, female):
        (m_father, m_mother) = male.parents if male.parents else ('', '')
        (f_father, f_mother) = female.parents if female.parents else ('', '')

        # checks for siblings/half siblings
        if m_father and m_mother and f_father and f_mother and (m_father == f_father or m_mother == f_mother):
            return False

        # checks if direct descendants
        if Nature.direct_descendants(male.children, female):
            return False

        # TODO find lowest common ancestor

        return True


    @staticmethod
    def chose_female_no_inbreed(male, female_population):
        for female in female_population:
            if not female.is_pregnent and not female.strength < 0:
                # check inbreeding
                if Nature.breedable(male, female):
                    return female

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

            available_female =  Nature.chose_female_no_inbreed(stronger_male, self.female_population)

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
            return Male(parents=(male, female)) if male.masculinity > female.feminity else Female(parents=(male, female))

    def select(self):
        self.male_population = [male for male in self.male_population]
        self.female_population = [female for female in self.female_population]

    def age(self):
        for individual in self.male_population + self.female_population:
                individual.grow_old()
