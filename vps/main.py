#!/usr/bin/env python3

import asyncio
import click
import logging
import socket
import ssl

from aiohttp import web, web_request
from typing import Union

from vps import __version__


HOSTNAME = socket.gethostname()
HTTPS_URL = f"https://{HOSTNAME}/"
LOG = logging.getLogger(__file__)


def _handle_debug(
    ctx: click.core.Context,
    param: Union[click.core.Option, click.core.Parameter],
    debug: Union[bool, int, str],
) -> Union[bool, int, str]:
    """Turn on debugging if asked otherwise INFO default"""
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        format=("[%(asctime)s] %(levelname)s: %(message)s (%(filename)s:%(lineno)d)"),
        level=log_level,
    )
    return debug


async def hello(request: web_request.BaseRequest) -> web.Response:
    print(f"Request = {request}")  # COOPER
    print(dir(request))  # COOPER
    print(vars(request))  # COOPER
    try:
        return web.Response(text=f"Hello from {HOSTNAME}")
    except ssl.SSLError as ssle:
        LOG.error(f"{request} had an SSL Error: {ssle}")


# TODO: Add support for request's endpoint once webserver has some
async def https_redirect(request: web_request.BaseRequest) -> None:
    raise web.HTTPFound(HTTPS_URL)


async def async_main(
    debug: bool, http_port: int, https_port: int, ssl_cert: str, ssl_key: str
) -> None:
    loop = asyncio.get_event_loop()

    http = web.Server(https_redirect)
    http_sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    http_sock.bind(("::", http_port))

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(ssl_cert, ssl_key)

    https = web.Server(hello)
    https_sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    https_sock.bind(("::", https_port))

    try:
        http_server = await loop.create_server(http, sock=http_sock)
        LOG.info(f"HTTP listenening on [::]:{http_port} ...")

        https_server = await loop.create_server(https, sock=https_sock, ssl=ssl_context)
        LOG.info(f"HTTPS listenening on [::]:{https_port} ...")

        await asyncio.gather(http_server.wait_closed(), https_server.wait_closed())
    except asyncio.CancelledError:
        LOG.info(f"Wait closing servers ...")
        http_server.close()
        https_server.close()
        await asyncio.gather(http_server.wait_closed(), https_server.wait_closed())


@click.command()
@click.option(
    "--debug",
    is_flag=True,
    callback=_handle_debug,
    show_default=True,
    help="Turn on debug logging",
)
@click.option(
    "-p", "--http-port", default=6968, show_default=True, help="HTTP TCP Port"
)
@click.option(
    "-P", "--https-port", default=6969, show_default=True, help="HTTPS TCP Port"
)
@click.option(
    "-s",
    "--ssl-cert",
    type=click.Path(exists=True),
    default=f"/etc/letsencrypt/live/{HOSTNAME}/fullchain.pem",
    show_default=True,
    help="Path to ssl crt file",
)
@click.option(
    "-S",
    "--ssl-key",
    type=click.Path(exists=True),
    default=f"/etc/letsencrypt/live/{HOSTNAME}/privkey.pem",
    show_default=True,
    help="Path to ssl key file",
)
@click.version_option(version=__version__, prog_name="vps")
@click.pass_context
def main(ctx: click.Context, **kwargs) -> None:
    loop = asyncio.get_event_loop()
    try:
        async_main_task = loop.create_task(async_main(**kwargs))
        loop.run_until_complete(async_main_task)
    except KeyboardInterrupt:
        LOG.debug("Canceling async_main")
        async_main_task.cancel()
        loop.run_until_complete(async_main_task)
    finally:
        loop.close()


if __name__ == "__main__":
    main()
