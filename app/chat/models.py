import uuid
from django.db import models
from django.conf import settings

class Thread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='threads')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.id)


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField(max_length=250)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    is_read = models.BooleanField(default=False)
