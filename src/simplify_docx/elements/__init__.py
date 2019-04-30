"""
Docx element objects
"""
# from .blocks import smartTag, customXml, fldSimple, hyperlink, paragraph_list, paragraph
from .base import el, container, IncompatibleTypeError

from .body import body
from .document import document, altChunk, subDoc, contentPart
from .table import table, tr, tc
from .run_contents import text, simpleTextElement, SymbolChar, empty
from .form import fldChar, checkBox, ddList, textInput, ffData
from .paragraph import  (
        EG_PContent,
        paragraph,
        hyperlink,
        fldSimple,
        customXml,
        smartTag,
)
