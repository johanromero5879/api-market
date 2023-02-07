from dependency_injector import containers, providers

from containers import Gateways, Repositories, Services


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(strict=True)

    # Make injection on API Routes and middlewares functions
    wiring_config = containers.WiringConfiguration(
        packages=[
            "app.auth",
            "app.user",
            "app.product",
            "app.purchase"
        ]
    )

    gateways = providers.Container(Gateways, config=config.gateways)
    repositories = providers.Container(Repositories, gateways=gateways)

    services = providers.Container(
        Services,
        config=config.services,
        repositories=repositories,
        gateways=gateways
    )
