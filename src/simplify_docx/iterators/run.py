"""
Build the iterator for the run elements
"""
from docx.oxml.ns import qn
from .generic import register_iterator
from ..elements import text, simpleTextElement, SymbolChar, empty, contentPart, fldChar

register_iterator(
    "CT_R",
    TAGS_TO_YIELD={
        qn("w:t"): text,
        qn("w:sym"): SymbolChar,
        qn("w:br"): simpleTextElement,
        qn("w:cr"): simpleTextElement,
        qn("w:tab"): simpleTextElement,
        qn("w:noBreakHyphen"): simpleTextElement,
        qn("w:softHyphen"): simpleTextElement,
        qn("w:ptab"): simpleTextElement,
        qn("w:fldChar"): fldChar,
        qn("w:instrText"): empty,
        qn("w:dayShort"): empty,
        qn("w:monthShort"): empty,
        qn("w:yearShort"): empty,
        qn("w:dayLong"): empty,
        qn("w:monthLong"): empty,
        qn("w:yearLong"): empty,
        qn("w:contentPart"): contentPart,
        qn("w:annotationRef"): empty,
        qn("w:footnoteRef"): empty,
        qn("w:endnoteRef"): empty,
        qn("w:footnoteReference"): empty,
        qn("w:endnoteReference"): empty,
        qn("w:commentReference"): empty,
        qn("w:object"): empty,
        qn("w:drawing"): empty,
    },
    TAGS_TO_IGNORE=[
        qn("w:rPr"),
        qn("w:delText"),
        qn("w:delInstrText"),
        qn("w:pgNum"),
        qn("w:separator"),
        qn("w:continuationSeparator"),
        qn("w:ruby"),
        qn("w:lastRenderedPageBreak"),
    ],
)
