from pydantic import BaseModel, Field, field_validator, StrictInt
from typing import List, Optional
from datetime import datetime
from enum import Enum

class Difficulty(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class Superpower(BaseModel):
    name: str
    description: str
    power_level: StrictInt = Field(ge=1, le=10)

    def increase_power_level(self, increase: int):
        self.power_level = min(10, max(1, self.power_level + increase))

class Superhero(BaseModel):
    name: str
    secret_identity: str
    age: int = Field(gt=0)
    superpowers: List[Superpower]
    arch_nemesis: Optional[str] = None
    catchphrase: str = "I'm here to save the day!"

    def increase_age(self, years: int):
        self.age += years

    @field_validator('age')
    def age_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Age must be positive')
        return v

class Mission(BaseModel):
    title: str
    description: str
    difficulty: Difficulty
    assigned_heroes: List[Superhero]
    deadline: datetime

    @field_validator('difficulty')
    def difficulty_must_be_valid(cls, v):
        if v not in Difficulty:
            raise ValueError('Invalid difficulty level')
        return v


# Create a superpower
super_strength = Superpower(name="Super Strength", description="Ability to lift heavy objects", power_level=8)
Superpower(
    name = "sdsa",
    description = "123",
    power_level = "10"
)

# Create a superhero
superman = Superhero(name="Superman", secret_identity="Clark Kent", age=30, superpowers=[super_strength])

# Create a mission
mission = Mission(
    title="Save the World",
    description="Prevent an alien invasion",
    difficulty=Difficulty.HARD,
    assigned_heroes=[superman],
    deadline=datetime.now()
)

exit(0)

# Serialization
import json
print(json.dumps(mission.dict(), default=str))

# Validation errors
try:
    invalid_hero = Superhero(name="Invalid", secret_identity="Test", age=-5, superpowers=[])
except ValueError as e:
    print(f"Validation error: {e}")

try:
    invalid_mission = Mission(
        title="Invalid",
        description="Test",
        difficulty="IMPOSSIBLE",
        assigned_heroes=[superman],
        deadline=datetime.now()
    )
except ValueError as e:
    print(f"Validation error: {e}")
