from models import create_tables, db

if db.is_closed():
    db.connect() 
create_tables()
db.close()

