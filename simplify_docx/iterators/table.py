"""
Table and row iterators
"""

from docx.oxml.ns import qn
from .generic import register_iterator
from ..elements import tr, tc, empty

# TABLE ITERATOR
register_iterator(
    "CT_Tbl",
    TAGS_TO_IGNORE=[qn("w:tblPr"), qn("w:tblGrid")],
    extends=["EG_ContentRowContent"],
)

register_iterator(
    "EG_ContentRowContent",
    TAGS_TO_YIELD={qn("w:tr"): tr, qn("w:sdt"): empty},
    TAGS_TO_NEST={qn("w:customXml"): "EG_ContentRowContent"},
    TAGS_TO_IGNORE=[qn("w:customXmlPr")],
    extends=["EG_RangeMarkupElements"],
)


# ROW ITERATOR
register_iterator(
    "CT_Row",
    TAGS_TO_IGNORE=[qn("w:tblPrEx"), qn("w:trPr")],
    extends=["EG_ContentCellContent"],
)

register_iterator(
    "EG_ContentCellContent",
    TAGS_TO_YIELD={qn("w:tc"): tc, qn("w:sdt"): empty},
    TAGS_TO_NEST={qn("w:customXml"): "EG_ContentCellContent"},
    TAGS_TO_IGNORE=[
        # FORMATTING PROPERTIES
        qn("w:customXmlPr")
    ],
    extends=["EG_RunLevelElts"],
)

# CELL ITERATOR
register_iterator("CT_Tc", TAGS_TO_IGNORE=[qn("w:tcPr")], extends=["EG_BlockLevelElts"])
