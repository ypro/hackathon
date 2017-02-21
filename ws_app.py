import tornado.httpserver
import tornado.websocket
import tornado.ioloop
from tornado.ioloop import PeriodicCallback
import tornado.web

PORT=8888

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.callback = PeriodicCallback(self.send_hello, 5000)
        self.callback.start()
        print "Opened Connection"

    def send_hello(self):
        self.write_message('hello')

    def send_echo(self, message):
        self.write_message(message)

    def on_message(self, message):
        self.send_echo(message)
        pass

    def on_close(self):
        self.callback.stop()
        print "Closed Connection"


class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
		

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/websocket', WebSocketHandler)
        ]
 
        settings = {
            'template_path': ''
        }
        tornado.web.Application.__init__(self, handlers, **settings)
 
 
if __name__ == '__main__':
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
