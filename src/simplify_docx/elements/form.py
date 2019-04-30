"""
Form Field Data
"""
from typing import Dict, Any, Sequence, Optional, Iterator
from warnings import warn
from ..types import xmlFragment
from . import el
from .base import get_val


class checkBox(el):
    """
    The ffData checkBox attribute
    """

    __type__ = "CT_FFCheckBox"
    __props__ = ["default", "checked"]


class ddList(el):
    """
    The ffData ddList attribute
    """

    __type__ = "CT_FFDDList"
    __props__ = ["default", "result", "listEntry_lst"]


class textInput(el):
    """
    The ffData textInput attribute
    """

    __type__ = "CT_FFTextInput"
    __props__ = ["default", "type_", "format_"]


class ffData(el):
    """
    The ffData element
    """

    __props__ = [
        "name",
        "label",
        "tabIndex",
        "enabled",
        "calcOnExit",
        "entryMacro",
        "exitMacro",
        "helpText",
        "statusText",
    ]
    __type__: str = "CT_FFData"

    def __init__(self, x: xmlFragment):
        super(ffData, self).__init__(x)

        _checkBox = x.checkBox
        if _checkBox is not None:
            self.checkBox = checkBox(_checkBox)

        _ddList = x.ddList
        if _ddList is not None:
            self.ddList = ddList(_ddList)

        _textInput = x.textInput
        if _textInput is not None:
            self.textInput = textInput(_textInput)

    def to_json(self, doc, options, super_iter: Optional[Iterator] = None):

        out = super(ffData, self).to_json(doc, options, super_iter)

        if self.fragment.checkBox is not None:
            out["checkBox"] = self.checkBox.to_json(doc, options)

        if self.fragment.ddList is not None:
            out["ddList"] = self.ddList.to_json(doc, options)

        if self.fragment.textInput is not None:
            out["textInput"] = self.textInput.to_json(doc, options)

        return out

    def field_results(self):
        """
        Extract the field results elements
        """
        return self.fragment


class fldChar(el):
    """
    Form Field Data
    """

    __type__: str = "fldChar"
    __props__ = ["fldCharType", "fldLock", "dirty"]

    fieldCodes: Sequence[el]
    fieldResults: Sequence[el]
    ffData: Optional[ffData]

    def __init__(self, x: xmlFragment):
        super(fldChar, self).__init__(x)

        self.status = "fieldCodes"
        self.fieldCodes = []
        self.fieldResults = []
        self._ffData = x.ffData

        _ffData = x.ffData
        if _ffData is not None:
            self.ffData = ffData(_ffData)
            if x.ffData.checkBox is not None:
                self.__type__ = "Checkbox"
            elif x.ffData.ddList is not None:
                self.__type__ = "DropDown"
            elif x.ffData.textInput is not None:
                self.__type__ = "TextInput"
            else:
                warn(
                    "fldChar has unexpected ffData attribute: treating as generic-field"
                )
                self.__type__ = "generic-field"
        else:
            self.ffData = None
            self.__type__ = "generic-field"

    def to_json(  # pylint: disable=too-many-branches, too-many-return-statements, too-many-statements
        self, doc, options: Dict[str, str], super_iter: Optional[Iterator] = None
    ) -> Dict[str, Any]:

        out = super(fldChar, self).to_json(doc, options, super_iter)
        from .paragraph import merge_run_contents

        if self.__type__ == "Checkbox":
            checked = self.ffData.checkBox.props["checked"]
            if checked is None and options.get("use-checkbox-default", True):
                checked = self.ffData.checkBox.props["default"]
            value = None if checked is None else checked.val

            if options.get("checkbox-as-text", False):
                out.update(
                    {"TYPE": "CT_Text", "VALUE": "[%s:%s]" % (self.__type__, value)}
                )
                return out

            if options.get("simplify-checkbox", True):
                del out["fldCharType"]
                out["VALUE"] = value
                _update_from(out, self.ffData.checkBox.props, ["default"])
                return out

        elif self.__type__ == "DropDown":
            _values = self.ffData.ddList.props["listEntry_lst"]

            if options.get("trim-dropdown-options", True):
                for _value in _values:
                    _value.val = _value.val.strip()

            if not _values:
                value = None
            else:
                _result = self.ffData.ddList.props["result"]
                _default = self.ffData.ddList.props["default"]
                if _result is None:
                    if _default is None:
                        value = _values[0].val
                    else:
                        value = _values[_default.val].val
                else:
                    value = _values[_result.val].val

            if options.get("dropdown-as-text", False):
                out.update(
                    {"TYPE": "CT_Text", "VALUE": "[%s:%s]" % (self.__type__, value)}
                )
                return out

            if options.get("simplify-dropdown", True):
                del out["fldCharType"]
                out["VALUE"] = value
                _update_from(
                    out,
                    self.ffData.ddList.props,
                    ["default", "result", "listEntry_lst"],
                )
                out["options"] = out.pop("listEntry_lst")
                return out

        elif self.__type__ == "TextInput":

            _contents = [elt.to_json(doc, options) for elt in self.fieldResults]
            contents = merge_run_contents(_contents, options)
            value = contents[0]["VALUE"] if len(contents) == 1 else contents

            if options.get("textinput-as-text", False):
                if len(contents) > 1:
                    warn(
                        "Textinput has more than one element; ignoring all but the first element"
                    )
                out.update(
                    {
                        "TYPE": "CT_Text",
                        "VALUE": "[%s:%s]" % (contents[0]["VALUE"] if contents else ""),
                    }
                )
                return out

            if options.get("simplify-textinput", True):
                del out["fldCharType"]
                if len(contents) > 1:
                    warn(
                        "Textinput has more than one element; ignoring all but the first element"
                    )
                out["VALUE"] = contents[0]["VALUE"] if contents else ""
                _update_from(out, self.ffData.textInput.props, ["default"])
                return out

        else:

            _contents = [elt.to_json(doc, options) for elt in self.fieldResults]
            value = merge_run_contents(_contents, options)
            if options.get("flatten-generic-field", True):
                out["VALUE"] = value
                del out["fldCharType"]
                return out

        _contents = [elt.to_json(doc, options) for elt in self.fieldResults]
        contents = merge_run_contents(_contents, options)
        codes = [elt.to_json(doc, options) for elt in self.fieldCodes]

        out.update(
            {
                "TYPE": self.__type__,
                "VALUE": value,
                "ffData": self.ffData.to_json(doc, options),
                "fieldCodes": codes,
                "fieldResults": contents,
            }
        )

        return out

    def update(self, other: el) -> bool:
        """
        Update an incomplete field character
        """

        if self.status == "complete":
            RuntimeError("Logic Error: Updating a completed field data")

        if isinstance(other, fldChar):
            if other.props["fldCharType"] == "begin":
                raise RuntimeError("Unhandled nesting of data fields")

            if other.props["fldCharType"] == "separate":
                self.status = "fieldResults"
                return False
            if other.props["fldCharType"] == "end":
                self.status = "complete"
                return True

        if self.status == "fieldResults":
            self.fieldResults.append(other)
        else:
            self.fieldCodes.append(other)
        return False


def _update_from(x: Dict[str, Any], y: Dict[str, Any], attrs: Sequence[str]) -> None:
    """
    A utility function for copying attributes from one object to another
    """
    for attr in attrs:
        val = y.get(attr, None)
        if val is not None:
            x[attr] = get_val(val)
