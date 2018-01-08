#!/usr/bin/env python3

import click
import logging

from aiohttp import web
from typing import Any, Union


LOG = logging.getLogger(__file__)


async def hello(request: Any) -> web.Response:
    return web.Response(text="Hello, world")


def _handle_debug(ctx, param, debug) -> Union[bool, int, str]:
    '''Turn on debugging if asked otherwise INFO default'''
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        format=(
            '[%(asctime)s] %(levelname)s: %(message)s ' +
            '(%(filename)s:%(lineno)d)'
        ),
        level=log_level
    )
    return debug


@click.command()
@click.option(
    '-p', '--port', default=80, help='TCP port to listen on for HTTP',
)
@click.pass_context
def main(
    ctx: click.Context,
    port: int,
) -> None:
    LOG.info
    app = web.Application()
    app.router.add_get('/', hello)
    web.run_app(app, port=port)


if __name__ == '__main__':
    main()
