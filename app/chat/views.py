from django.db.models.query import QuerySet
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import PermissionDenied

from .models import Thread, Message
from .serializers import MessageSerializer, ThreadSerializerList, ThreadSerializerRetrieve, ThreadSerializerCreate


class ThreadViewSet(viewsets.ModelViewSet):
    '''
    A ViewSet for Thread model
    '''
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self) -> QuerySet[Thread]:
        '''
        Get a list of all user's threads
        '''

        return Thread.objects.filter(participants=self.request.user)

    def get_serializer_class(self) -> (ThreadSerializerList | ThreadSerializerCreate
                                        | ThreadSerializerRetrieve | None):
        if self.action == 'list':
            return ThreadSerializerList
        elif self.action == 'create':
            return ThreadSerializerCreate
        elif self.action == 'retrieve':
            return ThreadSerializerRetrieve
        else:
            return None

    @action(detail=True, methods=['get'], url_path='messages')
    def get_messages(self, request, pk=None) -> Response:
        '''
        A custom endpoint to get list of all messages from all chats
        '''
        thread = self.get_object()

        if request.user not in thread.participants.all():
            return PermissionDenied({"detail": "Access denied."})

        messages = thread.messages.order_by('created')
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data)



class MessageViewSet(viewsets.ModelViewSet):
    '''
    A ViewSet for Message model
    '''
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 100
    pagination_class.max_limit = 250

    def get_queryset(self) -> QuerySet[Message]:
        '''
        Get a list of all messages in threads where
        a user is a participant
        '''
        return Message.objects.filter(thread__participants=self.request.user)

    @action(detail=False, methods=['get'], url_path='unread')
    def get_unread_messages(self, request) -> Response:
        '''
        Retrieve a list of all unread messages
        in all user's threads
        '''
        queryset = self.get_queryset().filter(is_read=False)
        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='mark-as-read')
    def mark_as_read_message(self, request, pk=None) -> Response:
        '''
        A custom endpoint to mark messages as "read"
        '''
        message = self.get_object()

        message_is_read = {'is_read': True}

        serializer = self.get_serializer(message, data=message_is_read, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

