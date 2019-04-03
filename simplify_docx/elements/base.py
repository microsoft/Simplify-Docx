"""
base classes for the docx elements
"""
from typing import Optional, Dict, Any, Sequence, Generator, Iterator
from docx.oxml.shared import CT_String, CT_OnOff, CT_DecimalNumber
from docx.shared import  Twips
from ..types import xmlFragment

# --------------------------------------------------
# Base Classes
# --------------------------------------------------

class IncompatibleTypeError(Exception):
    """
    Incompatible types
    """

class el:
    """
    Abstract base class for docx element
    """
    __type__: str
    parent: "el"
    fragment: xmlFragment
    __iter_name__: Optional[str] = None
    __iter_xpath__: Optional[str] = None
    __props__: Optional[Sequence[str]]
    props: Dict[str, Any]

    def __init__(self, x: xmlFragment):
        self.fragment = x
        __props__ = getattr(self, "__props__", None)
        if __props__:
            self.props = {}
            for prop in __props__:
                self.props[prop] = getattr(x, prop)

    def to_json(self,
            doc, # pylint: disable=unused-argument
            options: Dict[str, str],# pylint: disable=unused-argument
            super_iter: Optional[Iterator] = None) -> Dict[str, Any]:# pylint: disable=unused-argument
        """
        coerce an object to JSON
        """

        out = {"TYPE": self.__type__}

        if hasattr(self, "__props__"):
            for key, prop in self.props.items():
                if prop is None:
                    continue
                out[key] = get_val(prop)
            #return dict(self.props, **out)
        return out

    def __iter__(self) -> Generator['el', None, None]:
        from ..iterators import xml_iter
        node: xmlFragment = (self.fragment
                             if self.__iter_xpath__ is None
                             else self.fragment.xpath(self.__iter_xpath__))
        for elt in xml_iter(node,
                            self.__iter_name__ if self.__iter_name__ else self.__type__):
            yield elt

    def simplify(self, options: Dict[str, str]) -> 'el': # pylint: disable=unused-argument
        """
        Join the next element to the current one
        """
        return self

    def append(self, x: 'el') -> None: # pylint: disable=no-self-use
        """
        Join the next element to the current one
        """
        raise IncompatibleTypeError


def get_val(x):
    """
    Extract the value from a simple property
    """
    if isinstance(x, (str,bool)):
        return x
    if isinstance(x, list):
        return [get_val(elt) for elt in x]
    if isinstance(x, (CT_String, CT_OnOff, CT_DecimalNumber)):
        return x.val
    if isinstance(x, (Twips)):
        return x.twips
    raise RuntimeError("Unexpected value type '%s'" % x.__class__.__name__)

class container(el):
    """
    Represents an object that can contain other objects
    """

    def to_json(self,
            doc,
            options: Dict[str, str],
            super_iter: Optional[Iterator] = None) -> Dict[str, Any]:
        """Coerce a container object to JSON
        """
        out: Dict[str, Any] = super(container, self,).to_json(doc, options, super_iter)
        out.update({
                "TYPE": self.__type__,
                "VALUE": [ elt.to_json(doc, options) for elt in self],
                })
        return out
