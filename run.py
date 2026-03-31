import webbrowser
import os
from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        webbrowser.open('http://127.0.0.1:5050')
    socketio.run(app, debug=True, host='127.0.0.1', port=5050)
