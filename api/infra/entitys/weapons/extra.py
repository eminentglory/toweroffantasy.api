
from pydantic import BaseModel, BeforeValidator
from typing import Annotated

from api.utils import bold_numbers, place_weapon_skill_icon


class Skill(BaseModel):
    id: str
    icon: Annotated[str, BeforeValidator(place_weapon_skill_icon)]
    name: str
    description: Annotated[str, BeforeValidator(bold_numbers)]

class Skills(BaseModel):
    normals: list[Skill]
    dodge: list[Skill]
    skill: list[Skill]
    discharge: list[Skill]

class Stats(BaseModel):
    shatter: int | float
    charge: int | float

class Advancements(BaseModel):
    description: Annotated[str, BeforeValidator(bold_numbers)] | None = None
    stats: Stats
    need: str

class WeaponEffect(BaseModel):
    title: str
    description: str

class ShatterOrCharge(BaseModel):
    value: float
    tier: str