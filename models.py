from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = PostgresqlDatabase('barhap', user='adminmatt', password='password')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    city = CharField()
    state = CharField()
    password = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, city, state, password, **kwargs):
        email = email.lower()
        try:
            cls.select().where(
                (cls.email==email)
            ).get()
        except cls.DoesNotExist:
            user = cls(username=username, email=email, city=city, state=state)
            user.password = generate_password_hash(password)
            user.save()
            return user
        else:
            raise Exception("user with that username/email already exists ya dingus!!")

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()