import starfall.models
import starfall.database
import aiosqlite
import json

from starfall.handlers.base import BaseHandler
from jsonschema import validate
from jsonschema import ValidationError
from http import HTTPStatus


class WidgetsHandler(BaseHandler):
    #####
    # API Method Functions
    #####
    async def get(self, key) -> None:
        if not key:
            await self.get_record_list()
        else:
            await self.get_single_record(key=key)

    async def post(self, key):
        if key:
            self.write_response(status_code=HTTPStatus.NOT_FOUND)
        else:
            await self.create_record()

    async def put(self, key):
        if not key:
            self.write_response(status_code=HTTPStatus.NOT_FOUND)
        else:
            await self.update_record(key=key)

    async def delete(self, key):
        if not key:
            self.write_response(status_code=HTTPStatus.NOT_FOUND)
        else:
            await self.delete_record(key)

    #####
    # Supporting Functions. Could be refactored to another file
    #####
    async def get_single_record(self, key):
        async with aiosqlite.connect(self.get_db()) as db:
            row = await starfall.database.get_widget(db, id=key)
            self.set_default_headers()
            self.write(
                json.dumps(
                    starfall.models.widget_to_json(row)
                )
            )

    async def get_record_list(self):
        async with aiosqlite.connect(self.get_db()) as db:
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

    async def create_record(self):
        try:
            json_data = self.data_received()
            validate(instance=json_data, schema=starfall.models.WIDGET_SCHEMA)

            widget = starfall.models.Widget(
                name=json_data["name"],
                number=json_data["number"]
            )

            async with aiosqlite.connect(self.get_db()) as db:
                row = await starfall.database.create_widget(db, data=widget)
                self.set_default_headers()
                self.write(
                    json.dumps(
                        starfall.models.widget_to_json(row)
                    )
                )

        except ValidationError as ex:
            self.validation_error(ex)

    async def update_record(self, key):
        try:
            json_data = self.data_received()
            validate(
                instance=json_data,
                schema=starfall.models.WIDGET_SCHEMA
            )
            validate(
                instance=json_data,
                schema=starfall.models.WIDGET_SCHEMA_POST
            )

            if json_data["id"] != int(key):
                self.write_response(
                    status_code=HTTPStatus.BAD_REQUEST,
                    message="Key must match ID"
                )
            else:
                widget = starfall.models.Widget(
                    id=json_data["id"],
                    name=json_data["name"],
                    number=json_data["number"]
                )

                async with aiosqlite.connect(self.get_db()) as db:
                    row = await starfall.database.update_widget(
                        db,
                        data=widget
                    )
                    self.set_default_headers()
                    self.write(
                        json.dumps(
                            starfall.models.widget_to_json(row)
                        )
                    )
        except ValidationError as ex:
            self.validation_error(ex)

    async def delete_record(self, key):
        async with aiosqlite.connect(self.get_db()) as db:
            await starfall.database.delete_widget(db, id=key)
            self.set_default_headers()
            self.write_response(status_code=HTTPStatus.NO_CONTENT)
