from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Thread, Message


class ThreadSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ('id', 'participants', )

class ThreadSerializerRetrieve(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'


class ThreadSerializerCreate(serializers.ModelSerializer):
    # A neccessary override to make satisfy the requirement:
    # "Thread can’t have more than 2 participants."
    # In this case the initiator user fetched from the token and the second participant
    # specified in this field
    participant = serializers.IntegerField(source='participants', write_only=True)
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Thread
        fields = ('id', 'participant', )

    def create(self, validated_data) -> Thread:
        '''
        Custom Thread instance creation on POST request

        Create a new thread or return an existing one with a particular user.
        '''
        initiator = self.context['request'].user
        participant_id = validated_data.get('participants')

        if participant_id <= 0:
            raise ValidationError({'detail': 'A participant ID must be a positive int'})

        participant = User.objects.get(pk=participant_id)

        thread = Thread.objects.filter(participants=initiator).filter(participants=participant).first()

        if not thread:
            thread = Thread.objects.create()
            thread.participants.add(initiator, participant)

        return thread


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'sender', 'thread', 'text', 'created', 'is_read', )
        read_only_fields = ('id', 'sender', )


    def create(self, validated_data) -> Message:
        '''
        Custom Message instance creation on POST request
        '''
        sender = self.context['request'].user
        message = Message.objects.create(sender=sender, **validated_data)

        return message