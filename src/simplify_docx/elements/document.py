"""
The body element
"""
from typing import Dict, Any, Optional, Iterator
from .base import container

class document(container):
    """
    A document body element
    """
    __type__ = "CT_Document"


class CT_Rel(container):
    """
    A document body element
    """

    __type__ = "CT_Rel"
    __name__ = "CT_Rel"

    def to_json(
        self, doc, options: Dict[str, str] = None, super_iter: Optional[Iterator] = None
    ) -> Dict[str, Any]:
        """
        Coerce a container object to JSON
        """
        chunkId = self.fragment.rId
        chunkPart = doc.part.related_parts[chunkId]
        chunkDoc = chunkPart.element
        chunkDoc.element.body.getchildren()

        return {
            "TYPE": self.__name__,
            "VALUE": document(chunkPart.element.element).to_json(chunkDoc, options),
        }


class subDoc(CT_Rel):
    """
    A nested sub-document
    """

    __name__ = "subDoc"


class contentPart(CT_Rel):
    """
    A content part
    """

    __name__ = "contentPart"


class altChunk(CT_Rel):
    """
    An alternate format chunk
    """

    __type__ = "CT_AltChunk"
