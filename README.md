# Pokedex-API

Pokedex-API is the simple web application that serve Pokemon's data through REST-API.

## Source

[Pokemon Dex](https://pokemondb.net/pokedex/all)

## Configuration

- Create database named `pokedex`. This web application using database PostgreSQL.
- Change database configuration in `conn.py`.

## Instalation

```bash
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
