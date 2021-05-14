# -*- coding: utf-8 -*-
import sys
import click

from tech.mlsql.plugin.tool.commands.builder import PluginBuilder


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


@click.group()
@click.version_option()
def cli():
    pass


@cli.command()
@click.option(
    "--mvn",
    required=False,
    type=str,
    help="mvn command")
@click.option(
    "--module_name",
    required=False,
    type=str,
    help="module name")
def build(mvn: str, module_name: str):
    builder = PluginBuilder(mvn, module_name)
    builder.build()


def main():
    return cli()


if __name__ == "__main__":
    main()
