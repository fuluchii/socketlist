from geventwebsocket.handler import WebSocketHandler
from gunicorn.workers.ggevent import GeventPyWSGIWorker
class GeventWorker(GeventPyWSGIWorker):
    wsgi_handler = WebSocketHandler
