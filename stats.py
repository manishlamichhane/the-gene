from defaults import Index


class Statistics:
    def __init__(self, nature, **kwargs):
        self.nature = nature
        self.population = nature.male_population + nature.female_population
    
    def _calculate_fitness_percent(self, population):
        counter = 0
        for individual in population:
            if individual.fitness >= Index.FITNESS:
                counter += 1
        return counter / len(population) * 100

    def calculate_total_fit_percent(self):
        if not self.population:
            return 0
        return self._calculate_fitness_percent(self.population)
    
    def calculate_total_fit_male_percent(self):
        if not self.nature.male_population:
            return 0
        return self._calculate_fitness_percent(self.nature.male_population)
    
    def calculate_total_fit_female_percent(self):
        if not self.nature.female_population:
            return 0
        return self._calculate_fitness_percent(self.nature.female_population)
    
    def get_strongest_male(self):
        """Returns Male with highest fitness index"""
        sorted_male_pop = sorted(self.nature.male_population, key=lambda male: male.fitness, reverse=True)
        return sorted_male_pop[0]
    
    def get_fertile_male_pop(self):
        return sum(1 for male in self.nature.male_population if male.is_fertile)

    def get_fertile_female_pop(self):
        return sum(1 for female in self.nature.female_population if female.is_fertile)

    def display(self):
        print('##########################')
        print(f'Total Population: {self.nature.total_population}')
        print(f'Total Fit Population %: {self.calculate_total_fit_percent()} \n')
        print(f'Total Male: {len(self.nature.male_population)}')
        print(f'Total Fit Male %: {self.calculate_total_fit_male_percent()}')
        print(f'Total Fertile Male: {self.get_fertile_male_pop()}')
        print(f"Strongest Male's Attribute: {self.get_strongest_male().__dict__} \n")
        print(f'Total FeMale: {len(self.nature.female_population)}')
        print(f'Total Fit FeMale %: {self.calculate_total_fit_female_percent()}')
        print(f'Total Fertile FeMale: {self.get_fertile_female_pop()}')
        print('##########################')
