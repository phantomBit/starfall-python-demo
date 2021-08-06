import tornado.web

from starfall.handlers.widget import WidgetsHandler

def make_app(settings) -> tornado.web.Application:
    paths = [
        (r"/v1/widget/?(.*)?", WidgetsHandler),
    ]
    return tornado.web.Application(paths, **settings)
