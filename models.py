from mongoengine import *


class User(Document):
    user_id = StringField()


class Item(EmbeddedDocument):
    name = StringField()


class Room(Document):
    name = StringField()
    owner = ReferenceField(User, dbref=False)


class Location(Document):
    name = StringField()
    items = EmbeddedDocumentListField(Item)
    room = ReferenceField(Room, dbref=False)
