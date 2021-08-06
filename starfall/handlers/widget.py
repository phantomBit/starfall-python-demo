import starfall.models
import starfall.database

from http import HTTPStatus

import tornado.web
import aiosqlite
import json
import logging
from jsonschema import validate
from jsonschema import ValidationError


class WidgetsHandler(tornado.web.RequestHandler):
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
        self.write_response(status_code=HTTPStatus.BAD_REQUEST, message=" ".join(
            ["Invalid Request Payload:", ex.message]))

    async def get(self, key) -> None:
        if not key:
            async with aiosqlite.connect(self.application.settings["database"]) as db:
                results = await starfall.database.list_all_widgets(db)
                self.set_default_headers()
                self.write(
                    json.dumps(
                        [
                            starfall.models.widget_to_json(row)
                            for row in results
                        ]
                    )
                )
        else:
            async with aiosqlite.connect(self.application.settings["database"]) as db:
                row = await starfall.database.get_widget(db, id=key)
                self.set_default_headers()
                self.write(
                    json.dumps(
                        starfall.models.widget_to_json(row)
                    )
                )

    async def post(self, key):
        if key:
            self.write_response(status_code=HTTPStatus.NOT_FOUND)
        else:
            try:
                json_data = self.data_received()
                validate(instance=json_data, schema=starfall.models.WIDGET_SCHEMA)

                widget = starfall.models.Widget(
                    name=json_data["name"],
                    number=json_data["number"]
                )

                async with aiosqlite.connect(self.application.settings["database"]) as db:
                    row = await starfall.database.create_widget(db, widget)
                    self.set_default_headers()
                    self.write(
                        json.dumps(
                            starfall.models.widget_to_json(row)
                        )
                    )


            except ValidationError as ex:
                self.validation_error(ex)

    async def put(self, key):
        if not key:
            self.write_response(status_code=HTTPStatus.NOT_FOUND)
        else:
            try:
                json_data = self.data_received()
                validate(instance=json_data, schema=starfall.models.WIDGET_SCHEMA)
                validate(instance=json_data, schema=starfall.models.WIDGET_SCHEMA_POST)

                if json_data["id"] != int(key):
                    self.write_response(status_code=HTTPStatus.BAD_REQUEST, message="Key must match ID")
                else:
                    widget = starfall.models.Widget(
                        id=json_data["id"],
                        name=json_data["name"],
                        number=json_data["number"]
                    )

                    async with aiosqlite.connect(self.application.settings["database"]) as db:
                        row = await starfall.database.update_widget(db, widget)
                        self.set_default_headers()
                        self.write(
                            json.dumps(
                                starfall.models.widget_to_json(row)
                            )
                        )
            except ValidationError as ex:
                self.validation_error(ex)
