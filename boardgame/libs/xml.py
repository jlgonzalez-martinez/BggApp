"""Xml utils module."""
from typing import List, Dict, Any, Tuple

from xml.etree.ElementTree import Element


def xml_sub_element_attr(
    elem: Element,
    sub_elem: str,
    filter_attr: str = None,
    filter_value: str = None,
    default: Any = None,
):
    """
    Search for a sub-element filter by attribute.
    For the following XML document:
    .. code-block:: xml
        <xml_elem>
            <sub_element filter="this" value="THIS" />
        </xml_elem>
    a call to ``xml_sub_element_attr(xml_elem, "sub_element", "filter", "this")``
    would return ``"THIS"``
    Args:
        elem: Search the children nodes of this element
        sub_elem: Name of the sub-element
        filter_attr: Name of the sub-element attribute
        filter_value: Value of the attribute
        default: default value if the sub_element or attribute is not found
    Returns:
        Value of the attribute or ``None`` in error cases
    """
    value = default
    if filter_attr and filter_value:
        expr = f'.//{sub_elem}[@{filter_attr}="{filter_value}"]'
        elems = elem.findall(expr)
    else:
        elems = [elem.find(sub_elem)]
    for sub_element in elems:
        if sub_element.attrib.get("value"):
            value = sub_element.attrib.get("value")
    return value


def xml_sub_element_attr_list(
    elem: Element, sub_elem: str, attribute: str = "value"
) -> List[Dict[str, Any]]:
    """
    Get a list of all elements under the sub element tag.
    This would return a list of dicts including the tag id and the value
    specified in the value kwarg.
    Args:
        elem: Search the children nodes of this element
        sub_elem: Name of the sub-element to search for
        attribute: Name of the attribute to get
    Returns:
        List of dictionaries including the id and the value.
    """
    results = []
    if elem and sub_elem:
        sub_elements = elem.findall(sub_elem)
        results = [
            dict(id=int(el.attrib.get("id")), value=el.attrib.get(attribute))
            for el in sub_elements
        ]
    return results


def xml_sub_element_text(elem: Element, sub_elem: str, default=None) -> str:
    """
    Get the text of the specified sub_element.
    For the document below:
    .. code-block:: xml
        <xml_elem>
            <sub_element>text</sub_element>
        </xml_elem>
    ``"text"`` will be returned
    Args:
        elem: search the children nodes of this element
        sub_elem: name of the sub_element whose text will be retrieved
        default: default value if sub_element is not found
    Returns:
        The text associated with the sub-element or ``None`` in case of error
    """
    text = default
    sub_element = elem.find(sub_elem)
    if sub_element is not None and sub_element.text:
        text = sub_element.text
    return text


def parse_xml_poll(elem: Element, poll_name: str) -> Tuple[int, Any]:
    """
    Parse a xml poll element.
    Args:
        elem: Xml root element.
        poll_name: Poll name to search.
    Returns:
        Tuple indicating the total votes and the xml pool element.
    """
    total_votes = 0
    poll = elem.find("poll[@name='" + poll_name + "']")
    if poll:
        total_votes = int(poll.attrib.get("totalvotes", 0))
    return total_votes, poll


def fix_unsigned_negative(value: int):
    """
    Bgg API return negative years casted to unsigned ints (32 bit).
    This function fixes this error.
    Args:
        value: Input year value.
    Returns:
        Fixed year now positive.
    """
    if value > 0x7FFFFFFF:
        value -= 0x100000000
    return value
