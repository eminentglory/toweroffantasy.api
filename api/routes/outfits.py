
from fastapi import APIRouter

from api.enums import OUTFITS, LANGS, VERSIONS

from api.core.response import PrettyJsonResponse

from api.infra.repository import OutfitRepo
from api.infra.entitys import EntityBase, Outfit


OUTFIT_REPO = OutfitRepo()

router = APIRouter(prefix='/outfits', tags=['Outfits'])
METADATA = {
    'name': 'Outfits',
    'description': 'Player\'s cloths \n\n **DOES NOT CONTAINS CN DATA**',
    }


@router.get('/{id}', name='Get outfit', response_model=Outfit)
async def get_outfit(id: OUTFITS, lang: LANGS = LANGS('en'), include: bool = True):
    '''
    **Path Param** \n
        id: 
            type: str
            required: True
            desc: outfit_id

    **Query Params** \n
        lang:
            type: string
            default: en
            desc: possible languages to use
        
        include:
            type: bool
            default: True
            desc: Include all data keys
            
    **Return** \n
        Outfit
    '''
    
    outfit = await OUTFIT_REPO.get(EntityBase(id=id), lang, VERSIONS('global'))
    if include:
        return PrettyJsonResponse(outfit.model_dump())
    else:
        return PrettyJsonResponse(outfit.model_dump(include={'name', 'icon'}))



@router.get('', name='All outfits', response_model=list[Outfit])
async def get_all_outfits(lang: LANGS = LANGS('en'), include: bool = False):
    '''
    **Query Params** \n
        lang:
            type: string
            default: en
            desc: possible languages to use

        include:
            type: bool
            default: False
            desc: Include all data keys
            
    **Return** \n
        List[Outfit]
    '''
    
    outfits = await OUTFIT_REPO.get_all(lang, VERSIONS('global'))
    if include:
        return PrettyJsonResponse([outfit.model_dump() for outfit in outfits])
    else:
        return PrettyJsonResponse([outfit.model_dump(include={'name', 'icon'}) for outfit in outfits])
    
