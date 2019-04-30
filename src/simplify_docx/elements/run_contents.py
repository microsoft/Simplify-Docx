# -- coding: utf-8 --
"""
Run level elements
"""
import re
from typing import Dict, Any, Iterator, Optional
from docx.oxml.ns import qn
from ..types import xmlFragment
from . import el  # , IncompatibleTypeError

RE_SPACES = re.compile("  +", re.IGNORECASE)


class empty(el):
    """
    Generic for CT_Empty elements
    """

    __type__: str

    def __init__(self, x: xmlFragment):
        super(empty, self).__init__(x)
        self.__type__ = x.tag.split("}")[-1]

    def to_json(
        self, doc, options: Dict[str, str], super_iter: Optional[Iterator] = None
    ) -> Dict[str, Any]:  # pylint: disable=unused-argument
        """
        coerce an object to JSON
        """
        if options.get("empty-as-text", False):
            return {"TYPE": "CT_Text", "VALUE": "[w:%s]" % self.__type__}

        return {"TYPE": "CT_Empty", "VALUE": "[w:%s]" % self.__type__}


# settings to be imported at a later time
default_text_options = {
    "simplify_text": True,
    "simplify_symbol": True,
    "simplify_empty": True,
}


class text(el):
    """
    A Text element
    """

    __type__: str
    value: str

    def __init__(self, x: xmlFragment):
        super(text, self).__init__(x)
        self.__type__ = x.tag.split("}")[-1]
        if x.text is None:
            self.value = ""
        else:
            self.value = x.text

    def to_json(
        self, doc, options: Dict[str, str], super_iter: Optional[Iterator] = None
    ) -> Dict[str, Any]:  # pylint: disable=unused-argument
        """
        coerce an object to JSON
        """

        _value = self.value
        if options.get("dumb-quotes", True):
            _value = (
                _value.replace(u"\u2018", "'")
                .replace(u"\u2019", "'")
                .replace(u"\u201a", "'")
                .replace(u"\u201b", "'")
            )
            _value = _value.replace(u"\u201c", '"').replace(u"\u201d", '"')

        if options.get("dumb-hyphens", True):
            _value = (
                _value.replace(u"\u2000", "-")
                .replace(u"\u2001", "-")
                .replace(u"\u2002", "-")
                .replace(u"\u2003", "-")
                .replace(u"\u2004", "-")
                .replace(u"\u2005", "-")
                .replace(u"\u2006", "-")
                .replace(u"\u2007", "-")
                .replace(u"\u2008", "-")
                .replace(u"\u2009", "-")
                .replace(u"\u200A", "-")
                .replace(u"\u201B", "-")
            )

        if options.get("dumb-spaces", True):
            _value = (
                _value.replace(u"\u2010", "-")
                .replace(u"\u2011", "-")
                .replace(u"\u2012", "-")
                .replace(u"\u2013", "-")
                .replace(u"\u2014", "-")
                .replace(u"\u2015", "-")
                .replace(u"\u00A0", "-")
            )

        if options.get("ignore-joiners", True):
            _value = _value.replace(u"\u200C", "").replace(u"\u200D", "")

        if options.get("flatten-inner-spaces", True):
            _value = RE_SPACES(" ", _value)

        if options.get("ignore-left-to-right-mark", False):
            _value = _value.replace(u"\u200E", "")

        if options.get("ignore-right-to-left-mark", False):
            _value = _value.replace(u"\u200F", "")

        return {"TYPE": "CT_Text", "VALUE": _value}


class SymbolChar(el):
    """ The SymbolChar element. Even though this is basically a test element,
    it's an element in which the font is significant.
    """

    __type__ = "SymbolChar"
    char: str
    font: str

    def __init__(self, x):
        super(SymbolChar, self).__init__(x)
        self.char = x.get(qn("w:char"))
        self.font = x.get(qn("w:font"))

    def to_json(
        self, doc, options: Dict[str, str], super_iter: Optional[Iterator] = None
    ) -> Dict[str, Any]:  # pylint: disable=unused-argument
        """
        coerce an object to JSON
        """
        if options.get("symbol-as-text", True):
            return {"TYPE": "CT_Text", "VALUE": self.char}

        return {"TYPE": self.__type__, "VALUE": {"char": self.char, "font": self.font}}


simpleTextElementText = {
    "CarriageReturn": "\r",
    "Break": "\r",
    "TabChar": "\t",
    "PositionalTab": "\t",
    "NoBreakHyphen": "-",
    "SoftHyphen": "-",
}


tagToTypeMap: Dict[str, str] = {
    qn("w:br"): "Break",
    qn("w:cr"): "CarriageReturn",
    qn("w:tab"): "TabChar",
    qn("w:noBreakHyphen"): "NoBreakHyphen",
    qn("w:softHyphen"): "SoftHyphen",
    qn("w:ptab"): "PositionalTab",
}


class simpleTextElement(el):
    """
    A simple text element represented by a CT_Empty
    """

    def __init__(self, x: xmlFragment):
        super(simpleTextElement, self).__init__(x)
        self.__type__ = tagToTypeMap[x.tag]

    def to_json(self, doc, options=None, super_iter: Optional[Iterator] = None):

        if options.get("special-characters-as-text", True):
            return {"TYPE": "CT_Text", "VALUE": simpleTextElementText[self.__type__]}

        return {"TYPE": self.__type__}
