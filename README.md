# messaging_api
A simple rest API backend system that is responsible for handling messages between users.
I went the extra mile and added a register / log out routes even though it wasn't requested in the task's description, I hope that's ok.
Furthermore, every route (except for /register) requires a logged in user.

stack:
Flask, Flask-SQLAlchemy, PostgreSQL, Python

The API has eight routes:

1. /register - Registed users, request body must provide:
                {
                  'username': ' '          # min length - 3 max length - 10
                  'password': ' '          # min length - 3 max length - 10
                 }
                 
2. /login - Log in existing users, must provide: same as register

3. /message - Send a message to an existing user. User must be logged in to send a message.
             request body must provide:
             {
                'receiver': ' '
                'message': ' '     # max length - 100
                'subject': ' '     # max length - 20
             }
             sender & date-time are automatically filled and sent.
             
4. /get_messages - Get all received and sent messages of a logged in user in the form of:
              {
                 sent_messages: [] 
                 received_messages: []
               }
               
5. /read_message - Get last unread message sent to the logged in user, and then turn 'read' property of that message to True.

6. /get_unread - Get all unread messages sent to the logged in user, in the format of a JSON - array (json)

7. /delete/<msg_id> - Delete a message using it's id property.

8. /logout - Logs out the logged in user.
