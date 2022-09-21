import logging
from typing import TYPE_CHECKING

from boardgame.adapters import orm
from boardgame.adapters.clients.xml_bgg_client import XmlBggClient
from boardgame.domain.commands import LoadBoardgame
from boardgame.domain.events import BoardgameCreated
from boardgame.services.loader_service import LoaderService
from boardgame.services.messagebus import MessageBus
from boardgame.services.unit_of_work import SqlAlchemyUnitOfWork

if TYPE_CHECKING:
    from logging import Logger
    from boardgame.services.unit_of_work import AbstractUnitOfWork
    from boardgame.adapters.clients.abstract_bgg_client import AbstractBggClient


def bootstrap(
    bgg_client: "AbstractBggClient" = XmlBggClient.build(),
    start_orm: bool = True,
    uow: "AbstractUnitOfWork" = SqlAlchemyUnitOfWork(),
    logger: "Logger" = logging.getLogger(__name__),
) -> MessageBus:
    if start_orm:
        orm.start_mappers()
        orm.metadata.create_all(uow.engine)

    injected_event_handlers = {BoardgameCreated: [lambda e: logger.info(e)]}
    injected_command_handlers = {LoadBoardgame: LoaderService(logger, bgg_client, uow)}
    return MessageBus(uow, injected_event_handlers, injected_command_handlers)
