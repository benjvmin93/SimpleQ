# SimpleQ

>***Simple and liteweight Quantum emulator. The goal is to implement a centered API for future projects such as a library or an online graph editor !***

*Please make sure to read everything as you need to configure the project before running it!*
## Table of Contents

>- [Features](#features)
>- [Getting Started](#getting-started)
>  - [Prerequisites](#prerequisites)
>  - [Installation](#installation)
>- [Usage](#usage)
>- [Contributing](#contributing)
>- [License](#license)
>- [Acknowledgments](#acknowledgments)

## features

  - 1 qubit gates (H, X, Y, Z)
  - Multicontrol gates (the users are able to build any 1 qubit gates with an arbitrary number of controls)
  - Simulated measurement

## getting-started

In order to execute this API correctly, there are some Prerequisites and setups you need , but hey ! We did our best to make it as easy as possible !

### Prerequisites

- ```Python version : 3.10+```
- Windows 8+
- Docker Desktop

### Installation

in order to start your API, you need some setup:

>- create an ```.env``` file containing two variables at the root of the project :
    - ```POSTGRES_PASSWORD=#YOUR_PASSWORD_HERE#``` Put your current Postgres password here, if you forgot it or didnt set it up, no worries ! we are covering it underneath (1)
    - ```POSTGRES_DB=#YOUR_BD_NAME_HERE#```
>- run ```docker-compose up --build``` to execute the project !
>- head to http://127.0.0.1:8000/ to test your endpoints !

*(1): in case you have forgotten your Postgres Password or havent set it up yet, execute ```docker exec -it postgres-container psql -U postgres``` and then simply change your password with the following SQL command : ```ALTER USER postgres PASSWORD 'password_inside_your_env_file';``` and exit the prompt with ```\q```*

## Usage

### Initiate the Database

>if you run the project for the first time you might have to modify the ```docker-compose.yml``` file as you can configurate it at your needs ! head down to the alembic environment variable section called ``ALEMBIC_MODE``. you can change its value to your desired mode:
>- **init** : migrate and initiate the database (necessary at the first run)
>- **upgrade** : if you add new models, this mode will update the database
>- **reset** : reset the database
>- **none** : sometimes you might want to keep things simple and change nothing :)

### Access the Database
- ```docker exec -it postgres-container psql -U postgres```

  //TODO ! (mini doc)

## Contributing

>1. Fork it !
>2. Create your feature branch: ``git checkout -b my-new-feature``
>3. Commit your changes: ``git commit -am 'Add some feature'``
>4. Push to the branch: ``git push origin my-new-feature``
>5. Submit a pull request and you are set ! thanks for your contribution !

## license

The MIT License (MIT)

Copyright (c) 2023 Bouyjou Maximilien, Guichard Benjamin

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## acknowledgments

  //TODO ! (quirks/qiskit ?)
