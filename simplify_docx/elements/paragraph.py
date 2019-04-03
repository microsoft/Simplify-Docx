"""
Elements which inherit from EG_PContent
"""
from typing import Optional, Dict, List, Any, Sequence, Iterator
from warnings import warn
from . import el, container
from .form import fldChar
from ..utils.paragrapy_style import get_paragraph_ind

class EG_PContent(container):
    """
    Base class for elements which with  EG_PContent
    """

    def to_json(
        self, doc, options: Dict[str, str], super_iter: Optional[Iterator] = None
    ) -> Dict[str, Any]:

        _fldChar = None
        _fldChar: Optional[fldChar]
        bare_contents = []

        run_iterator = iter(self)
        while True:

            # ITERATE OVER THE PARAGRAPH CONTENTS
            for elt in run_iterator:

                if _fldChar is not None:
                    finished: bool = _fldChar.update(elt)
                    if finished:
                        _fldchar_json = _fldChar.to_json(doc, options)

                        if _fldchar_json.get(
                            "TYPE", None
                        ) == "generic-field" and options.get(
                            "flatten-generic-field", True
                        ):
                            bare_contents.extend(_fldchar_json.get("VALUE", []))
                        else:
                            bare_contents.append(_fldchar_json)
                        _fldChar = None
                    continue

                if isinstance(elt, fldChar):
                    _fldChar = elt
                    continue

                bare_contents.append(elt.to_json(doc, options))

            if _fldChar is not None:
                # THE PARAGRAPH ENDED IN AN INCOMPLETE FORM-FIELD
                if options.get("greedy-text-input", True):
                    _next = super_iter.peek()
                    if isinstance(super_iter.peek(), paragraph):
                        # TODO: insert a line break into the text run...
                        run_iterator = iter(super_iter.__next__())
                    else:
                        warn(
                            "Paragraph ended with an un-closed form-field followed by a %s element: this may cause parsing to fail"
                            % _next.__class__.__name__
                        )
                        break
                else:
                    warn(
                        "Paragraph ended with an un-closed form-field: this may cause parsing to fail.  Consider setting 'greedy-text-input' to True."
                    )
                    break
            else:
                break

        contents = merge_run_contents(bare_contents, options)
        return {"TYPE": self.__type__, "VALUE": contents}


def merge_run_contents(x: Sequence[Dict[str, Any]], options: Dict[str, str]):
    """
    Merge a series of run contents as appropriate
    """

    out: List[Dict[str, Any]] = []
    prev_data: Optional[Dict[str, Any]] = None
    for data in x:

        if (
            options.get("ignore-empty-text", True)
            and data["TYPE"] == "CT_Text"
            and not data["VALUE"]
        ):
            continue

        if not prev_data:
            prev_data = data
            out.append(data)
            continue

        if (
            prev_data["TYPE"] == "CT_Text"
            and data["TYPE"] == "CT_Text"
            and options.get("merge-consecutive-text", True)
        ):
            prev_data["VALUE"] += data["VALUE"]

        else:
            prev_data = data
            out.append(data)

    return out


class numPr(el):
    """
    The paragraph numbering property
    """

    __type__ = "numPr"
    __props__ = ["ilvl", "numId"]


class indentation(el):
    """
    ``<w:ind>`` element, specifying paragraph indentation.
    """

    __type__ = "CT_Ind"
    __props__ = ["left", "right", "firstLine", "hanging"]


class paragraph(EG_PContent):  
    """ 
    Represents a simple paragraph
    """

    __name__ = "CT_P"
    __type__ = "CT_P"

    def to_json(
        self, doc, options: Dict[str, str], super_iter: Optional[Iterator] = None
    ) -> Dict[str, Any]:
        """Coerce a container object to JSON
        """
        out: Dict[str, Any] = super(paragraph, self).to_json(doc, options, super_iter)

        if options.get("remove-leading-white-space", True):
            children: List[Dict[str, Any]] = out["VALUE"]
            while children:
                if children[0]["TYPE"] != "CT_Text":
                    break
                first = children.pop(0)
                first["VALUE"] = first["VALUE"].lstrip()
                if first["VALUE"]:
                    children.insert(0, first)
                    break

        if options.get("remove-trailing-white-space", True):
            children = out["VALUE"]
            while children:
                if children[-1]["TYPE"] != "CT_Text":
                    break
                last = children.pop()
                last["VALUE"] = last["VALUE"].rstrip()
                if last["VALUE"]:
                    children.append(last)
                    break

        if options.get("include-paragraph-indent", True):
            _indent = get_paragraph_ind(self.fragment, doc)
            if _indent is not None:
                out["style"] = {"indent": indentation(_indent).to_json(doc, options)}

        if (
            options.get("include-paragraph-numbering", True)
            and self.fragment.pPr is not None
            and self.fragment.pPr.numPr is not None
        ):
            out["style"] = out.get("style", {})
            out["style"]["numPr"] = numPr(self.fragment.pPr.numPr).to_json(doc, options)

        return out


class hyperlink(EG_PContent):  
    """
    The hyperlink element
    """

    __type__ = "CT_Hyperlink"
    __props__ = ["anchor", "docLocatoin", "history", "id", "tgtFrame", "tooltip"]


class fldSimple(EG_PContent):  
    """
    The SimpleField element
    """

    __type__ = "CT_SimpleField"
    __props__ = ["instr", "fldLock", "dirty"]


class customXml(container):  
    """
    The customXml element
    """

    __name__ = "CustomXmlRun"
    __type__ = "CT_CustomXmlRun"
    __props__ = ["element"]


class smartTag(container):  
    """
    The smartTag element
    """

    __name__ = "CT_SmartTagRun"
    __type__ = "EG_PContent"
    __props__ = ["element", "uri"]
