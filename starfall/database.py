import logging
import typing

import aiosqlite

import starfall.models

logger = logging.getLogger(__name__)


class Widget:
    async def get_list(
            self,
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

    async def get_from_id(
            self,
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

    async def create(
            self,
            db: aiosqlite.Connection,
            data: starfall.models.Widget
    ) -> starfall.models.Widget:
        cursor = await db.execute(
            "INSERT INTO `widgets` (`name`, `number`)"
            "VALUES (:name, :number)",
            {"name": data.name, "number": data.number},
        )
        await db.commit()

        return await self.get_from_id(db, cursor.lastrowid)

    async def update(
            self,
            db: aiosqlite.Connection,
            data: starfall.models.Widget
    ) -> starfall.models.Widget:
        await db.execute(
            "UPDATE `widgets` "
            "SET `name` = :name, `number` = :number "
            "WHERE id = :id",
            {"name": data.name, "number": data.number, "id": data.id}
        )
        await db.commit()

        return await self.get_from_id(db, data.id)

    async def delete(
            self,
            db: aiosqlite.Connection,
            id: int
    ) -> None:
        await db.execute(
            "DELETE FROM `widgets` WHERE id = :id",
            {"id": id}
        )
        await db.commit()
