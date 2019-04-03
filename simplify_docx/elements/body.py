"""
The body element
"""
from typing import Dict, Any, Optional, Iterator
from more_itertools import peekable
from .base import container


class body(container):
    """
    A document body element
    """

    __type__ = "CT_Body"

    def to_json(
        self, doc, options: Dict[str, str] = None, super_iter: Optional[Iterator] = None
    ) -> Dict[str, Any]:
        """
        Coerce a container object to JSON
        """
        contents = []
        iter_me = peekable(self)
        for elt in iter_me:
            JSON = elt.to_json(doc, options, iter_me)

            if (
                JSON["TYPE"] == "CT_P"
                and options.get("ignore-empty-paragraphs", False)
                and not JSON["VALUE"]
            ):
                continue

            contents.append(JSON)

        out: Dict[str, Any] = {"TYPE": self.__type__, "VALUE": contents}
        return out
