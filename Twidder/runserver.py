from gevent.wsgi import WSGIServer
from Twidder import app
from geventwebsocket.handler import WebSocketHandler

server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
server.serve_forever()
