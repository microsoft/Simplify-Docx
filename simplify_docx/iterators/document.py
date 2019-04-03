"""
Iterate over Document and AltChunk (i.e. "things that can contain EG_BlockLevelElts")
"""
from docx.oxml.ns import qn
from ..elements import body
from .generic import register_iterator

register_iterator(
    "CT_Document",
    TAGS_TO_YIELD={qn("w:body"): body},
    TAGS_TO_IGNORE=[qn("w:docPartPr")],
)
