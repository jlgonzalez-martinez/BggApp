from unittest.mock import patch, MagicMock

import pytest
from sqlalchemy.orm import Session

from boardgame.adapters.repositories import (
    BoardgameSqlAlchemyRepository,
    CategorySqlAlchemyRepository,
    FamilySqlAlchemyRepository,
    MechanicSqlAlchemyRepository,
)
from boardgame.services.unit_of_work import SqlAlchemyUnitOfWork


@patch("boardgame.services.unit_of_work.create_engine")
@patch("boardgame.services.unit_of_work.sessionmaker")
class TestSqlAlchemyUnitOfWork:
    @pytest.fixture
    def session(self):
        return MagicMock(spec=Session)

    @pytest.mark.unit
    def test_commit(self, mock_sessionmaker, mock_create_engine, session):
        mock_sessionmaker.return_value = MagicMock(return_value=session)
        mock_create_engine.return_value = MagicMock()
        uow = SqlAlchemyUnitOfWork()
        with uow:
            uow.commit()

        session.commit.assert_called_once()
        session.close.assert_called_once()
        assert isinstance(uow.boardgames, BoardgameSqlAlchemyRepository)
        assert isinstance(uow.categories, CategorySqlAlchemyRepository)
        assert isinstance(uow.families, FamilySqlAlchemyRepository)
        assert isinstance(uow.mechanics, MechanicSqlAlchemyRepository)

    @pytest.mark.unit
    def test_rollback(self, mock_sessionmaker, mock_create_engine, session):
        mock_sessionmaker.return_value = MagicMock(return_value=session)
        mock_create_engine.return_value = MagicMock()
        uow = SqlAlchemyUnitOfWork()
        with uow:
            uow.rollback()

        session.close.assert_called_once()
        assert session.rollback.called
        assert isinstance(uow.boardgames, BoardgameSqlAlchemyRepository)
        assert isinstance(uow.categories, CategorySqlAlchemyRepository)
        assert isinstance(uow.families, FamilySqlAlchemyRepository)
        assert isinstance(uow.mechanics, MechanicSqlAlchemyRepository)

    @pytest.mark.unit
    def test_collect_new_events(self, mock_sessionmaker, mock_create_engine, session):
        mock_sessionmaker.return_value = MagicMock(return_value=session)
        mock_create_engine.return_value = MagicMock()
        uow = SqlAlchemyUnitOfWork()
        boardgame_events = ["event_1", "event_2"]
        category_events = ["event_3", "event_4"]
        family_events = ["event_5"]
        mechanic_events = ["event_6"]

        with uow:
            uow.boardgames.seen = [MagicMock(events=list(boardgame_events))]
            uow.categories.seen = [MagicMock(events=list(category_events))]
            uow.families.seen = [MagicMock(events=list(family_events))]
            uow.mechanics.seen = [MagicMock(events=list(mechanic_events))]
            events = list(uow.collect_new_events())

        assert len(events) == 6
        assert (
            events
            == boardgame_events + category_events + family_events + mechanic_events
        )
