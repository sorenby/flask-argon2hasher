__version_info__ = ("0", "9", "2")
__version__ = ".".join(__version_info__)
__author__ = "Andreas Sörenby"
__author_email__ = "sorenby@abaddon.se"

from argon2.low_level import Type
import os

# Default type for argon2 (Recommended)
ARGON2HASHER_TYPE = Type.ID
# Default version for argon2 (Recommended)
ARGON2HASHER_VERSION = 19
# Default salt lenght value for argon2 (Recommended)
ARGON2HASHER_SALT_LEN = 16
# Default hash lenght value for argon2 (Recommended)
ARGON2HASHER_HASH_LEN = 32
# Default time cost value for argon2 (Recommended)
ARGON2HASHER_TIME_COST = 1
# Default memory cost value for argon2 (Recommended)
ARGON2HASHER_MEMORY_COST = 2097152
# Default parallelism value for argon2 (Recommended)
ARGON2HASHER_PARALLELISM = 4
# Default encoding
ARGON2HASHER_ENCODING = 'utf-8'
# Default profile for argon2 (Recommended)
ARGON2HASHER_PROFILE= 'Default'
# If value = False don´t use pepper, if value = True use APP_SECRET_KEY as pepper or if value = "String" use "String" as pepper. 
ARGON2HASHER_PEPPER = False

__PROTECTED_PROFILES__ = [
    "RFC_9106_HIGH_MEMORY", "RFC_9106_LOW_MEMORY", "DEFAULT", "USER_DEFINED", 
]

__PROTECTED_WORDS__ = [
    "LOAD_JSON", "ADD_PROFILE", "DELETE_PROFILE", "CONVERT_STRING",
    "CLEAR", "COPY", "DATA", "FROMKEYS", "GET",
    "ITEMS", "KEYS", "POP", "POPITEM",
    "SETDEFAULT", "UPDATE", "VALUES",
    ]

__PROFILES__ = os.path.join(os.path.dirname(__file__), 'profiles.json')