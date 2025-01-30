from conn import *

conn = engine.connect()

conn.execute(db.text("""CREATE TABLE IF NOT EXISTS pokemons(
                        pokemon_id SERIAL PRIMARY KEY,
                        pokemon_code VARCHAR(4) UNIQUE NOT NULL,
                        pokemon_name VARCHAR(20) NOT NULL,
                        pokemon_hp INT DEFAULT 0,
                        pokemon_attack INT DEFAULT 0,
                        pokemon_defense INT DEFAULT 0,
                        pokemon_sp_attack INT DEFAULT 0,
                        pokemon_sp_defense INT DEFAULT 0,
                        pokemon_speed INT DEFAULT 0,
                        pokemon_total INT DEFAULT 0,
                        pokemon_desc TEXT
                    );"""))

conn.execute(db.text("""CREATE TABLE IF NOT EXISTS types(
                        type_id SERIAL PRIMARY KEY,
                        type_name VARCHAR(10) UNIQUE NOT NULL
                    );"""))

conn.execute(db.text("""CREATE TABLE IF NOT EXISTS pokemon_types(
                        pokemontype_id SERIAL PRIMARY KEY,
                        pokemon_id INT NOT NULL,
                        type_id INT NOT NULL,
                        pokemontype_code VARCHAR(30) UNIQUE NOT NULL,
                        CONSTRAINT fk_pokemon FOREIGN KEY(pokemon_id) REFERENCES pokemons(pokemon_id),
                        CONSTRAINT fk_type FOREIGN KEY(type_id) REFERENCES types(type_id)
                    );"""))

conn.commit()

conn.close()