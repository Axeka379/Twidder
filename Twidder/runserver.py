from gevent.wsgi import WSGIServer
from Twidder import app
from geventwebsocket.handler import WebSocketHandler

http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
http_server.serve_forever()
