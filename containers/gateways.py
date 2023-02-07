from dependency_injector import containers, providers
from pymongo import MongoClient


class Gateways(containers.DeclarativeContainer):

    config = providers.Configuration(strict=True)

    database_client = providers.Singleton(MongoClient, config.database.uri)
