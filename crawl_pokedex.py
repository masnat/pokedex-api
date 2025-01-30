from conn import *
import requests
from bs4 import BeautifulSoup

source_url = "https://pokemondb.net"
sess = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries = 3)
sess.mount('https://', adapter)
req = sess.get(source_url+"/pokedex/all")

soup = BeautifulSoup(req.content, "html.parser")
# print(soup.prettify())
tbl = soup.find("table", id="pokedex")
tbody = tbl.find("tbody")
rows = tbody.find_all("tr")
# print(rows)

for r in rows:
    conn = engine.connect()
    # r = rows
        # col = r.find_all("td")
        # print(col)
    pokemon_code = r.select("td:nth-child(1) > .infocard-cell-data")[0].text
    pokemon_name = r.select("td:nth-child(2) > .ent-name")[0].text
    pokemon_link = r.select("td:nth-child(2) > .ent-name")[0].get('href')
    pokemon_types = r.select("td:nth-child(3) > a")

    poketypes = []
    for tp in pokemon_types:
        poketypes.append(tp.text)

    pokemon_total = r.select("td:nth-child(4)")[0].text
    pokemon_hp = r.select("td:nth-child(5)")[0].text
    pokemon_attack = r.select("td:nth-child(6)")[0].text
    pokemon_defense = r.select("td:nth-child(7)")[0].text
    pokemon_sp_attack = r.select("td:nth-child(8)")[0].text
    pokemon_sp_def = r.select("td:nth-child(9)")[0].text
    pokemon_speed = r.select("td:nth-child(10)")[0].text

    req = sess.get(source_url+pokemon_link)
    soup = BeautifulSoup(req.content, "html.parser")
    mainpage = soup.find("main", id="main")
    p1 = mainpage.select("p")[0]
    p2 = mainpage.select("p")[1]
    pokemon_desc = str(p1) + str(p2)

    # print(pokemon_code)
    # print(pokemon_name)
    # print(pokemon_link)
    # print(pokemon_desc)
    # print(pokemon_types)
    # print(poketypes)
    # print(pokemon_total)
    # print(pokemon_hp)
    # print(pokemon_attack)
    # print(pokemon_defense)
    # print(pokemon_sp_attack)
    # print(pokemon_sp_def)
    # print(pokemon_sp_attack)
    # print(pokemon_speed)

    pokemons = conn.execute(db.text("INSERT INTO pokemons(pokemon_code, pokemon_name \
    , pokemon_hp, pokemon_attack, pokemon_defense, pokemon_sp_attack \
    , pokemon_sp_defense, pokemon_speed, pokemon_total, pokemon_desc) \
    VALUES (:pokemon_code, :pokemon_name, :pokemon_hp \
        , :pokemon_attack, :pokemon_defense \
            , :pokemon_sp_attack, :pokemon_sp_def \
            , :pokemon_speed, :pokemon_total, :pokemon_desc) \
    ON CONFLICT (pokemon_code) DO UPDATE \
    SET pokemon_code = excluded.pokemon_code \
    RETURNING pokemon_id"), {
        'pokemon_code': pokemon_code, 
        'pokemon_name': pokemon_name,
        'pokemon_hp': pokemon_hp,
        'pokemon_attack': pokemon_attack,
        'pokemon_defense': pokemon_defense,
        'pokemon_sp_attack': pokemon_sp_attack,
        'pokemon_sp_def': pokemon_sp_def,
        'pokemon_speed': pokemon_speed,
        'pokemon_total': pokemon_total,
        'pokemon_desc': pokemon_desc,
    })
    [pokemon_id] = pokemons.fetchone()

    for tp in poketypes: 
        types = conn.execute(db.text("INSERT INTO types(type_name) \
        VALUES (:type_name) \
        ON CONFLICT (type_name) DO UPDATE \
        SET type_name = excluded.type_name \
        RETURNING type_id"), {
            'type_name': tp
        })
        [type_id] = types.fetchone()

        pokemontype_code = pokemon_code+"_"+tp
        
        poketypes = conn.execute(db.text("INSERT INTO pokemon_types(pokemon_id, type_id, pokemontype_code) \
        VALUES ("+str(pokemon_id)+", "+str(type_id)+", '"+pokemontype_code+"') \
        ON CONFLICT (pokemontype_code) DO UPDATE \
        SET pokemontype_code = excluded.pokemontype_code \
        RETURNING pokemontype_id"))
        [pokemontype_id] = poketypes.fetchone()

    conn.commit()
    conn.close()
    print("Crawl data success!")