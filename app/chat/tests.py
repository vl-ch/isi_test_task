import pytest
from uuid import UUID
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from django.contrib.auth.models import User


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def users():
    tester1 = User.objects.create_user(username="tester1", password="1234")
    tester2 = User.objects.create_user(username="tester2", password="1234")
    tester3 = User.objects.create_user(username="tester3", password="1234")
    tester4 = User.objects.create_user(username="tester4", password="1234")

    return [tester1, tester2, tester3, tester4]


class ModelsTestHelper:
    '''
    A helper class to contain generic operations used through all the tests
    '''
    client = APIClient()

    def _create_thread_item(self, initiator: User, participant: User):
        '''
        Create an instance of Thread model item
        '''
        data = {'participant': participant.id}

        url = reverse('thread-list')
        self.client.force_authenticate(user=initiator)
        response = self.client.post(url, data, format='json')

        return response

    def _create_message_item(self, user: User, thread_id: UUID, text: str):
        '''
        Create an instance of Message model item
        '''
        data = {
            'thread': thread_id,
            'text': text
        }

        url = reverse('message-list')
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')

        return response


@pytest.mark.django_db
class TestThreadViewSet(ModelsTestHelper):
    '''
    Test class for Thread model to cover all related requirements of the task
    '''
    def test_thread_create(self, users: list[User]):
        initiator = users[0]
        participant = users[1]

        response = self._create_thread_item( initiator, participant)

        assert response.status_code == 201

    def test_thread_create_duplicate(self, users: list[User]):
        initiator = users[0]
        participant = users[1]

        results = []

        for _ in range(2):
            response = self._create_thread_item(initiator, participant)
            results.append(response)

        assert results[0].data == results[1].data

    def test_thread_delete(self, api_client, users):
        initiator = users[0]
        participant = users[1]

        response = self._create_thread_item(initiator, participant)
        thread_id = response.data['id']

        url = reverse('thread-detail', args=[thread_id])
        api_client.force_authenticate(user=initiator)
        response = api_client.delete(url)

        assert response.status_code == 204

    def test_thread_get_list(self, api_client, users: list[User]):
        initiator = users[0]
        participants = users[1:]

        for participant in participants:
            self._create_thread_item(initiator, participant)

        api_client.force_authenticate(user=initiator)
        response = api_client.get('/chat-api/threads/')

        assert response.status_code == 200

    def test_thread_get_list_of_messages_in_thread(self, api_client, users: list[User]):
        initiator = users[0]
        participant = users[1]
        messages_count = 10

        response = self._create_thread_item(initiator, participant)
        thread_id = response.data['id']

        for counter in range(messages_count):
            text = f'This is the text for message {counter}'
            self._create_message_item(initiator, thread_id, text)

        url = reverse('thread-get-messages', args=[thread_id])
        api_client.force_authenticate(user=initiator)
        response = api_client.get(url)

        assert response.status_code == 200
        assert messages_count == len(response.data)



@pytest.mark.django_db
class TestMessageViewSet(ModelsTestHelper):
    '''
    Test class for Message model to cover all related requirements of the task
    '''
    @pytest.fixture(autouse=True)
    def setup(self, users: list[User]):
        self.users = users
        self.thread = self._create_thread_item(self.users[0], self.users[1])
        self.thread_id = self.thread.data['id']

    def test_message_create(self, users: list[User]):
        user = users[0]

        response = self._create_message_item(user, self.thread_id, 'New message!')

        assert response.status_code == 201

    def test_message_mark_as_read(self, api_client, users: list[User]):
        user = users[0]
        message = self._create_message_item(user, self.thread_id, 'New message!')
        message_id = message.data['id']

        url = reverse('message-mark-as-read-message', args=[message_id])
        api_client.force_authenticate(user=user)
        response = api_client.patch(url)

        assert response.status_code == 200
        assert response.data['is_read'] == True

    def test_message_get_all_unread(self, api_client, users: list[User]):
        user = users[0]
        messages_count = 20
        read_messages_count = 15
        unread_messages_count = messages_count - read_messages_count

        for counter in range(messages_count):
            text = f'This is the text for message {counter}'
            message = self._create_message_item(user, self.thread_id, text)

            if counter < read_messages_count:
                message_id = message.data['id']
                url = reverse('message-mark-as-read-message', args=[message_id])
                api_client.force_authenticate(user=user)
                api_client.patch(url)

        url = reverse('message-get-unread-messages')
        api_client.force_authenticate(user=user)
        response = api_client.get(url)
        response_messages_count = response.data['count']

        assert response.status_code == 200
        assert unread_messages_count == response_messages_count
