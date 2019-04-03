"""
Iterate over containers (i.e. "things that can contain EG_BlockLevelElts")
"""
from docx.oxml.ns import qn
from .generic import register_iterator
from ..elements import paragraph, table, empty, altChunk


# RANGE MARKUP
register_iterator(
    "EG_RangeMarkupElements",
    TAGS_TO_IGNORE=[
        qn("w:bookmarkStart"),
        qn("w:bookmarkEnd"),
        qn("w:commentRangeStart"),
        qn("w:commentRangeEnd"),
        qn("w:moveToRangeStart"),
        qn("w:moveToRangeEnd"),
    ],
    TAGS_TO_WARN={
        qn("w:customXmlInsRangeStart"): "Ignoring Revision Tags",
        qn("w:customXmlInsRangeEnd"): "Ignoring Revision Tags",
        qn("w:customXmlDelRangeStart"): "Ignoring Revision Tags",
        qn("w:customXmlDelRangeEnd"): "Ignoring Revision Tags",
        qn("w:customXmlMoveFromRangeStart"): "Ignoring Revision Tags",
        qn("w:customXmlMoveFromRangeEnd"): "Ignoring Revision Tags",
        qn("w:customXmlMoveToRangeStart"): "Ignoring Revision Tags",
        qn("w:customXmlMoveToRangeEnd"): "Ignoring Revision Tags",
    },
    TAGS_TO_SKIP={qn("w:moveFromRangeStart"): ("id", qn("w:MoveFromRangeEnd"))},
)

# RUN LEVEL LEMENTS
register_iterator(
    "EG_RunLevelElts",
    TAGS_TO_YIELD={qn("m:oMathPara"): empty, qn("m:oMath"): empty},
    TAGS_TO_NEST={qn("w:ins"): "EG_RunLevelElts", qn("w:moveTo"): "EG_RunLevelElts"},
    TAGS_TO_IGNORE=[
        # INVISIBLE THINGS
        qn("w:proofErr"),
        qn("w:permStart"),
        qn("w:permEnd"),
        qn("w:del"),
        qn("w:moveFrom"),
        qn("w:commentRangeStart"),
        qn("w:commentRangeEnd"),
        # RANGE MARKER
        qn("w:moveToRangeStart"),
        qn("w:moveToRangeEnd"),
    ],
    extends=["EG_RangeMarkupElements"],
)

# BLOCK LEVEL ELEMENTS
register_iterator(
    "EG_BlockLevelElts",
    TAGS_TO_YIELD={
        qn("w:p"): paragraph,
        qn("w:tbl"): table,
        qn("w:sdt"): empty,
        qn("w:altChunk"): altChunk,
    },
    TAGS_TO_NEST={qn("w:customXml"): "EG_BlockLevelElts"},
    TAGS_TO_IGNORE=[qn("w:sectPr"), qn("w:tcPr"), qn("w:pPr")],
    extends=["EG_RunLevelElts"],
)

# BODY
register_iterator(
    "CT_Body", TAGS_TO_IGNORE=[qn("w:sectPr")], extends=["EG_BlockLevelElts"]
)
