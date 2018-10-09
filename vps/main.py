#!/usr/bin/env python3

import asyncio
import click
import logging
import socket

from aiohttp import web, web_request
from typing import Union


HOSTNAME = socket.gethostname()
LOG = logging.getLogger(__file__)


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


async def hello(request: web_request.BaseRequest) -> web.Response:
    return web.Response(text=f"Hello from {HOSTNAME}")


async def async_main(
    debug: bool,
    port: int,
) -> None:
    loop = asyncio.get_event_loop()
    aiohttp_server = web.Server(hello)
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.bind(('::', port))
    try:
        http_server = await loop.create_server(aiohttp_server, sock=sock)
        LOG.info(f"Listenening on [::]:{port} ...")
        await http_server.wait_closed()
    except asyncio.CancelledError:
        LOG.info(f"Closing server on [::]:{port} ...")
        http_server.close()
        await http_server.wait_closed()


@click.command()
@click.option('--debug', is_flag=True, callback=_handle_debug,
              show_default=True, help='Turn on debug logging')
@click.option(
    '-p', '--port', default=6969, help='TCP port to listen on for HTTP',
)
@click.pass_context
def main(
    ctx: click.Context,
    debug: bool,
    port: int,
) -> None:
    loop = asyncio.get_event_loop()
    try:
        async_main_task = loop.create_task(async_main(debug, port))
        loop.run_until_complete(async_main_task)
    except KeyboardInterrupt:
        LOG.debug("Canceling async_main")
        async_main_task.cancel()
        loop.run_until_complete(async_main_task)
    finally:
        loop.close()


if __name__ == '__main__':
    main()
