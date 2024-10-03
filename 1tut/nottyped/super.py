'''
    Mission class

    Attributes:
        title (str): The title of the mission
        description (str): The description of the mission
        difficulty (int): The difficulty level of the mission
        assigned_heroes (list): The list of Superhero objects assigned to the mission
        deadline (datetime): The deadline for the mission

    Methods:
'''
class Mission:
    def __init__(self, title, description, difficulty, assigned_heroes, deadline):
        self.title = title
        self.description = description
        self.difficulty = difficulty
        self.assigned_heroes = assigned_heroes
        self.deadline = deadline

'''
    Superhero class
    Represents a superhero with a secret identity, age, superpowers, arch-nemesis, and catchphrase.

    Attributes:
        name (str): The superhero's name
        secret_identity (str): The superhero's secret identity
        age (int): The superhero's age
        superpowers (list): A list of Superpower objects representing the superhero's superpowers
        arch_nemesis (str): The superhero's arch-nemesis
        catchphrase (str): The superhero's catchphrase
    
    Methods:
'''
class Superhero:
    def __init__(self, name, secret_identity, age, superpowers, arch_nemesis=None, catchphrase="I'm here to save the day!"):
        self.name = name
        self.secret_identity = secret_identity
        self.age = age
        self.superpowers = superpowers
        self.arch_nemesis = arch_nemesis
        self.catchphrase = catchphrase
    
    def increase_age(self, years):
        self.age += years


'''
    Superpower class
    Attributes:
        name (str): The name of the superpower
        description (str): A brief description of the superpower
        power_level (int): The power level of the superpower, from 1 to 10
    Methods:
        increase_power_level(increase: int): Increase the power level of the superpower by the specified amount
'''
class Superpower:
    def __init__(self, name, description, power_level):
        self.name = name
        self.description = description
        self.power_level = power_level
    
    def increase_power_level(self, increase):
        self.power_level += increase

# Problematic usage examples

# 1. No type checking
# power_level should be an int
# name and description should be strings
super_strength = Superpower("super strength", "Ability to lift heavy objects", "very strong")
'''
self.power_level += increase
TypeError: can only concatenate str (not "int") to str
'''
# super_strength.increase_power_level(10)


# 2. No validation
superman = Superhero("Superman", "Clark Kent", -5, [super_strength])  # Age shouldn't be negative
superman.increase_age(-10)  # Age can be decreased

'''
self.age += years
TypeError: unsupported operand type(s) for +=: 'int' and 'str'
'''
superman.increase_age("10")


# 3. Missing required fields
incomplete_mission = Mission("Save the World", "Prevent an alien invasion", 5, [superman], "deadline")  # Deadline should be a datetime object
incomplete_mission.difficulty = 1002 # Should be EASY, MEDIUM, or HARD

# 5. Difficult serialization
import json
try:
    json.dumps(incomplete_mission.__dict__)
except TypeError as e:
    print(f"Serialization error: {e}")

# 6. No built-in data validation or error messages
print(f"Superman's age: {superman.age}")  # Prints -15, which doesn't make sense
