import websockets
import asyncio

import socketio

# standard Python
sio = socketio.Client()


@sio.event
def message(data):
    print('data received: ' + data)


@sio.on('my message')
def on_message(data):
    print('I received a message!')


sio.connect('http://127.0.0.1:3005/')
sio.send('asdsadsad')
