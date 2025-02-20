
from fastapi import APIRouter
from pathlib import Path
from json import loads

from api.core.response import PrettyJsonResponse
from api.infra.entitys import Raritys


RARITYS_DATA: dict[str, dict[str, dict[str, str]]] = loads(Path('api/infra/database/rarity.json').read_bytes())
RARITY_DATA_RE = {rarity_key: value_asset
                for rarity_key, rarity_value in RARITYS_DATA.items() 
                for _, value_asset in rarity_value.items()}

RARITY_MODEL = Raritys(**RARITY_DATA_RE) # type: ignore


router = APIRouter(prefix='/rarities', tags=['Rarities'])
METADATA = {
    'name': 'Rarities',
    'description': 'Simple route to get rarities assets',
    }


@router.get('', name='Get rarity', response_model=Raritys)
async def get_rarity():
    '''  
    **Return** \n
        Rarity
    '''

    return PrettyJsonResponse(RARITY_MODEL.model_dump())



    