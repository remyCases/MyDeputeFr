# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from typing import List, Union
import aiosqlite


class DatabaseManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def add_notification(self, user_id: int, server_id: int, depute_ref: str) -> bool:
        """
        This function will add a notification.
        """

        rows = await self.connection.execute(
            "SELECT id FROM notification WHERE user_id=? AND server_id=? AND depute_ref=?",
            (
                user_id,
                server_id,
                depute_ref,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            if result:
                return False

            await self.connection.execute(
                "INSERT INTO notification(id, user_id, server_id, depute_ref) VALUES (?, ?, ?, ?)",
                (
                    1,
                    user_id,
                    server_id,
                    depute_ref,
                ),
            )
            await self.connection.commit()

            return True


    async def remove_notifications(self, user_id: int, server_id: int, depute_ref: Union[str, None] = None) -> None:
        """
        This function will remove all notifications stored for a user.

        :param user_id: The ID of the user.
        :param server_id: The ID of the server.
        """

        if depute_ref:
            await self.connection.execute(
                "DELETE FROM notification WHERE user_id=? AND server_id=? AND depute_ref=?",
                (
                    user_id,
                    server_id,
                    depute_ref
                ),
            )
        else:
            await self.connection.execute(
                "DELETE FROM notification WHERE user_id=? AND server_id=?",
                (
                    user_id,
                    server_id,
                ),
            )
        await self.connection.commit()

    async def get_notifications(self, user_id: int, server_id: int) -> List[str]:
        """
        This function will get all the notifications of a user.
        """
        rows = await self.connection.execute(
            "SELECT depute_ref FROM notification WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row[0])
            return result_list
