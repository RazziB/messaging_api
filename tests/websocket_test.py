import logging
import gevent

from flask import Flask, jsonify, after_this_request, request
from flask_socketio import SocketIO, send, emit
from werkzeug.wrappers import cors, response


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins=True)
app.logger.setLevel('INFO')


@socketio.on('message')
def asd(msg):

    emit('asd123', f'RECEIVED asdasd{msg}', to=request.sid)
    emit('asd123', '2nd emit is it sent? ', to=request.sid)

if __name__ == '__main__':
    socketio.run(app, port=3005)
