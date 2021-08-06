import starfall.models
import starfall.database

import tornado.web
import aiosqlite
import json
import logging


class WidgetsHandler(tornado.web.RequestHandler):
    database: None

    async def get(self) -> None:
        async with aiosqlite.connect(self.application.settings["database"]) as db:
            results = await starfall.database.list_all_widgets(db)
            self.set_header("Content-Type", "application/json")
            self.set_header("Access-Control-Allow-Origin", "*")
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
