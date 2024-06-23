from peewee import *
import datetime
from babel.dates import format_date

# Define a database connection (Mysql in this case)
db = MySQLDatabase('artificial', host='localhost', port=3306, user='root', password='password')

# Define a base model class that specifies the database
class BaseModel(Model):
    class Meta:
        database = db

# Define the User model
class User(BaseModel):
    email = CharField(unique=True)
    password = CharField()
    username = CharField(unique=True)
    admin = BooleanField(default=False)

# Define the MissingPerson model
class MissingPerson(BaseModel):
    name = CharField()
    birthday = DateField()
    bi = CharField()
    family_contact = CharField()
    image_path = CharField()
    date = DateTimeField(default=datetime.datetime.now)
    solved = BooleanField(default=False)
    def to_dict(self):
        return {
            'ID': self.id,
            'Nome': self.name,
            'Data de Nascimento': format_date(self.birthday, locale="PT"),
            'BI': self.bi,
            'Contacto da Familia': self.family_contact,
            'Data de Desaparecimento': format_date(self.date, locale="PT"),
            'Resolvido': bool(self.solved),
            'image_path': self.image_path,
        }

# Define the Found model
class Found(BaseModel):
    missing_person = ForeignKeyField(MissingPerson, backref='found_records')
    date = DateTimeField(default=datetime.datetime.now)
    location = CharField()
    camera = CharField()
    def to_dict(self):
        return {
            'ID': self.id,
            'Data da Aparição': format_date(self.date, locale="PT"),
            'Localização': self.location,
            'Camera': self.camera,
            'Desaparecido': self.missing_person.to_dict()
        }

def create_tables():
   with db:
      db.create_tables([User, MissingPerson, Found]) 