"""XML utils unit test module."""
from xml.etree import ElementTree

import pytest as pytest

from boardgame.libs.xml import (
    xml_sub_element_attr,
    xml_sub_element_text,
    parse_xml_poll,
)


class TestXml:
    """XML utils unit test class."""

    @pytest.fixture(scope="class")
    def root(self):
        """Create a root element."""
        return "root"

    @pytest.fixture(scope="class")
    def element(self):
        """Create an element."""
        return "element"

    @pytest.fixture(scope="class")
    def sub_element(self):
        """Create a sub-element."""
        return "sub_element"

    @pytest.fixture(scope="class")
    def text(self):
        """Create a test text."""
        return "test"

    @pytest.fixture(scope="class")
    def filter_value(self):
        """Create a test filter."""
        return "filter"

    @pytest.fixture(scope="class")
    def filter_name(self):
        """Create a test filter name."""
        return "filter_name"

    @pytest.fixture(scope="class")
    def value(self):
        """Create a test value."""
        return "value"

    @pytest.fixture(scope="class")
    def default_value(self):
        """Create a default value."""
        return "default"

    @pytest.fixture(scope="class")
    def unknown_name(self):
        """Create a default value."""
        return "default"

    @pytest.fixture(scope="class")
    def poll_name(self):
        """Create a test poll name."""
        return "poll_name"

    @pytest.fixture(scope="class")
    def total_votes(self):
        """Create a test total votes."""
        return 5

    @pytest.fixture(scope="class")
    def poll_element(self):
        """Create a test poll element."""
        return "poll"

    @pytest.fixture(scope="class")
    def poll_attributes(self, poll_name, total_votes):
        """Create a test poll element."""
        return f'name="{poll_name}" totalvotes="{total_votes}"'

    @pytest.fixture(scope="class")
    def xml_string(self, element, sub_element, filter_name, filter_value, value, text):
        """Create a test xml string"""
        return f'<{element}><{sub_element} {filter_name}="{filter_value}" value="{value}">{text}</{sub_element}></{element}>'

    @pytest.fixture(scope="class")
    def xml(self, xml_string):
        """Create a test xml."""
        return ElementTree.fromstring(xml_string)

    @pytest.fixture(scope="class")
    def xml_poll(self, root, poll_element, poll_attributes, xml_string):
        """Create a test xml"""
        return ElementTree.fromstring(
            f"<{root}><{poll_element} {poll_attributes}>{xml_string}</{poll_element}></{root}>"
        )

    @pytest.mark.unit
    def test_xml_sub_element_attr(
        self, xml, sub_element, filter_name, filter_value, value
    ):
        """Test normal behaviour of sub element attribute."""
        result = xml_sub_element_attr(
            xml, sub_element, filter_attr=filter_name, filter_value=filter_value
        )
        assert result == value

    @pytest.mark.unit
    def test_xml_sub_element_attr_default_value_with_no_results(
        self, xml, unknown_name, filter_name, filter_value, default_value
    ):
        """Test that if the sub element it's not present returns the default value."""
        result = xml_sub_element_attr(
            xml,
            unknown_name,
            filter_attr=filter_name,
            filter_value=filter_value,
            default=default_value,
        )
        assert result == default_value

    @pytest.mark.unit
    def test_xml_sub_element_attr_without_filters(self, xml, sub_element, value):
        """Test that if no filters provided return the first element."""
        result = xml_sub_element_attr(xml, sub_element)
        assert result == value

    @pytest.mark.unit
    def test_xml_sub_element_text(self, xml, sub_element, text):
        """Test normal behaviour of sub element text."""
        result = xml_sub_element_text(xml, sub_element)
        assert result == text

    @pytest.mark.unit
    def test_xml_sub_element_text_default_value_with_no_results(
        self, xml, unknown_name, default_value
    ):
        """Test that if the sub element it's not present returns the default value."""
        result = xml_sub_element_text(xml, unknown_name, default=default_value)
        assert result == default_value

    @pytest.mark.unit
    def test_parse_xml_poll(self, xml_poll, poll_element, poll_name, total_votes):
        """Test that parse xml poll return the total votes and the poll xml element."""
        votes, poll = parse_xml_poll(xml_poll, poll_name)
        assert votes == total_votes
        assert poll_element == poll.tag

    @pytest.mark.unit
    def test_parse_xml_poll_with_an_non_existing_poll(self, xml_poll, unknown_name):
        """Test that parse xml poll with non-existing pool returns empty result."""
        votes, poll = parse_xml_poll(xml_poll, unknown_name)
        assert 0 == votes
        assert poll is None
