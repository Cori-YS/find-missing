from database.models import User, MissingPerson, Found, db

# Create functions
def create_user(email, password, username, admin=False):
    if db.is_closed():
        db.connect()
    user = User.create(email=email, password=password, username=username, admin=admin)
    db.close()
    return user

def create_missing_person(name, birthday, bi, family_contact, date, image_path):
    if db.is_closed():
        db.connect()
    person = MissingPerson.create(
        name=name,
        birthday=birthday,
        family_contact=family_contact,
        image_path=image_path,
        date=date,
        bi=bi,
    )
    db.close()
    return person

def create_found(missing_person, location, camera):
    if db.is_closed():
        db.connect()
    found = Found.create(
        missing_person=missing_person,
        location=location,
        camera=camera
    )
    db.close()
    return found

# Update functions
def update_user(user_id, email=None, password=None, username=None, admin=None):
    if db.is_closed():
        db.connect()
    user = User.get(User.id == user_id)
    if email is not None:
        user.email = email
    if password is not None:
        user.password = password
    if username is not None:
        user.username = username
    if admin is not None:
        user.admin = admin
    user.save()
    db.close()
    return user

def update_missing_person(person_id, name=None, birthday=None, family_contact=None, image_path=None, date=None, solved=None):
    if db.is_closed():
        db.connect()
    person = MissingPerson.get(MissingPerson.id == person_id)
    if name is not None:
        person.name = name
    if birthday is not None:
        person.birthday = birthday
    if family_contact is not None:
        person.family_contact = family_contact
    if image_path is not None:
        person.image_path = image_path
    if date is not None:
        person.date = date
    if solved is not None:
        person.solved = solved
    person.save()
    db.close()
    return person

def update_found(found_id, missing_person=None, date=None, location=None, camera=None):
    if db.is_closed():
        db.connect()
    found = Found.get(Found.id == found_id)
    if missing_person is not None:
        found.missing_person = missing_person
    if date is not None:
        found.date = date
    if location is not None:
        found.location = location
    if camera is not None:
        found.camera = camera
    found.save()
    db.close()
    return found

# Delete functions
def delete_user(user_id):
    if db.is_closed():
        db.connect()
    user = User.get(User.id == user_id)
    user.delete_instance()
    db.close()

def delete_missing_person(person_id):
    if db.is_closed():
        db.connect()
    person = MissingPerson.get(MissingPerson.id == person_id)
    person.delete_instance()
    db.close()

def delete_found(found_id):
    if db.is_closed():
        db.connect()
    found = Found.get(Found.id == found_id)
    found.delete_instance()
    db.close()

# List and get functions
def list_users(page=1, page_size=10):
    if db.is_closed():
        db.connect()
    users = User.select().paginate(page, page_size)
    count = User.select().count()
    db.close()
    return {"users": list(users), "count": count}

def get_user_by_id(user_id):
    if db.is_closed():
        db.connect()
    user = User.get(User.id == user_id)
    db.close()
    return user

def get_user_by_username(username):
    if db.is_closed():
        db.connect()
    user = User.get(User.username == username)
    db.close()
    return user

def list_missing_persons(search=None, page=1, page_size=5):
    if db.is_closed():
        db.connect()
    if search:
        persons = MissingPerson.select().where((MissingPerson.bi == search) & (MissingPerson.solved == False)).order_by(MissingPerson.id.desc()).paginate(page, page_size)
        count = MissingPerson.select().where((MissingPerson.bi == search) & (MissingPerson.solved == False)).count()
    else:
        persons = MissingPerson.select().where(MissingPerson.solved == False).order_by(MissingPerson.id.desc()).paginate(page, page_size)
        count = MissingPerson.select().where(MissingPerson.solved == False).count()
    db.close()
    return {"persons": list(persons), "count": count}

def get_missing_person_by_id(person_id):
    if db.is_closed():
        db.connect()
    person = MissingPerson.get(MissingPerson.id == person_id)
    db.close()
    return person

def get_missing_person_by_bi(person_bi):
    if db.is_closed():
        db.connect()
    person = MissingPerson.get(MissingPerson.bi == person_bi)
    db.close()
    return person

def list_founds(search=None, page=1, page_size=5):
    if db.is_closed():
        db.connect()
    if search:
        founds = Found.select().join(MissingPerson, on=(Found.missing_person == MissingPerson.id)).where((MissingPerson.bi == search) & (MissingPerson.solved == False)).order_by(Found.date.desc()).paginate(page, page_size)
        count = Found.select().join(MissingPerson, on=(Found.missing_person == MissingPerson.id)).where((Found.missing_person == search) & (MissingPerson.solved == False)).count()
    else:
        founds = Found.select().join(MissingPerson, on=(Found.missing_person == MissingPerson.id)).where(MissingPerson.solved == False).order_by(Found.date.desc()).paginate(page, page_size)
        count = Found.select().join(MissingPerson, on=(Found.missing_person == MissingPerson.id)).where(MissingPerson.solved == False).count()
    db.close()
    return {"founds": list(founds), "count": count}

def get_found_by_bi(bi):
    if db.is_closed():
        db.connect()
    found = Found.get(Found.missing_person.bi == bi)
    db.close()
    return found
