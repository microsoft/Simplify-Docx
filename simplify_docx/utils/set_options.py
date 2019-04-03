"""
Utilities for setting options that change how the document is traversed
"""

from docx.oxml.ns import qn
from typing import Dict, Union, Type
from ..iterators.generic import register_iterator, build_iterators
from ..elements import empty, fldSimple, hyperlink, customXml, subDoc, el

def set_options(options: Dict[str, Union[str, bool, int, float]]) -> None:
    """
    Register iterators depending on the selected options
    """
    __set_EG_PContents__(options)
    __set_EG_ContentRunContents__(options)
    build_iterators()


def __set_EG_PContents__(options: Dict[str, Union[str, bool, int, float]]) -> None:
    """
    group:"EG_PContent"
    """
    TAGS_TO_YIELD: Dict[str, Type[el]] = {qn("w:subDoc"): subDoc}

    TAGS_TO_NEST: Dict[str, str] = {qn("w:r"): "CT_R"}

    # -----------------------------------------------
    if options["flatten-simpleField"]:
        TAGS_TO_NEST[qn("w:fldSimple")] = "EG_PContent"
    else:
        TAGS_TO_YIELD[qn("w:fldSimple")] = fldSimple

    # -----------------------------------------------
    if options["flatten-hyperlink"]:
        TAGS_TO_NEST[qn("w:hyperlink")] = "EG_PContent"
    else:
        TAGS_TO_YIELD[qn("w:hyperlink")] = hyperlink

    # -----------------------------------------------
    register_iterator(
        "EG_PContent",
        TAGS_TO_YIELD=TAGS_TO_YIELD,
        TAGS_TO_NEST=TAGS_TO_NEST,
        TAGS_TO_IGNORE=[qn("w:customXmlPr"), qn("w:smartTagPr")],
        extends=["EG_RunLevelElts"],
        check_name=False,
    )


def __set_EG_ContentRunContents__(
    options: Dict[str, Union[str, bool, int, float]]
) -> None:
    """
    group: EG_ContentRunContent
    """

    TAGS_TO_YIELD: Dict[str, Type[el]] = {qn("w:sdt"): empty}

    TAGS_TO_NEST: Dict[str, str] = {qn("w:r"): "CT_R"}

    # -----------------------------------------------
    if options["flatten-smartTag"]:
        TAGS_TO_NEST[qn("w:smartTag")] = "EG_PContent"
    else:
        TAGS_TO_YIELD[qn("w:smartTag")] = empty

    # -----------------------------------------------
    if options["flatten-customXml"]:
        TAGS_TO_NEST[qn("w:customXml")] = "EG_PContent"
    else:
        TAGS_TO_YIELD[qn("w:customXml")] = customXml

    # -----------------------------------------------
    register_iterator(
        "EG_ContentRunContents",
        TAGS_TO_YIELD=TAGS_TO_YIELD,
        TAGS_TO_NEST=TAGS_TO_NEST,
        TAGS_TO_WARN={
            qn("w:dir"): "Ignoring text-direction tags",
            qn("w:bdo"): "Ignoring text-direction tags",
        },
        extends=["EG_RunLevelElts"],
        check_name=False,
    )
