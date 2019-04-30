"""
Abstract classes for typing purposes only
"""
# pylint: disable=no-self-use,pointless-statement,missing-docstring,invalid-name, too-few-public-methods
from __future__ import annotations
from typing import Optional, Dict, Sequence

class xmlFragment:
    """an abstract class representing the xml fragments returned by python-docx
    """
    tag: str
    prefix: Optional[str]
    attrib: Dict[str, str]
    nsmap: Dict[str, str]
    text: Optional[str]
    tail: Optional[str]
    def getchildren(self) -> Sequence[xmlFragment]:
        ...
    def getparent(self) -> Optional[xmlFragment]:
        ...
    def getnext(self) -> Optional[xmlFragment]:
        ...
    def xpath(self, x:str) -> Optional[xmlFragment]: # pylint: disable=unused-argument
        ...


class ct_altchunk(xmlFragment):
    rId: str

class ct_p(xmlFragment):
    ...

class ct_numpr(xmlFragment):
    ...


# BASIC TYPES

class ct_onoff:
    val: bool

class ct_string(xmlFragment):
    val: str

class ct_decimalnumber(xmlFragment):
    val: float

# TEXT TYPES

class ct_br(xmlFragment):
    type: Optional[str]
    clear: Optional[str]

class ct_pPr(xmlFragment):
    numpr: Optional[ct_numpr]

class ct_rPr(xmlFragment):
    vanish: Optional[ct_onoff]
    webHidden: Optional[ct_onoff]

class ct_r(xmlFragment):
    rPr: Optional[ct_rPr]

class ct_num(xmlFragment):
    abstractNumId: xmlFragment #  = OneAndOnlyOne('w: abstractNumId')
    # lvlOverride = ZeroOrMore('w: lvlOverride')
    numId: float #  = RequiredAttribute('w: numId', ST_DecimalNumber)


# tables

class ct_cell(xmlFragment):
    ...

class ct_row(xmlFragment):
    # tblPrEx = Optional[ct_tblPrEx]
    tc: Optional[Sequence[ct_cell]]

class ct_tbl(xmlFragment):
    tblPr: xmlFragment
    tr: Optional[Sequence[ct_row]]


# parts

class part():
    element: xmlFragment

class documentPart():
    element: ct_document # pylint: disable=used-before-assignment
    related_parts: Dict[str, part]

class altchunkpart():
    element: documentPart

class ct_sectionPr(xmlFragment):
    ...

class ct_body(xmlFragment):
    sectPr: Optional[ct_sectionPr]

class ct_document(xmlFragment):
    body: ct_body
    part: documentPart
