from django.db import models
from django.contrib.auth.models import AbstractUser

from uuid import uuid4


def generate_uuid():
    return str(uuid4())


class User(AbstractUser):
    pass
    # create_user(email = email, name = name, phone = phone, password = password)


class Room(models.Model):
    uuid = models.CharField(max_length=32, db_index=True, default=generate_uuid)
    name = models.CharField(max_length=50, unique=True)
    participant_count = models.PositiveIntegerField(default=0)
    message_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    uuid = models.CharField(max_length=32, db_index=True, default=generate_uuid)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)


