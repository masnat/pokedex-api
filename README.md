# Pokedex-API

Pokedex-API is the simple web application that serve Pokemon's data through REST-API.

## Source

[Pokemon Dex](https://pokemondb.net/pokedex/all)

## Configuration

- create database named `pokedex`
- change database configuration in `conn.py`

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

```bash
#generate table
python generate_table.py
# start crawl
python crawl_pokedex.py
```
