from conn import *

conn = engine.connect()

conn.execute(db.text("""TRUNCATE TABLE pokemons CASCADE;"""))

conn.execute(db.text("""TRUNCATE TABLE types CASCADE;"""))

conn.execute(db.text("""TRUNCATE TABLE pokemon_types;"""))

conn.commit()

conn.close()