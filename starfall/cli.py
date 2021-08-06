import logging

import click
import tornado.ioloop
import tornado.web

import starfall.database
import starfall.server


@click.group()
@click.option(
    "--database",
    envvar="STARFALL_DATABASE",
    type=click.Path(dir_okay=False),
    required=True,
)
@click.option(
    "--log-level",
    type=click.Choice(
        ["debug", "info", "warn", "error"],
        case_sensitive=False,
    ),
    default="warn",
)
@click.pass_context
def main(ctx, database, log_level):
    logging.basicConfig(
        level={
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warn": logging.WARN,
            "error": logging.ERROR,
        }.get(log_level.lower())
    )
    ctx.ensure_object(dict)
    ctx.obj["database"] = database


@main.command()
@click.option("--port", type=int, envvar="STARFALL_PORT", default=8888)
@click.option("--scheme", envvar="STARFALL_SCHEME")
@click.option("--debug", is_flag=True)
@click.pass_context
def server(ctx, port, scheme, debug):
    app = starfall.server.make_app(
        {
            **ctx.obj,
            "scheme": scheme,
            "debug": debug,
        }
    )
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
