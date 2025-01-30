from conn import *
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import sys

class Server(BaseHTTPRequestHandler):
    
    def do_GET(self):
        
        # pathlist = self.path.split('/')
        # print(pathlist)
        
        parsed_url = urlparse(self.path)
        pathlist = parsed_url.path.split('/')
        pokemon_path = ''
        pokemon_id = '0'
        # print(pathlist)
        # exit()
        if(len(pathlist) >= 2):
            pokemon_path = pathlist[1]
        if(len(pathlist) >= 3):
            pokemon_id = pathlist[2]
        query_params = parse_qs(parsed_url.query)
        include_qparam = query_params.get('include')

        include_exist = False
        if(include_qparam) :
            include_exist = list(filter(lambda x: x == "type", include_qparam))

        # print(include_qparam)
        # print(query_params.get('include'))
        # if self.path == '/':
        #     self.path = '/index.html'
        # print(pokemon_path)
        # print(pokemon_id)
        if(pokemon_path != 'pokemons') :
            err_response = json.dumps({"errors": [{"status": "400", "detail": "Data not found"}]})
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(err_response.encode("utf-8"))
            return 0
            
        try:
            # file_to_open = open(self.path[1:]).read()
            # self.send_response(200)
            # self.send_header('Content-type', 'text/html')
            # self.end_headers()
            # self.wfile.write(bytes(file_to_open, 'utf-8'))
            conn = engine.connect()

            # print('pokemonxxx')
            # print(pokemon_id)
            if(int(pokemon_id) > 0) :
                print('pokemonxxx')
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

                # relationships = {}

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
                    # print('xxxxxaa')
                    temp_jsonapi["included"] = included
                    # print(temp_jsonapi)

                # print(temp_jsonapi)
                jsonapi = temp_jsonapi

            else:
                pokemonquery = conn.execute(db.text("SELECT * FROM pokemons ORDER BY pokemon_id LIMIT 10"))
                pokemonfetch = pokemonquery.fetchall()
                # print(len(pokemonfetch))
                # print(len(pokemonfetch) <= 0)
                if(len(pokemonfetch) <= 0):
                    err_response = json.dumps({"errors": [{"status": "400", "detail": "Data not found"}]})
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(err_response.encode("utf-8"))
                    return 0
                # print('xxxxx')
                i = 0
                jsonapi = []
                for poke in pokemonfetch:
                    pokemon = poke._asdict()
                    # print("xxx")
                    # print(pokemon)
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
                    # print(pokemontypes)
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
                        # print('xxxxxaa')
                        temp_jsonapi["included"] = included

                    temp_jsonapi["meta"] = {
                        "total_pages": 5,
                        "total_count": 100
                    }
                    temp_jsonapi["links"] = {
                        "self": "/pokemons?page=1",
                        "next": "/pokemons?page=2"
                    }

                    jsonapi.append(temp_jsonapi)

                conn.commit()
                conn.close()
                
                # jsonresponse = json.dumps(jsonapi)

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