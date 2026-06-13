import os
from mongoengine import connect, Document, StringField, ListField, ReferenceField, CASCADE, BooleanField
from dotenv import load_dotenv

load_dotenv()

# Підключення через безпечний файл .env
MONGODB_URI = os.getenv("MONGODB_URI")
connect(host=MONGODB_URI)

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()
    meta = {'collection': 'authors'}

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, reverse_delete_rule=CASCADE, required=True)
    quote = StringField(required=True)
    meta = {'collection': 'quotes'}

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    phone = StringField(required=True)
    preferred_method = StringField(choices=['email', 'sms'], default='email')
    is_sent = BooleanField(default=False)
    meta = {'collection': 'contacts'}