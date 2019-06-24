import random
from model import db, Donor, Donation, User
from passlib.hash import pbkdf2_sha256

db.connect()

# This line will allow you "upgrade" an existing database by
# dropping all existing tables from it.
db.drop_tables([User, Donor, Donation])

db.create_tables([User, Donor, Donation])

alice = Donor(name="Alice")
alice.save()

bob = Donor(name="Bob")
bob.save()

charlie = Donor(name="Charlie")
charlie.save()

donors = [alice, bob, charlie]

for x in range(30):
    Donation(donor=random.choice(donors), value=random.randint(100, 10000)).save()

User(name="admin", password=pbkdf2_sha256.hash("password")).save()
User(name="bob", password=pbkdf2_sha256.hash("bobbob")).save()
