import logging
import os
from messaging_api import app, socketio
PORT = int(os.environ.get('APP_PORT', 3004))
logger = logging.getLogger()
logger.setLevel(level=logging.DEBUG)
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3004, log_output=True)

