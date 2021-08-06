import tornado.web
import json
from http import HTTPStatus


class BaseHandler(tornado.web.RequestHandler):
    def get_db(self):
        return self.application.settings["database"]

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')
        self.set_header("Access-Control-Allow-Origin", "*")

    def data_received(self, chunk=None):
        if self.request.body:
            return json.loads(self.request.body)

    def write_response(self, status_code, result=None, message=None):
        self.set_status(status_code)
        if result:
            self.finish(json.dumps(result))
        elif message:
            self.finish(json.dumps({
                "message": message
            }))
        elif status_code:
            self.set_status(status_code)
            self.finish()

    def validation_error(self, ex):
        self.write_response(
            status_code=HTTPStatus.BAD_REQUEST,
            message=" ".join(
                ["Invalid Request Payload:", ex.message]
            )
        )
