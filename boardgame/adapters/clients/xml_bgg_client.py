from typing import Optional, List
from xml.etree import ElementTree

from boardgame.adapters.clients.abstract_bgg_client import AbstractBggClient
from boardgame.adapters.clients.dto import (
    BoardgameDto,
    ExpansionDto,
    PlayerDto,
    LanguageDependenceDto,
)
from boardgame.libs.xml import (
    xml_sub_element_attr_list,
    parse_xml_poll,
    xml_sub_element_attr,
    xml_sub_element_text,
    fix_unsigned_negative,
)


class XmlBggClient(AbstractBggClient):
    """Bgg xml client."""

    def get(self, bgg_id: int) -> Optional["BoardgameDto"]:
        response = self.fetch(bgg_id)
        boardgame_xml = ElementTree.fromstring(response.text).find("item")
        bgg_id = (
            int(boardgame_xml.attrib["id"])
            if boardgame_xml and hasattr(boardgame_xml, "attrib")
            else None
        )
        self.logger.info(f"Trying to load boardgame with bgg id {bgg_id}")
        if bgg_id:
            categories = xml_sub_element_attr_list(
                boardgame_xml, "link[@type='boardgamecategory']"
            )
            mechanics = xml_sub_element_attr_list(
                boardgame_xml, "link[@type='boardgamemechanic']"
            )
            families = xml_sub_element_attr_list(
                boardgame_xml, "link[@type='boardgamefamily']"
            )
            statistic = boardgame_xml.find("statistics/ratings")
            return BoardgameDto(
                bgg_id=bgg_id,
                name=xml_sub_element_attr(
                    boardgame_xml, "name", filter_attr="type", filter_value="primary"
                ),
                description=xml_sub_element_text(boardgame_xml, "description"),
                year_published=fix_unsigned_negative(
                    int(xml_sub_element_attr(boardgame_xml, "yearpublished", default=0))
                ),
                min_players=int(
                    xml_sub_element_attr(boardgame_xml, "minplayers", default=0)
                ),
                max_players=int(
                    xml_sub_element_attr(boardgame_xml, "maxplayers", default=0)
                ),
                playing_time=int(
                    xml_sub_element_attr(boardgame_xml, "playingtime", default=0)
                ),
                min_play_time=int(
                    xml_sub_element_attr(boardgame_xml, "minplaytime", default=0)
                ),
                max_play_time=int(
                    xml_sub_element_attr(boardgame_xml, "maxplaytime", default=0)
                ),
                min_age=int(xml_sub_element_attr(boardgame_xml, "minage", default=0)),
                image_url=xml_sub_element_text(boardgame_xml, "image"),
                std_dev=float(xml_sub_element_attr(statistic, "stddev")),
                median=float(xml_sub_element_attr(statistic, "median")),
                owned=int(xml_sub_element_attr(statistic, "owned")),
                trading=int(xml_sub_element_attr(statistic, "trading")),
                wanting=int(xml_sub_element_attr(statistic, "wanting")),
                wishing=int(xml_sub_element_attr(statistic, "wishing")),
                weight_average=float(xml_sub_element_attr(statistic, "averageweight")),
                rating_average=float(xml_sub_element_attr(statistic, "average")),
                bayes_average=float(xml_sub_element_attr(statistic, "bayesaverage")),
                num_rates=int(xml_sub_element_attr(statistic, "usersrated")),
                num_comments=int(xml_sub_element_attr(statistic, "numcomments")),
                num_weights=int(xml_sub_element_attr(statistic, "numweights")),
                expansions=self.parse_expansions(boardgame_xml),
                language_dependence=self.parse_languange_dependence(boardgame_xml),
                categories=[category.get("value", None) for category in categories],
                families=[family.get("value", None) for family in families],
                mechanics=[mechanic.get("value", None) for mechanic in mechanics],
                players=self.parse_num_players(boardgame_xml),
            )

    @staticmethod
    def parse_expansions(boardgame_xml) -> List["ExpansionDto"]:
        expansions = xml_sub_element_attr_list(
            boardgame_xml, "link[@type='boardgameexpansion']"
        )
        return [
            ExpansionDto(bgg_id=ex.get("id"), name=ex.get("value", ""))
            for ex in expansions
        ]

    @staticmethod
    def parse_num_players(boardgame_xml) -> List["PlayerDto"]:
        _, players_results = parse_xml_poll(boardgame_xml, "suggested_numplayers")
        players_dto = []
        for xml_player in players_results:
            players_results = {
                res.attrib.get("value"): int(res.attrib.get("numvotes", 0))
                for res in xml_player.findall("result")
            }
            if "+" not in xml_player.attrib.get("numplayers"):
                player_dto = PlayerDto(
                    number=int(xml_player.attrib.get("numplayers")),
                    best=players_results.get("Best", 0),
                    recommended=players_results.get("Recommended", 0),
                    not_recommended=players_results.get("Not Recommended", 0),
                )
                players_dto.append(player_dto)
        return players_dto

    @staticmethod
    def parse_languange_dependence(boardgame_xml) -> Optional["LanguageDependenceDto"]:
        _, poll_results = parse_xml_poll(boardgame_xml, "language_dependence")
        if poll_results:
            xml_results = poll_results[0].findall("result")
            language_results = {
                res.attrib.get("level"): res.attrib.get("numvotes", 0)
                for res in xml_results
            }
            return LanguageDependenceDto(
                very_low=int(language_results.get("1", 0)),
                low=int(language_results.get("2", 0)),
                medium=int(language_results.get("3", 0)),
                high=int(language_results.get("4", 0)),
                very_high=int(language_results.get("5", 0)),
            )
