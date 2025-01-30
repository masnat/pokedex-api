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
pip install pyscopg2
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
