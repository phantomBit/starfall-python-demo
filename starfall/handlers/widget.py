import starfall.models
import starfall.database

import tornado.web
import aiosqlite
import json
import logging


class WidgetsHandler(tornado.web.RequestHandler):

    async def get(self, key) -> None:
        if not key:
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
        else:
            async with aiosqlite.connect(self.application.settings["database"]) as db:
                row = await starfall.database.get_widget(db, id=key)
                self.set_header("Content-Type", "application/json")
                self.set_header("Access-Control-Allow-Origin", "*")
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
