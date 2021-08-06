import tornado.web


def make_app(settings) -> tornado.web.Application:
    paths = [

    ]
    return tornado.web.Application(paths, **settings)
