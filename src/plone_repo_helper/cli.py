from plone_repo_helper import _types as t
from plone_repo_helper.commands.plone import app as app_plone
from plone_repo_helper.commands.release import app as app_release
from plone_repo_helper.commands.version import app as app_version
from plone_repo_helper.settings import get_settings

import typer


app = typer.Typer(no_args_is_help=True)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Welcome to Plone Distribution Helper."""
    try:
        settings = get_settings()
    except RuntimeError:
        typer.echo("Not running inside a mono repo.")
        raise typer.Exit() from None
    else:
        ctx_obj = t.CTLContextObject(settings=settings)
        ctx.obj = ctx_obj
        ctx.ensure_object(t.CTLContextObject)


app.add_typer(
    app_release, name="release", no_args_is_help=True, help="Release mono repo packages"
)
app.add_typer(
    app_plone,
    name="plone",
    no_args_is_help=True,
    help="Handle Products.CMFPlone dependency",
)
app.add_typer(app_version)


def cli():
    app()


__all__ = ["cli"]
