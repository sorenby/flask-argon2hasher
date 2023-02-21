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
The following configuration options are available.

| Variable Name | Description | Type | Default |
|------|------|------|------|
|`ARGON2HASHER_TYPE`| Choose whether you want Argon2i ("I"), Argon2d ("D"), or Argon2id ("ID"). If you don’t know what that means, choose "ID". | <str> | "ID" |
|`ARGON2HASHER_VERSION`| The latest supported version of the Argon2 algorithm is 19. | <int> | 19 |
|`ARGON2HASHER_SALT_LEN`| Length of random salt to be generated for each password. | <int> | 16 |
|`ARGON2HASHER_HASH_LEN`| Length of the hash in bytes. | <int> | 32 |
|`ARGON2HASHER_TIME_COST`| Defines the amount of computation realized and therefore the execution time, given in number of iterations. | <int> | 1 |
|`ARGON2HASHER_MEMORY_COST`| Defines the memory usage, given in kibibytes. | <int> | 2097152 |
|`ARGON2HASHER_PARALLELISM`| Defines the number of parallel threads (changes the resulting hash value). | <int> | 4 |
|`ARGON2HASHER_ENCODING`| The Argon2 C library expects bytes. So if hash() or verify() are passed a str, it will be encoded using this encoding. | <str> | "utf-8" |
|`ARGON2HASHER_PEPPER`| Add a pepper to the password. | <str> or <bool> | False |
|`ARGON2HASHER_PROFILE`| Use a predefined profile. | <str> | "Default" |