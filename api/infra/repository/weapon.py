
import json

from pathlib import Path
from typing import Any

from api.infra.repository.base_repo import ModelRepository
from api.infra.entitys import Weapon, EntityBase

from api.core.exceptions import VersionNotFound, LanguageNotFound, FileNotFound

from api.enums import LANGS, LANGS_CN, VERSIONS
from api.utils import sort_weapons
from api.config import GB_BANNERS


class WeaponRepo(ModelRepository[EntityBase, Weapon]):
    cache = {}
    __load_all_data__: bool = False

    def __init__(self) -> None:
        super().__init__(model_base=EntityBase, 
                         model=Weapon, 
                         class_base=WeaponRepo,
                         repo_name='weapons')
        
        self.META_GB: dict[str, dict[str, list[Any]]] = json.loads(Path('api/infra/database/global/meta.json').read_bytes())
    
    async def get_all(self, lang: LANGS | LANGS_CN | str, version: VERSIONS) -> list[Weapon]:
        if version in self.class_base.cache:
            if lang in self.class_base.cache[version]:
                return list(self.class_base.cache[version][lang].values())

        VERSION_PATH = Path(f'api/infra/database/{version}')
        if not VERSION_PATH.exists():
            raise VersionNotFound(version)
        
        LANG_PATH = Path(VERSION_PATH, lang)
        if not LANG_PATH.exists():
            raise LanguageNotFound(lang, version)

        FILEPATH = Path(LANG_PATH, f'{self.repo_name}.json')
        if not FILEPATH.exists():
            raise FileNotFound(self.repo_name, lang, version)

        DATA: dict[str, dict[str, Any]] = json.loads(FILEPATH.read_bytes())

        if version not in self.cache:
            self.cache.update({version: {}})

        if lang not in self.cache[version]:
            self.cache[version].update({lang: {}})

        for key_id, value_dict in DATA.items():
            weaponEffects: list[dict[str, str]] = []

            if advancements := value_dict.get('WeaponAdvancements', []):
                if description := advancements[0].get('Description', None):
                    if '*:' in description:
                        weaponEffect = description.split('\r', 1)

                        for i in weaponEffect:
                            key, value_ = i.split('*:', 1)
                            key = key.replace('*', '').replace('\n', '').replace('\r', '')
                            value_ = value_.replace('\n', '').replace('\r', '').replace(' ', '', 1)
                            weaponEffects.append({'title': key, 'description': value_})

                    else:
                        if value_dict['id'].lower() == 'fan_superpower':
                            weaponEffects.append({'title': 'Altered Damage', 'description': description.replace('\n', ' ').replace('\r', '')})

                        else:
                            weaponEffects.append({'title': 'Unknown', 'description': description.replace('\n', ' ').replace('\r', '')})

            value_dict.update({
                    'WeaponEffects': weaponEffects, 
                    'Shatter': value_dict['WeaponAdvancements'][0]['Shatter'],
                    'Charge': value_dict['WeaponAdvancements'][0]['Charge']
                })
            

            if len(value_dict['WeaponAdvancements']) == 7:
                value_dict['WeaponAdvancements'].pop(0)
            

            if version == 'global':
                value_dict['Meta'] = self.META_GB.get(key_id.lower(), None)
                value_dict['Banners'] = [banner for banner in GB_BANNERS if banner.weapon_id and banner.weapon_id == key_id.lower()]

            if value_dict.get('id', None):
                self.cache[version][lang].update({key_id.lower(): Weapon(**value_dict)})
            else:
                self.cache[version][lang].update({key_id.lower(): Weapon(**value_dict, id=key_id)})

        self.cache[version][lang] = {i.id: i for i in list(sorted(list(self.cache[version][lang].values()), key=sort_weapons))}

        return list(self.cache[version][lang].values())
