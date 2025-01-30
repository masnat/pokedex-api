# Pokedex-API

Pokedex-API is the simple web application that serve Pokemon's data through REST-API.

## Source

[Pokemon Dex](https://pokemondb.net/pokedex/all)

## Configuration

- Create database named `pokedex`. This web application using database PostgreSQL.
- Change database configuration in `conn.py`.

## Instalation

```bash
# install virtual environment for linux or mac (skip if you use global environment)
# read this for the detail configuration https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
python3 -m venv .venv
source .venv/bin/activate

# upgrade pip module if needed
python3 -m pip install --upgrade pip

# module for get the crawl page
pip install requests
# module for easy process the elements in the page
pip install beautifulsoup4
# module db driver for postgresql
pip install psycopg2
# module for running multiple db driver
pip install sqlalchemy
```

## Usage

### Crawl Data

```bash
# generate table
python generate_table.py
# start crawl
python crawl_pokedex.py
```

### Running Rest-API

```bash
# generate table
python server.py
```

- Url for list all pokemon `http://localhost:8000/pokemons`
- Url for list all pokemon with query params `http://localhost:8000/pokemons?include=type&page[number]=1&page[size]=10`
- Url for get pokemon by id `http://localhost:8000/pokemons/{pokemon_id}`
- Url for get random pokemon `http://localhost:8000/pokemons/0`
