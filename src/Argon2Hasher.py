try:
    from argon2 import PasswordHasher
    from argon2.low_level import Type
    from argon2.exceptions import Argon2Error, VerifyMismatchError, VerificationError, InvalidHash
except ImportError as e:
    print('argon2_cffi is required to use Flask-Argon2Hasher')
    raise e
from flask import Flask
from typing import Union, Literal
from config import (
    ARGON2HASHER_TYPE,
    ARGON2HASHER_VERSION,
    ARGON2HASHER_SALT_LEN,
    ARGON2HASHER_HASH_LEN,
    ARGON2HASHER_TIME_COST,
    ARGON2HASHER_MEMORY_COST,
    ARGON2HASHER_PARALLELISM,
    ARGON2HASHER_ENCODING,
    ARGON2HASHER_PROFILE,
    ARGON2HASHER_PEPPER,
    )
from profiles import Profiles
from profiles import Params as Parameters

### TODO:
# Add: 
# support for logging
# comments
# README
# LICENSE
# tests (pytest or nox)
# 


class Argon2Hasher():
    def __init__(self, app: Flask = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask = None):
        self.TYPE = app.config.get('ARGON2HASHER_TYPE', ARGON2HASHER_TYPE)
        self.VERSION = app.config.get('ARGON2HASHER_VERSION',ARGON2HASHER_VERSION)
        self.SALT_LEN = app.config.get('ARGON2HASHER_SALT_LEN',ARGON2HASHER_SALT_LEN)
        self.HASH_LEN = app.config.get('ARGON2HASHER_HASH_LEN',ARGON2HASHER_HASH_LEN)
        self.TIME_COST = app.config.get('ARGON2HASHER_TIME_COST',ARGON2HASHER_TIME_COST)
        self.MEMORY_COST = app.config.get('ARGON2HASHER_MEMORY_COST',ARGON2HASHER_MEMORY_COST)
        self.PARALLELISM = app.config.get('ARGON2HASHER_PARALLELISM',ARGON2HASHER_PARALLELISM)
        self.ENCODING = app.config.get('ARGON2HASHER_ENCODING',ARGON2HASHER_ENCODING)
        self.PROFILE = app.config.get('ARGON2HASHER_PROFILE',ARGON2HASHER_PROFILE)
        self.PEPPER = app.config.get('ARGON2HASHER_PEPPER',ARGON2HASHER_PEPPER)
        self.profiles = Profiles()
        self._set_user_defined_profile()
        self._passwordhasher = self._get_passwordhasher()
        app.argon2hasher = self

    def _get_passwordhasher(self):
        passwordhasher = PasswordHasher(encoding=self.ENCODING)
        passwordhasher._parameters = self._select_profile()
        return passwordhasher
    
    def _set_user_defined_profile(self):
        self.profiles.add_profile("USER_DEFINED", Parameters(
            self.TYPE, 
            self.VERSION, 
            self.SALT_LEN, 
            self.HASH_LEN, 
            self.TIME_COST, 
            self.MEMORY_COST, 
            self.PARALLELISM
            )
        )

    def _select_profile(self) -> Parameters:
        if self.profiles['DEFAULT'] != self.profiles['USER_DEFINED']:
            return self.profiles['USER_DEFINED']
        else:
            return self.profiles['DEFAULT']

    def generate_password_hash(self, password: Union[str, bytes]) -> str:
        #Add logging
        _PEPPER = self.PEPPER
        if isinstance(_PEPPER, str):
            #Add logging
            self._passwordhasher.hash(_PEPPER+password)
        elif _PEPPER:
            #Add logging
            _PEPPER = "Argon2Pepper"
            self._passwordhasher.hash(_PEPPER+password)
        else:
            #Add logging
            self._passwordhasher.hash(password)

    def check_password_hash(self, hash: Union[str, bytes], password: Union[str, bytes]) -> Literal[True]:
    #Add logging
        try:
            _PEPPER = self.PEPPER
            if isinstance(_PEPPER, str):
                #Add logging
                return self._passwordhasher.verify(hash, _PEPPER+password)
            elif _PEPPER:
                #Add logging
                _PEPPER = "Argon2Pepper"
                return self._passwordhasher.verify(hash, _PEPPER+password)
            else:
                #Add logging
                return self._passwordhasher.verify(hash, password)
        except VerifyMismatchError:
            #Add logging
            return False
        except VerificationError:
            #Add logging
            return False
        except InvalidHash:
            #Add logging
            return False
        except:
            #Add logging
            return False

# Fast helper function for quick hashing and verifications.
# from flask_argon2hasher import generate_password_hash, check_password_hash

def generate_password_hash(password):
    _passwordhasher = PasswordHasher()
    return _passwordhasher.hash(password)

def check_password_hash(hash, password):
    _passwordhasher = PasswordHasher()
    try:
        result = _passwordhasher.verify(hash, password)
    except VerifyMismatchError:
        #Add logging
        return False
    except VerificationError:
        #Add logging
        return False
    except InvalidHash:
        #Add logging
        return False

passhash = generate_password_hash("somepassword")

verify = check_password_hash(passhash, "somepdassword")

print(verify)
