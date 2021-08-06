import datetime
import logging
import typing

import aiosqlite

import starfall.models

logger = logging.getLogger(__name__)


async def list_all_widgets(
        db: aiosqlite.Connection
) -> typing.List[starfall.models.Widget]:
    db.row_factory = aiosqlite.Row
    params = {}
    query = " ".join(
        [
            "SELECT `widgets`.* FROM `widgets`",
        ]
    )
    cursor = await db.execute(query, params)
    rows = await cursor.fetchall()
    return [
        starfall.models.Widget(
            id=row["id"],
            name=row["name"],
            number=row["number"],
            createdOn=row["createdOn"],
            updatedOn=row["updatedOn"]
        )
        for row in rows
    ]
