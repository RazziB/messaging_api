import logging

from messaging_api import app, socketio
logger = logging.getLogger()
logger.setLevel(level=logging.DEBUG)
if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=3004, log_output=True)

