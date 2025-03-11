from plone_repo_helper import _types as t

import typer


app = typer.Typer()


@app.command()
def version(ctx: typer.Context):
    """Report versions of all components of this repository."""
    settings: t.RepositorySettings = ctx.obj.settings
    typer.echo(f"{'-' * 50}\nVersions\n{'-' * 50}")
    typer.echo(f"Repository: {settings.version}")
    for title, package in (
        ("Backend", settings.backend),
        ("Frontend", settings.frontend),
    ):
        typer.echo(f"{package.name} ({title}): {package.version}")
