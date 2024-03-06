import json

import click

from utils import printGreen


def exportPostmanCollection(export: bool = False) -> None:
    from config.app import createApp
    from config.settings import ConfigName
    from urls.api import api, router

    app = createApp(ConfigName.POSTMAN)
    app.register_blueprint(router)

    with app.app_context():
        data = api.as_postman(urlvars=False, swagger=True)

    if export:
        with open("postmanCollection.json", "w") as f:
            f.write(json.dumps(data))
            print()
            printGreen("Postman collection exported to 'postmanCollection.json'")
            print()
        return
    print()
    print(json.dumps(data))
    print()


@click.command(name="postman")
@click.option("--export", type=click.BOOL, default=False, help="Export Postman collection")
def postman(export: bool) -> None:
    """
    Generate the Postman collection for the application.

    Args:\n
        export (bool): A flag indicating whether to export the Postman collection.

    Usage:\n
        (printed collection): poetry run flask postman\n
        (exported collection to json): poetry run flask postman --export=True
    """
    exportPostmanCollection(export)
