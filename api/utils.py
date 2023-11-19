
import re

from typing import TYPE_CHECKING

from api.enums import LANGS

if TYPE_CHECKING:
    from api.infra.entitys import Simulacra, Weapon, Matrix


def bold_numbers(text: str):
    return re.sub(r'\d+(.\d+)?%?', lambda x: f'**{x.group(0)}**' 
                  if text[x.span(0)[0]-1] not in ('*', '+', '-') or text[x.span(0)[1]] not in ('*', '+', '-') else x.group(0), 
                  text.replace('<shuzhi>', '').replace('</>', ''), flags=re.IGNORECASE)

def replace_cv(text: str):
    if not text or text == '':
        return None
    return text.replace('CV : ', '')

def replace_icon(text: str):
    if '/Game/Resources/' in text:
        return text.replace('/Game/Resources', '/assets')
    else:
        return text

def localized_asset(text: str, lang: LANGS):
    return f'/assets/L10N/{lang}/Resources/{text.replace("/Game/Resources/", "")}'

def put_imitation_icon(text: str):
    if '/assets' in text:
        return text
    return f'/assets/UI/huanxing/lihui/{text}'

def check_string(text: str):
    if text.lower() == 'none':
        return None
    return text

def replace_rarity_asset(text: str):
    if text.lower() == 'none':
        return None
    if '/Game/Resources/' in text:
        return text.replace('/Game/Resources', '/assets')
    else:
        return text

def classifier(number: float):
    if number >= 15:
        return 'SS'
    elif number >= 10.01:
        return 'S'
    elif number >= 8:
        return 'A'
    elif number >= 4:
        return 'B'
    else:
        return 'C'
    
def matrice_set_rework(rarity: str, sets: list[dict[str, str]]):
    if rarity == 'N':
        return [{'need': 4, 'description': sets[0].get('2', '')}]
    elif rarity == 'R':
        return [{'need': 3, 'description': sets[0].get('2', '')}]
    elif rarity == 'SR':
        return [{'need': 3, 'description': sets[0].get('2', '')}]
    elif rarity == 'SSR':
        return [{'need': 2, 'description': sets[0].get('2', '')}, 
                {'need': 4, 'description': sets[0].get('4', '')}]
    else:
        return None

def trait_rework(trait: dict[str, dict[str, str]]):
    return [value for key, value in trait.items() if not key == 'id']

def voice_actors_rework(va: list[dict[str, str]]):
    return {key.lower(): value for i in va for key, value in i.items()}

def classify_rework(value: float):
    return {'tier': classifier(value), 'value': value}

def material_rework(mats: dict[str, int]):
    return [{'id': key.lower(), 'need': value} for key, value in mats.items()]

def pet_material_rework(mats: dict[str, int]):
    return [{'id': key.lower(), 'xpGain': value} for key, value in mats.items()]

def relic_advanc_rework(advanc: list[dict[str, str]]):
    return [value for i in advanc for key, value in i.items() if not key == 'id']


def sort_simulacra(simulacrum: 'Simulacra') -> tuple[int, int, str]:
    if not simulacrum.rarity and not simulacrum.banners:
        return 0, 0, simulacrum.name
    
    if simulacrum.rarity == 'SSR':
        if simulacrum.banners:
            return (-simulacrum.banners[-1].bannerNo, -1, simulacrum.name)
        else:
            return (1, -1, simulacrum.name)
        
    elif simulacrum.rarity == 'SR':
        if simulacrum.banners:
            return (-simulacrum.banners[-1].bannerNo, 1, simulacrum.name)
        else:
            return (1, 1, simulacrum.name)
        
    return 1, 2, simulacrum.name

def sort_weapons(weapon: 'Weapon') -> int:
    if not weapon.rarity:
        return 0
    
    if weapon.rarity == 'SSR':
        return -1
    
    elif weapon.rarity == 'SR':
        return 1
    
    elif weapon.rarity == 'R':
        return 2
    
    return 3
    
def sort_matrices(matrice: 'Matrix') -> tuple[int, int]:
    if not matrice.rarity:
        return 0, 0
    
    if matrice.rarity == 'SSR':
        return -1, -int(matrice.id.rsplit('ssr', 1)[1])
    
    elif matrice.rarity == 'SR':
        return 1, -int(matrice.id.rsplit('sr', 1)[1])
    
    elif matrice.rarity == 'R':
        return 2, -int(matrice.id.rsplit('r', 1)[1])

    elif matrice.rarity == 'N':
        return 3, -int(matrice.id.rsplit('n', 1)[1])
    
    return 0, 0