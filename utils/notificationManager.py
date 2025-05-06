# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.



import asyncio
from logging import Logger
from typing import Callable, List, Union

import discord

from common.config import NOTIF_HOUR, SCRUTINS_FOLDER, MIN_DATE_CURRENT_MOTION
from handlers.deputeHandler import vote_by_ref_handler
from utils.databaseManager import DatabaseManager
from utils.scrutinManager import Scrutin
from utils.utils import compute_time_for_notifications, read_files_from_directory


async def notification_task(logger: Logger, event: asyncio.Event, database: DatabaseManager, getter: Callable[[int], Union[discord.User, None]]):
    """Task that sends notifications to users after updates, later in the day."""
    logger.info("Starting notification task")

    while True:
        # Wait for the update to complete
        logger.info("Waiting for daily update to complete...")
        await event.wait()

        logger.info("Update completed, scheduling notifications...")

        # Calculate time to wait before sending notifications
        target_time, seconds_until_target = compute_time_for_notifications(NOTIF_HOUR)

        logger.info("Notifications planed at %s in %.2f seconds.",
                    target_time, seconds_until_target)
        if seconds_until_target > 0:
            await asyncio.sleep(seconds_until_target)

        logger.info("Sending notifications")
        # Send notifications to users
        await send_notifications(database, getter)


async def send_notifications(database: DatabaseManager, getter: Callable[[int], Union[discord.User, None]]):

    last_scrutin_date = MIN_DATE_CURRENT_MOTION
    scrutins: List[Scrutin] = []
    for data in read_files_from_directory(SCRUTINS_FOLDER):
        scrutin = Scrutin.from_json(data)
        if scrutin.dateScrutin > last_scrutin_date:
            last_scrutin_date = scrutin.dateScrutin
            scrutins = [scrutin]
        elif scrutin.dateScrutin == last_scrutin_date:
            scrutins.append(scrutin)

    user_ids: List[str] = await database.get_users()

    if not user_ids:
        return

    for user_id in user_ids:
        user = getter(int(user_id))
        ref_notifs: List[str] = await database.get_notifications(user)
        if not ref_notifs: # TODO check, abnormal behaviour
            continue

        for ref in ref_notifs:
            embeds: List[discord.Embed] = vote_by_ref_handler(scrutins, ref)
            for embed in embeds:
                await user.send(embed=embed)
