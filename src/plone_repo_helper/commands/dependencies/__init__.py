from .plone import app as app_plone

import typer


app = typer.Typer(no_args_is_help=True)

app.add_typer(
    app_plone,
    name="plone",
    no_args_is_help=True,
    help="Handle Products.CMFPlone dependency",
)
