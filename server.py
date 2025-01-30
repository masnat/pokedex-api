from conn import *
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json, math, random

class Server(BaseHTTPRequestHandler):
    
    def do_GET(self):
        
        parsed_url = urlparse(self.path)
        pathlist = parsed_url.path.split('/')
        pokemon_path = ''
        pokemon_id = '-1'

        if(len(pathlist) >= 2):
            pokemon_path = pathlist[1]
        if(len(pathlist) >= 3):
            pokemon_id = pathlist[2]
        query_params = parse_qs(parsed_url.query)
        include_qparam = query_params.get('include')
        page_qparam = query_params.get('page[number]')
        size_qparam = query_params.get('page[size]')
        # print('page_qparam')
        # print(page_qparam)
        page = 1
        limit = 10
        
        if(page_qparam != None):
            page = int(page_qparam[0])

        if(size_qparam != None):
            limit = int(size_qparam[0])

        include_exist = False
        if(include_qparam) :
            include_exist = list(filter(lambda x: x == "type", include_qparam))

        if(pokemon_path != 'pokemons') :
            err_response = json.dumps({"errors": [{"status": "400", "detail": "Data not found"}]})
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(err_response.encode("utf-8"))
            return 0
            
        try:

            conn = engine.connect()
            
            if(int(pokemon_id) >= 0) :
                if(int(pokemon_id) == 0): # get random pokemon
                    pokemonids_query = conn.execute(db.text("SELECT pokemon_id FROM pokemons"))
                    pokemondatas = pokemonids_query.fetchall()
                    pokemonids = []
                    for id in pokemondatas:
                        poke = id._asdict()
                        pokemonids.append(poke["pokemon_id"])
                        
                    # print(pokemonids)
                    pokemon_id = random.choice(pokemonids)
                    pokemonquery = conn.execute(db.text("SELECT * FROM pokemons WHERE pokemon_id = :pokemon_id ORDER BY pokemon_id LIMIT 1"), {"pokemon_id": pokemon_id})

                else :
                    pokemonquery = conn.execute(db.text("SELECT * FROM pokemons WHERE pokemon_id = :pokemon_id ORDER BY pokemon_id LIMIT 1"), {"pokemon_id": pokemon_id})

                pokemonfetch = pokemonquery.fetchone()
                # print(pokemonfetch)
                if(pokemonfetch == None):
                    err_response = json.dumps({"errors": [{"status": "400", "detail": "Data not found"}]})
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(err_response.encode("utf-8"))
                    return 0
                
                pokemon = pokemonfetch._asdict()
                pokemontypequery = conn.execute(db.text("SELECT types.type_id, type_name FROM types JOIN pokemon_types ON pokemon_types.type_id = types.type_id WHERE pokemon_id = :pokemon_id"), {"pokemon_id": pokemon['pokemon_id']})
                pokemontypes = pokemontypequery.fetchall()
                # print(pokemontypes)
                conn.commit()
                conn.close()

                included = []
                if(len(pokemontypes) > 1):
                    relationships = {
                        "type" : {
                            "data": []
                        }
                    }
                else:
                    relationships = {
                        "type" : {
                            "data": {}
                        }
                    }

                if(pokemontypes):
                    for ptype in pokemontypes:
                        pt = ptype._asdict()
                        # print(pt)
                        if(len(pokemontypes) > 1):
                            relationships["type"]["data"].append({
                                        "type": "type", 
                                        "id": pt['type_id']
                                    })
                        else:
                            relationships["type"]["data"] = {
                                        "type": "type", 
                                        "id": pt['type_id']
                                    }
                            
                        # print(relationships)
                        
                        if(include_exist and 'type' in include_qparam):
                            included.append({
                                "type": "type",
                                "id": pt['type_id'],
                                "attributes": {
                                    "name": pt['type_name']
                                }
                            })

                # format as jsonapi.org
                temp_jsonapi = {
                    "data": [
                        {
                            "type": "pokemons",
                            "id": pokemon['pokemon_id'],
                            "attributes": {
                                "name": pokemon['pokemon_name'],
                                "description": pokemon['pokemon_desc']
                            },
                            "relationships": relationships
                        }
                    ],
                }
                
                # print(include_exist)
                if(include_exist and 'type' in include_qparam):
                    temp_jsonapi["included"] = included

                # print(temp_jsonapi)
                jsonapi = temp_jsonapi

            else:
                limit_page = limit
                offset_page = 0
                if(page > 1):
                    offset_page = limit_page * (int(page) - 1)
                # print(limit)
                # print(limit_page)
                # print(offset_page)
                pokemontotal_query = conn.execute(db.text("SELECT COUNT(*) as total FROM pokemons LIMIT 1"))
                pokemontotal = pokemontotal_query.fetchone()._asdict()
                # print(pokemontotal)
                pokemonquery = conn.execute(db.text("SELECT * FROM pokemons ORDER BY pokemon_id LIMIT :limit OFFSET :offset"), {"limit": limit_page, "offset": offset_page})
                pokemonfetch = pokemonquery.fetchall()
                # print(pokemonfetch)
                if(len(pokemonfetch) <= 0):
                    err_response = json.dumps({"errors": [{"status": "400", "detail": "Data not found"}]})
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(err_response.encode("utf-8"))
                    return 0
                
                jsonapi = []
                for poke in pokemonfetch:
                    pokemon = poke._asdict()
                    
                    pokemontypequery = conn.execute(db.text("SELECT types.type_id, type_name FROM types JOIN pokemon_types ON pokemon_types.type_id = types.type_id WHERE pokemon_id = :pokemon_id"), {"pokemon_id": pokemon['pokemon_id']})
                    pokemontypes = pokemontypequery.fetchall()
                    
                    included = []
                    if(len(pokemontypes) > 1):
                        relationships = {
                            "type" : {
                                "data": []
                            }
                        }
                    else:
                        relationships = {
                            "type" : {
                                "data": {}
                            }
                        }
                        
                    if(pokemontypes):
                        for ptype in pokemontypes:
                            pt = ptype._asdict()
                            # print(pt)
                            if(len(pokemontypes) > 1):
                                relationships["type"]["data"].append({
                                            "type": "type", 
                                            "id": pt['type_id']
                                        })
                            else:
                                relationships["type"]["data"] = {
                                            "type": "type", 
                                            "id": pt['type_id']
                                        }
                            
                            if(include_exist and 'type' in include_qparam):
                                included.append({
                                    "type": "type",
                                    "id": pt['type_id'],
                                    "attributes": {
                                        "name": pt['type_name']
                                    }
                                })
                    # print(relationships)

                    # format as jsonapi.org
                    temp_jsonapi = {
                        "data": [
                            {
                                "type": "pokemons",
                                "id": pokemon['pokemon_id'],
                                "attributes": {
                                    "name": pokemon['pokemon_name'],
                                    "description": pokemon['pokemon_desc']
                                },
                                "relationships": relationships
                            }
                        ],
                    }
                    
                    # print(include_exist)
                    if(include_exist and 'type' in include_qparam):
                        temp_jsonapi["included"] = included

                    jsonapi.append(temp_jsonapi)


                total_pages = math.ceil(pokemontotal['total'] / limit_page)
                total_count = pokemontotal['total']
                jsonapi.append(
                    {
                        "meta" : {
                            "total_pages": total_pages,
                            "total_count": total_count
                        }
                    }
                )
                links = {
                    "links" : {
                        "self": "/"+pokemon_path+"?page="+str(page),
                        "first": "/"+pokemon_path+"?page=1",
                        "last": "/"+pokemon_path+"?page="+str(total_pages),
                    }
                }
                if(page > 1):
                    prevpage = page - 1
                    links["links"]["prev"] = "/pokemons?page="+str(prevpage)

                if(total_pages > page):
                    nextpage = page + 1
                    links["links"]["next"] = "/pokemons?page="+str(nextpage)
                    

                jsonapi.append(links)

                conn.commit()
                conn.close()
                
            jsonresponse = json.dumps(jsonapi)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(jsonresponse.encode('utf-8'))

        except:
            err_response = json.dumps({"errors": [{"status": "400", "detail": "Data not found"}]})
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(err_response.encode("utf-8"))


httpd = HTTPServer(('', 8000), Server)
httpd.serve_forever()