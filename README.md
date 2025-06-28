# isi_test_task

This is a test task project "**Simple chat**". The task requirements were provided in a PDF file so I do not double them here.


## Endpoints
The endpoints are provided with predefined localhost URLs to meet the docker image configuration.

### Get a token

This is needed to generate an auth token to be able to interact as a user with the system.
```
GET http://localhost:8000/chat-api/token/
```
Example of payload:
```
{
    "username": "user3",
    "password": "1234"
}
```
**All further requests must have the "Authorization" header with the user token from this endpoint for proper work.**

### Create a thread

Create a thread with a specific user. There could be no more than 2 participants in one thread (usually you and someone else).
In case the thread already exists, the system will return this thread ID instead of creating a duplicate.
```
POST http://localhost:8000/chat-api/threads/
```
Example of payload:
```
{
    "participant": 2
}
```

The "participant" key represents a target user ID.

### Delete a thread

Delete the created thread related to the authorized user.
```
DELETE http://localhost:8000/chat-api/threads/7b0befd9-89b3-4e00-a03e-f6698e4f82cd/
```
Example of payload:
```
Empty
```
"`7b0befd9-89b3-4e00-a03e-f6698e4f82cd`" - a target thread ID.

### Retrieve the list of threads for any user
This endpoint returns a list of all existing threads where a specific user is a participant.

```
GET http://localhost:8000/chat-api/threads/
```
Example of payload:
```
Empty
```

### Create a message
Create a message for a specific thread.

```
POST http://localhost:8000/chat-api/messages/
```
Example of payload:
```
{
    "thread": "3cff18f1-d049-43f3-9c69-fcc8948f66f6",
    "text": "New message in the thread!"
}
```

### Retrieve message list for the thread
This endpoint returns a list of messages in a specific thread.
```
GET http://localhost:8000/chat-api/threads/3cff18f1-d049-43f3-9c69-fcc8948f66f6/messages/
```
Example of payload:
```
Empty
```
"`3cff18f1-d049-43f3-9c69-fcc8948f66f6`" - a target thread ID.

### Mark message as read
A custom endpoint to mark messages as "read". It will update the "is_read" field in the Message table in the database and set it to "True".
```
PATCH http://localhost:8000/chat-api/messages/539/mark-as-read/
```
Example of payload:
```
Empty
```
"`539`" - a target message ID.

### Retrieve a number of unread messages for the user
A custom endpoint provides a list of all unread messages of a specific user.
The endpoint supports LimitOffsetPagination. The default page limit is 100.
```
GET http://localhost:8000/chat-api/messages/unread/
```
With pagination:
```
http://localhost:8000/chat-api/messages/unread/?limit=10&offset=10
```
Example of payload:
```
Empty
```

### Additonal endpoints

* Get information about a thread
```
GET http://localhost:8000/chat-api/threads/3cff18f1-d049-43f3-9c69-fcc8948f66f6/
```

* Get information about a message
```
GET http://localhost:8000/chat-api/messages/551/
```

* Delete a message
```
DELETE http://localhost:8000/chat-api/messages/551/
```


## Instruction
The repository includes a Dockerfile with proper instructions to run the app. **This instruction is designed for the Linux environment**.
Thus to start the app you need to perform a few simple steps:

1. Clone this repository

For this purpose, there is a big green button "Code" on the top of the page. Feel free to use any option as you like.
For the instruction, I`ll provide a command for downloading via HTTPS:
```
git clone https://github.com/vl-ch/isi_test_task.git /tmp/isi_test_task/
```
I specified a download path to make you easily follow the instructions.
However, you can download the repository to any directory.

2. Go to the downloaded repository directory

It may be your custom path, but the instruction requires consistency:
```
cd /tmp/isi_test_task/
```

3. Build a docker image

At this moment, you should be in the repository directory. Directly from this location execute the following command:
```
docker build -t test-task-app:latest .
```
Now wait a bit while docker finishes the build process.

4. Start the app

Finally, the Docker image has been built, and we are ready to launch:
```
docker run --name test-task-container -p 8000:8000 test-task-app:latest
```
You also could use `-d` key to launch the process on background:
```
docker run -d --name test-task-container -p 8000:8000 test-task-app:latest
```