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


async def get_widget(
        db: aiosqlite.Connection,
        id: int = 0
) -> starfall.models.Widget:
    db.row_factory = aiosqlite.Row
    params = {}
    query = " ".join(
        [
            "SELECT `widgets`.* FROM `widgets`",
            f"WHERE id = {id}"
        ]
    )
    cursor = await db.execute(query, params)
    row = await cursor.fetchone()
    return starfall.models.Widget(
        id=row["id"],
        name=row["name"],
        number=row["number"],
        createdOn=row["createdOn"],
        updatedOn=row["updatedOn"]
    )


async def create_widget(
        db: aiosqlite.Connection,
        data: starfall.models.Widget
) -> starfall.models.Widget:
    cursor = await db.execute(
        "INSERT INTO `widgets` (`name`, `number`)"
        "VALUES (:name, :number)",
        {"name": data.name, "number": data.number},
    )
    await db.commit()

    return await get_widget(db, cursor.lastrowid)
