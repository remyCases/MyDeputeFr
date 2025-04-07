# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import asyncio
from logging import Logger
from config.config import TCP_SERVER_HOST, TCP_SERVER_PORT, TCP_TOKEN
from download.download import update

async def handle_client(log: Logger, reader, writer):
    """Handling client connections to TCP server"""
    data = await reader.readline()
    message = data.decode().strip()
    addr = writer.get_extra_info("peername")
    
    log.info(f"Connexion reçue de {addr}: {message}")
    
    if message == TCP_TOKEN:
        log.info("Token valide, démarrage de la mise à jour...")
        result = await update(log, update_acteur_organe=True)
        writer.write(f"{result}\n".encode())
    else:
        writer.write(b"Token invalide.\n")
    
    await writer.drain()
    writer.close()

async def start_update_server(log: Logger):
    server = await asyncio.start_server(
        lambda reader, writter: handle_client(log, reader, writter),
        TCP_SERVER_HOST,
        TCP_SERVER_PORT
    )
    
    addr = server.sockets[0].getsockname()
    log.info(f"Serveur de mise à jour démarré sur {addr}")
    
    async with server:
        await server.serve_forever()
