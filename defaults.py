

class Attribute:
    EGO = 20
    HEALTH = 40
    STRENGTH = 40
    HAPPINESS = 20
    INTELLIGENCE = 20

class Cost:
    EGO = 20
    HEALTH = 20
    STRENGTH = 5
    HAPPINESS = 10
    REPRODUCTION = 10
    INTELLIGENCE  = 10
    


class Threshold:
    HEALTH  = 10
    STRENGTH = 10
    SURVIVAL = 30
    POPULATION = 200

class Index:
    FITNESS = 50

class Ancestors:
    # They are like Adam and Eve, they don't have any parents
    ORIG_POP = 16

    # Direct descendants of the ORIG_POP
    INITIAL_POP = 160

    # Percentage of general male population
    MALE_PCT = 60

