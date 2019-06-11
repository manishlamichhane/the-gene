import random
from collections import deque

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
    def breedable(m1,m2):
        return not Nature.are_family(m1, m2)

    @staticmethod
    def are_family(member_1, member_2):
        # print(f"===START:: Checking breedability between {member_1} and {member_2}")

        (m1_father, m1_mother) = member_1.parents if member_1.parents else ('', '')
        (m2_father, m2_mother) = member_2.parents if member_2.parents else ('', '')

        is_family = False
        # checks for siblings/half siblings directly
        if m1_father and m1_mother and m2_father and m2_mother and (m1_father == m2_father or m1_mother == m2_mother):
            is_family = True
        elif Nature.trace_common_family(member_1, member_2, 1):
            is_family = True

        else:
            is_family = False

        # print(f"===END:: {member_1} and {member_2} are{' not' if not is_family else ''} a family")

        return is_family

    @staticmethod
    def print_individual(individuals):
        if type(individuals) == list or type(individuals) == set or type(individuals) == tuple:
            _str = "["
            for i in individuals:
                _str += str(i) + ", "

            _str += "]"
            return _str
        elif type(individuals) == Male or type(individuals) == Female:
            return str(individuals)


    @staticmethod
    def trace_common_family(members_to_check_against, member, depth, back_ref=deque(maxlen=3)):
        """Checks if member is a close family member based on Ancestors.DESCENDANCY_DEPTH"""

        # print(f"Checking {member} at depth level:{str(depth)} against {Nature.print_individual(members_to_check_against)}")
        if abs(depth) > Ancestors.DESCENDANCY_DEPTH:
            # print("Max depth reached")
            return False
        elif not members_to_check_against:
            # print("No further members to check")
            return False
        elif type(members_to_check_against) == tuple or\
                type(members_to_check_against) == list or\
                type(members_to_check_against) == set:

            if member in members_to_check_against:
                # print("Family member found")
                return True
            else:
                family_found = False

                for member_to_check in members_to_check_against:
                    qpop = back_ref.popleft() if len(back_ref) > 0 else ''
                    if qpop:
                        back_ref.appendleft(qpop)

                    if qpop != member_to_check:
                        back_ref.append(member_to_check)
                        family_found = Nature.trace_common_family(member_to_check,
                                                                  member, abs(depth) + 1, back_ref)
                    # else:
                        # print(f"{member_to_check} skipped due to back reference {str(back_ref)}")

                    if family_found:
                        return True

                return family_found

        else:
            q1 = back_ref.copy()
            q2 = back_ref.copy()
            if len(back_ref) == 0:
                q1.append(members_to_check_against)
                q2.append(members_to_check_against)

            return Nature.trace_common_family(members_to_check_against.parents,
                                              member, abs(depth),  q1) or \
                   Nature.trace_common_family(members_to_check_against.children,
                                              member, abs(depth),  q2)


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
