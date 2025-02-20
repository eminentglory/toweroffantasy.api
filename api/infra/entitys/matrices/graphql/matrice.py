
import strawberry

from api.infra.entitys.graphql.banner import Banner
from .extra import MatriceSet, MatrixAssets


@strawberry.type
class Matrice:
    id: str
    SimulacrumID: str | None
    name: str
    type: str
    description: str
    assets: MatrixAssets
    rarity: str
    sets: list[MatriceSet]
    Banners: list[Banner]
