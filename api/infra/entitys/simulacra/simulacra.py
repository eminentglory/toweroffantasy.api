
from pydantic import Field

from api.infra.entitys.base import EntityBase
from api.infra.entitys.simulacra.extra import VoiceActors, Awakening, Assets


class Simulacra(EntityBase):
    name: str
    avatarID: str
    advanceId: str | None = None
    assets: Assets
    weapon: str
    age: str
    height: str
    gender: str
    state: str
    city: str
    rating: str
    gift_types: list[str] = Field(alias='gp', serialization_alias='gift_types')
    voice_actors: VoiceActors = Field(alias='va', serialization_alias='voice_actors')
    awakenings: list[Awakening] = Field(alias='trait', default=[], serialization_alias='awakenings')

