# Overview

DOCX files are complex, and their complexity makes scraping documents
for their content difficult. The aim of this package is to simplify
`.docx` files to just the components which carry meaning thereby easing the
process of document identification and scraping by converting a `.docx`
file into a predictable an *human readable* JSON file.

Simplifying a complex document down to it's *meaningful* parts of course
requires taking a position on what does and does-not convey meaning in a
document. Generally, this package takes the stance that the document
structure (body, paragraphs, tables, etc.) are meaningful as is the text
itself, whereas text styling (font, font-weight, etc.) is ignored almost
entirely, with the exception of paragraph indentation and numbering which
is often used to create lists, block quotes, etc.  Furthermore, the
opinions expressed by this package are explained in the Options section
below and can be changed to suite your needs.

# Usage
```python
import docx
from simplify_docx import simplify

# read in a document 
my_doc = docx.Document("/path/to/my/favorite/file.docx")

# coerce to JSON using the standard options
my_doc_as_json = simplify(my_doc)

# or with non-standard options
my_doc_as_json = simplify(my_doc,{"remove-leading-white-space":False})
```

# Installation

This project relies on the `python-docx` package which can be installed via
`pip install python-docx`. **However**, as of this writing, if you wish to
scrape documents which contain (A) form fields such as drop down lists,
checkboxes and text inputs or (B) nested documents (subdocs, altChunks,
etc.), you'll need to clone [this fork](https://github.com/jdthorpe/python-docx) of the python-docx package.

# Options

### General

* **"friendly-names"**: (*Default = `True`*): Use user-friendly type names
	such as "table-cell", over standard element names like "CT_Tc"

### Ignoring Invisible things

* **"ignore-empty-paragraphs"**: (*Default = `True`*): Empty paragraphs are
	often used for styling purpose and rarely have significance in the
	meaning of the document.
* **"ignore-empty-text"**: (*Default = `True`*): Empty text runs can make an
	otherwise empty paragraph appear to contain data.
* **"remove-leading-white-space"**: (*Default = `True`*): Leading white-space
	at the start of a paragraph is ocassionaly used for styling purposes
	and rarely has significance in the interpretation of a document.
* **"remove-trailing-white-space"**: (*Default = `True`*): Trailing white-space
	at the end of a paragraph rarely has significance in the interpretation
	of a document.
* **"flatten-inner-spaces"**: (*Default = `False`*): Collapse multiple
	space characters between words to a single space.
* **"ignore-joiners"**: (*Default = `False`*): Zero width joiner and non-joiner 
	characters are special characters used to create ligatures in displayed
	text and don't typically convey meaning (at least in alphabet based
	languages).

### Special symbols

* **"dumb-quotes"**: (*Default = `True`*): Replace smart quotes with
	dumb quotes.
* **"dumb-hyphens"**: (*Default = `True`*): Replace en-dash, em-dash,
	figure-dash, horizontal bar, and non-breaking hyphens with ordinary hyphens.
* **"dumb-spaces"**: (*Default = `True`*): Replace zero width spaces, hair 
	spaces, thin spaces, punctuation spaces, figure spaces, six per em
	spaces, four per em spaces, three per em spaces, em spaces, en spaces,
	em quad spaces, and en quad spaces with ordinary spaces.
* **"special-characters-as-text"**: (*Default = `True`*): Coerce special
	characters into text equivalents according to the following table:

| Character | Text Equivalent | 
| --------- | --------------- | 
| CarriageReturn | `\n` |
| Break | `\r` |
| TabChar | `\t` |
| PositionalTab | `\t` |
| NoBreakHyphen | `-` |
| SoftHyphen | `-` |

* **"symbol-as-text"**: (*Default = `True`*): Special symbols often cary
	meaning other than the underlying unicode character, especially when
	the font is a special font such as `Wingdings`. If `True` these are
	included as ordinary text and their font information is omitted.
* **"empty-as-text"**: (*Default = `False`*): There are a variety of "Empty"
	tags such as the `<"w:yearLong">` tag which cause the current year to
	be inserted into the document text. If `True`, include these as text
	formatted as `"[yearLong]"`.
* **"ignore-left-to-right-mark"**: (*Default = `False`*): Ignore the left-to-right
	mark, which is not writeable by pythons csv writer.
* **"ignore-right-to-left-mark"**: (*Default = `False`*): Ignore the right-to-left
	mark which is not writeable by pythons csv writer.

### Paragraph style:

Paragraph style markup are one exception to the styling vs. content
dichotomy. For example, block quotes are often indicated by indenting whole
paragraphs, and Ordered lists, Unordered lists and nesting of lists is
often used to divide sections of a document into logical components. 

* **"include-paragraph-indent"**: (*Default = `True`*): Include the
	indentation markup on paragraph (`CT_P`) elements. Indentation is
	measured in twips
* **"include-paragraph-numbering"**: (*Default = `True`*): Include the
	numbering styles, which are included in the `CT_P.pPr.numPr` element.
	The `ilvl` attribute indicates the level of nesting (zero based index)
	and the `numId` attribute refers to a specific numbering style
	included in the document's internal styles sheet. 

### Form Elements

* **"simplify-dropdown"**: (*Default = `True`*): Include just the selected
	and default values, the available options, and the name and label attributes in the form element.
* **"simplify-textinput"**: (*Default = `True`*): Include just the current
	and default values, and the name and label attributes in the form element.
* **"greedy-text-input"**: (*Default = `True`*): Continue consuming run
	elements when the text-input has not ended at the end of a paragraph,
	and the next block level element is also a paragraph. This typically
	occurs when the user preses the return key while editing a text input
	field.
* **"simplify-checkbox"**: (*Default = `True`*): Include just the current
	and default values, and the name and label attributes in the form element.
* **"use-checkbox-default"**: (*Default = `True`*): If the checkbox has no
	`value` attribute (typically because the user has not interacted with
	it), report the default value as the checkbox value.
* **"checkbox-as-text"**: (*Default = `False`*): Coerce the value of the
	checkbox to text, represented as either `"[CheckBox:True]"` or `"[CheckBox:False]"`
* **"dropdown-as-text"**: (*Default = `False`*): Coerce the value of the
	checkbox to text, represented as `"[DropDown:<selected value>]"`
* **"trim-dropdown-options"**: (*Default = `True`*): Remove white-space on
	the left and right of drop down option items.
* **"flatten-generic-field"**: (*Default = `True`*): `generic-fields` are
	`CT_FldChar` runs which are not marked as a drop-down, text-input, or
	checkbox. These may include special instructions which apply special
	formatting to a text run (e.g. a hyper link). If `True`, the contents
	of generic-fields are included in the normal flow of text

### Special content

* **"merge-consecutive-text"**: (*Default = `True`*): Sentences and even single
	words can be represented by multiple text elements. If `True`,
	concatenate consecutive text elements into a single text element.
* **"flatten-hyperlink"**: (*Default = `True`*): Flatten hyperlinks, including
	their contents in the flow of normal text.
* **"flatten-smartTag"**: (*Default = `True`*): Flatten smartTag elements, 
	including their contents in the flow of normal text.
* **"flatten-customXml"**: (*Default = `True`*): Flatten customXml elements, 
	including their contents in the flow of normal text.
* **"flatten-simpleField"**: (*Default = `True`*): Flatten simpleField elements, 
	including their contents in the flow of normal text.

# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
