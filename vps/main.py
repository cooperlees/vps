#!/usr/bin/env python3

import asyncio
import click
import logging
import socket

from aiohttp import web
from typing import Any, Union


LOG = logging.getLogger(__file__)


async def hello(request: Any) -> web.Response:
    return web.Response(text="Hello, world")


def _handle_debug(
    ctx: click.core.Context,
    param: Union[click.core.Option, click.core.Parameter],
    debug: Union[bool, int, str],
) -> Union[bool, int, str]:
    '''Turn on debugging if asked otherwise INFO default'''
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        format=('[%(asctime)s] %(levelname)s: %(message)s ' +
                '(%(filename)s:%(lineno)d)'),
        level=log_level,
    )
    return debug


async def async_main(
    debug: bool,
    port: int,
) -> None:
    loop = asyncio.get_event_loop()
    server = web.Server(hello)
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.bind(('::', port))
    try:
        http_server = await loop.create_server(server, sock=sock)
        LOG.info(f"Listenening on [::]:{port} ...")
        await asyncio.sleep(2**64)  # COOPER - Fix to wait nicely on server
    finally:
        http_server.close()
        await http_server.wait_closed()


@click.command()
@click.option('--debug', is_flag=True, callback=_handle_debug,
              show_default=True, help='Turn on debug logging')
@click.option(
    '-p', '--port', default=80, help='TCP port to listen on for HTTP',
)
@click.pass_context
def main(
    ctx: click.Context,
    debug: bool,
    port: int,
) -> None:
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(async_main(debug, port))
    except KeyboardInterrupt:
        ...
    finally:
        loop.close()


if __name__ == '__main__':
    main()
