from models import create_tables, User, MissingPerson, Found, db
from crud_operations import (
    create_user, create_missing_person, create_found,
    update_user, update_missing_person, update_found,
    delete_user, delete_missing_person, delete_found,
    list_users, get_user_by_id,
    list_missing_persons, get_missing_person_by_id,
    list_founds, get_found_by_id
)
import datetime

if db.is_closed():
    db.connect() 
create_tables()
db.close()

'''    
def query_records():
    if db.is_closed():
        db.connect()
    # Retrieve all users
    users = User.select()
    for user in users:
        print(f'User: {user.username}, Email: {user.email}, Admin: {user.admin}')

    # Retrieve all missing persons
    missing_persons = MissingPerson.select()
    for person in missing_persons:
        print(f'Missing Person: {person.name}, Birthday: {person.birthday}, Family Contact: {person.family_contact}, Date Missing: {person.date}')

    # Retrieve all found records
    found_records = Found.select()
    for record in found_records:
        print(f'Found Person: {record.missing_person.name}, Date: {record.date}, Location: {record.location}, Camera: {record.camera}')
    db.close()

if __name__ == '__main__':
    # Create tables
    create_tables()

    # Create records
    user = create_user('john@example.com', 'securepassword123', 'john_doe', True)
    missing_person = create_missing_person(
        name='Jane Doe',
        birthday=datetime.date(1990, 5, 21),
        family_contact='john_doe@example.com',
        image_path='/path/to/image.jpg',
        date=datetime.date(2024, 6, 10)
    )
    found_person = create_found(
        missing_person=missing_person,
        date=datetime.datetime(2024, 6, 15, 14, 30),
        location='Times Square',
        camera='Camera 1'
    )

    # Query records
    query_records()

    # List records with pagination
    print("\nList Users (Page 1):")
    users = list_users(page=1, page_size=2)
    for user in users:
        print(f'User: {user.username}, Email: {user.email}, Admin: {user.admin}')

    print("\nList Missing Persons (Page 1):")
    persons = list_missing_persons(page=1, page_size=2)
    for person in persons:
        print(f'Missing Person: {person.name}, Birthday: {person.birthday}, Family Contact: {person.family_contact}, Day Missing: {person.day_missing}')

    print("\nList Founds (Page 1):")
    founds = list_founds(page=1, page_size=2)
    for found in founds:
        print(f'Found Person: {found.missing_person.name}, Date: {found.date}, Location: {found.location}, Camera: {found.camera}')

    # Get specific records by ID
    user = get_user_by_id(user.id)
    print(f'\nSpecific User: {user.username}, Email: {user.email}, Admin: {user.admin}')

    person = get_missing_person_by_id(missing_person.id)
    print(f'Specific Missing Person: {person.name}, Birthday: {person.birthday}, Family Contact: {person.family_contact}, Day Missing: {person.day_missing}')

    found = get_found_by_id(found_person.id)
    print(f'Specific Found Person: {found.missing_person.name}, Date: {found.date}, Location: {found.location}, Camera: {found.camera}')

    # Update records
    update_user(user.id, email='john.doe@example.com')
    update_missing_person(missing_person.id, family_contact='new_contact@example.com')
    update_found(found_person.id, location='Central Park')

    # Query records again to see updates
    query_records()

    # Delete records
    delete_found(found_person.id)
    delete_missing_person(missing_person.id)
    delete_user(user.id)

    # Query records again to see deletions
    query_records()
'''