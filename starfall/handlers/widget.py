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

    def validation_error(self, ex):
        self.finish(json.dumps({
            'error': {
                'code': HTTPStatus.BAD_REQUEST,
                'message': " ".join(["Invalid Request Payload key '", str(ex.relative_path[0]), "':", ex.message])
            }
        }))

    async def get(self, key) -> None:
        if not key:
            async with aiosqlite.connect(self.application.settings["database"]) as db:
                results = await starfall.database.list_all_widgets(db)
                self.set_default_headers()
                self.write(
                    json.dumps(
                        [
                            {
                                "id": row.id,
                                "name": row.name,
                                "number": row.number,
                                "created_on": row.createdOn,
                                "updated_on": row.updatedOn,
                            }
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
                        {
                            "id": row.id,
                            "name": row.name,
                            "number": row.number,
                            "created_on": row.createdOn,
                            "updated_on": row.updatedOn,
                        }
                    )
                )

    async def post(self, args):
        try:
            data = self.data_received()
            schema = {
                "type": "object",
                "properties": {
                    "number": {"type": "integer", "minimum": 0},
                    "name": {"type": "string", "minLength": 1, "maxLength": 64},
                },
            }

            validate(instance=data, schema=schema)

            self.write('true')

        except ValidationError as ex:
            self.validation_error(ex)
