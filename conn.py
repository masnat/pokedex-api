import sqlalchemy as db

dbengine = "postgresql"
username = "postgres"
password = ""
if(password):
    password = ":"+password

print(password)
host = "localhost"
port = 5432
dbname = "pokedex"
engine = db.create_engine(dbengine+"://"+username+password+"@"+host+":"+str(port)+"/"+dbname)