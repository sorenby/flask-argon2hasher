from argon2._utils import Parameters, _check_types
from argon2.low_level import Type
from collections import UserDict
from typing import Optional
from dataclasses import dataclass
from unicodedata import normalize

import json
from .config import __PROFILES__, __PROTECTED_PROFILES__, __PROTECTED_WORDS__

@dataclass
class Params(Parameters):
    def _check_types(self) -> Optional[str]:
        _return = True
        for name, field_def in self.__dataclass_fields__.items():
            actual_type = type(getattr(self, name))
            if actual_type != field_def.type:
                _return = False
        return _return

    def __post_init__(self):
         if not self._check_types():
             raise ValueError('Wrong types')

class Profiles(UserDict):
    """
    Argon2 hasher parameter profiles dictionary, with hardcoded "DEFAULT" profile and self loading profiles from json file.

    Availible methods:

    load_json(filename=file.json)

    add_profile(name="PROFILE NAME", profile=parameter_object)

    delete_profile(name="PROFILE NAME")
    """
    def __init__(self):
        super().__init__(self)
        self.__setitem__("DEFAULT", 
            Params(
                type=Type.ID,
                version=19,
                salt_len=16,
                hash_len=32,
                time_cost=1,
                memory_cost=2097152,
                parallelism=4
                )
            )
        self.load_json()

    def __setitem__(self, key: str = None, item: Params = None) -> None:
        """Set a key/value pair, converts keys to uppercase"""
        key = self.convert_string(key)
        try:
            if key not in self.data and key in __PROTECTED_PROFILES__:
                setattr(self, key, item)
                return super().__setitem__(key, item)
            elif key in __PROTECTED_WORDS__ or key in __PROTECTED_PROFILES__ or key.startswith("__") or key.startswith("_"):
                print(f"Error (Protected name): {key}")
            else:
                setattr(self, key, item)
                return super().__setitem__(key, item)
        except Exception as e:
            print(f"Invalid: {e}")

    def __getitem__(self, key: str = None) -> Params:
        """Get a parameter, converts the key to uppercase before searching"""
        key = self.convert_string(key)
        try:
            return super().__getitem__(key)
        except:
            return super().__getitem__("DEFAULT")

    def load_json(self, filename: str = __PROFILES__):
        """ Loads profiles from a JSON file """

        try:
            with open(__PROFILES__, 'r') as profiles:
                    self._json = json.load(profiles)
        except IOError as e:
            print(f"Couldn´t open %s: %s" % (__PROFILES__, e))
        try:
            for profile in self._json:
                _type_in_json = self._json[profile]['type']
                if _type_in_json.upper() == "I":
                    _type = Type.I
                elif _type_in_json.upper() == "D":
                    _type = Type.D
                else:
                    _type = Type.ID
                _profile = Params(
                    type=_type,
                    version=self._json[profile]['version'],
                    salt_len=self._json[profile]['salt_len'],
                    hash_len=self._json[profile]['hash_len'],
                    time_cost=self._json[profile]['time_cost'],
                    memory_cost=self._json[profile]['memory_cost'],
                    parallelism=self._json[profile]['parallelism']
                )
                self.__setitem__(profile, _profile)
        except Exception as e:
            print(f"Couldn´t load profile from json: {e}")
    
    def add_profile(self, name: str, profile: Params) -> None:
        """Adds a new profile to the dictionary."""

        try:
            self.__setitem__(name, profile)
        except Exception as e:
            print(f"Couldn´t add profile: {name}")

    def delete_profile(self, name: str) -> None:
        """Deletes a profile."""

        name = self.convert_string(name)
        try:
            if name not in __PROTECTED_WORDS__ and name not in __PROTECTED_PROFILES__:
                if name.startswith("__") or name.startswith("_"):
                    print(f"Couldn´t delete profile: {name}")
                else:
                    self.__delattr__(name)
                    self.data.pop(f"{name}", f'No such profile: {name}')
            else:
                print(f"Couldn´t delete profile: {name}")
        except Exception as e:
            print(f"Couldn´t delete profile: {name}")

    def convert_string(self, string: str = None) -> str:
        """Convert string to uppercase without unicode characters."""

        return normalize("NFKD", string).upper().encode('ascii', 'ignore').decode()
