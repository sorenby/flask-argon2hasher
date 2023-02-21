# Flask-Argon2Hasher

Flask-Argon2Hasher is a Flask extension that provides Argon2 hashing utilities for
your Flask app. 

## Installation

Install the extension with the following command:

    $ pip install flask-argon2hasher

## Quickstart
To use the extension import the Argon2Hasher class.

    from flask import Flask
    from flask_argon2hasher import Argon2Hasher

Then either instantiate the class by passing your Flask app to it.

    app = Flask(__name__)
    argon2hasher = Argon2Hasher(app)

Or if you use the Application Factory pattern.

    argon2hasher = Argon2Hasher()

    def init_app():
        app = Flask(__name__)
        argon2hasher.init_app(app)

        return app

## Usage
There´s a couple of different way to hash passwords using the extension.

    password_hash_example1a = argon2hasher.hash("MySuperSecretPassword")
    password_hash_example1b = argon2hasher.generate_password_hash("MySuperSecretPassword")
    
    password_hash_example2a = app.password.hash("MySuperSecretPassword")
    password_hash_example2b = app.password.generate_password_hash("MySuperSecretPassword")

To verify if a password is correct use one of the following examples.

    if argon2hasher.verify(password_hash_example1a, "MySuperSecretPassword"):
        print("Password match!")
    else:
        print("Incorrect password!")

or

    argon2hasher.check_password_hash(password_hash_example1b, "MySuperSecretPassword"):
    app.password.verify(password_hash_example2a, "MySuperSecretPassword")
    app.password.check_password_hash(password_hash_example2b, "MySuperSecretPassword")

## Configurations
It´s easy to configure Flask-Argon2Hasher using Flask configuration values. The default configuration are the per RFC 9106 recommended settings.
There are several different predefined configuration profiles available.
- RFC_9106_LOW_MEMORY
- RFC_9106_HIGH_MEMORY (***default***)
- TESTING_ONLY_PROFILE

The following configuration options are available.

| Variable Name | Description | Type | Default |
|------|------|------|------|
|`ARGON2HASHER_TYPE`| Choose whether you want Argon2i ("I"), Argon2d ("D"), or Argon2id ("ID"). If you don’t know what that means, choose "ID". | *string* | **"ID"** |
|`ARGON2HASHER_VERSION`| The latest supported version of the Argon2 algorithm is 19. | *integer* | **19** |
|`ARGON2HASHER_SALT_LEN`| Length of random salt to be generated for each password. | *integer* | **16** |
|`ARGON2HASHER_HASH_LEN`| Length of the hash in bytes. | *integer* | **32** |
|`ARGON2HASHER_TIME_COST`| Defines the amount of computation realized and therefore the execution time, given in number of iterations. | *integer* | **1** |
|`ARGON2HASHER_MEMORY_COST`| Defines the memory usage, given in kibibytes. | *integer* | **2097152** |
|`ARGON2HASHER_PARALLELISM`| Defines the number of parallel threads (changes the resulting hash value). | *integer* | **4** |
|`ARGON2HASHER_ENCODING`| The Argon2 C library expects bytes. So if hash() or verify() are passed a str, it will be encoded using this encoding. | *string* | **"utf-8"** |
|`ARGON2HASHER_PEPPER`| Add a pepper to the password. | *string* or *boolean* | **False** |
|`ARGON2HASHER_PROFILE`| Use a predefined profile. | *string* | **"Default"** |
|`ARGON2HASHER_PROFILES_JSON`| Load user defined profiles from JSON file. | *string* or *bool* | **False** |

You can create your own configuration profiles in a JSON file with the following syntax.

    {
        "MY_FIRST_PROFILE": {
            "type" : "ID",
            "version" : 19,
            "salt_len" : 16,
            "hash_len" : 32,
            "time_cost" : 3,
            "memory_cost" : 65536,
            "parallelism" : 4
        },
        "MY_SECOND_PROFILE": {
            "type" : "ID",
            "version" : 19,
            "salt_len" : 16,
            "hash_len" : 32,
            "time_cost" : 1,
            "memory_cost" : 2097152,
            "parallelism" : 4
        }
    }

Save the JSON in your project folder and update your configuration accordingly.

    ARGON2HASHER_PROFILES_JSON = "my_argon2_profiles.json"

### Pepper

You have the option of using a password pepper by setting ARGON2HASHER_PEPPER to either a string or boolean value.
If it´s a boolean value **True**, the password pepper defaults to "***Argon2Pepper***".
Otherwise it will use whatever string value set in ARGON2HASHER_PEPPER.
By default Flask-Argon2Hasher won´t use a pepper, but the option is there if you want it.
If you decide to use it, make sure you store it somewhere ***safe*** and ***NOT*** alongside the password hashes in you database.

> ***WARNING If you loose your pepper all password hashes created with it will be USELESS***. 
  