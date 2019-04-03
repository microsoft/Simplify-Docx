"""
Paragraph and EG_PContent iterators
"""
from docx.oxml.ns import qn
from .generic import register_iterator

# Paragraph
register_iterator("CT_P", TAGS_TO_IGNORE=[qn("w:pPr")], extends=["EG_PContent"])

# custom xml
register_iterator(
    "CT_CustomXmlRun", TAGS_TO_IGNORE=[qn("w:customXmlPr")], extends=["EG_PContent"]
)

# Hyperlink
register_iterator("CT_Hyperlink", extends=["EG_PContent"])

# simple field
register_iterator("CT_SimpleField", extends=["EG_PContent"])

# smart tag
register_iterator(
    "CT_SmartTagRun", TAGS_TO_IGNORE=[qn("w:smartTagPr")], extends=["EG_PContent"]
)
