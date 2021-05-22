# -*- coding: utf-8 -*-
import sys
import click

from tech.mlsql.plugin.tool.commands.builder import PluginBuilder
from tech.mlsql.plugin.tool.commands.compile_process import Spark311, Spark243


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
    required=True,
    type=str,
    help="module name")
@click.option(
    "--spark",
    required=False,
    type=str,
    help="spark version")
def build(mvn: str, module_name: str, spark: str):
    builder = PluginBuilder(mvn, module_name, spark)
    builder.build()


@cli.command()
def spark311():
    builder = Spark311()
    builder.pom_convert()
    builder.source_convert()


@cli.command()
def spark243():
    builder = Spark243()
    builder.pom_convert()
    builder.source_convert()


def main():
    return cli()


if __name__ == "__main__":
    main()
