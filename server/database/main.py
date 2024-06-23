from models import create_tables, User, MissingPerson, Found, db

if db.is_closed():
    db.connect() 
create_tables()
db.close()

