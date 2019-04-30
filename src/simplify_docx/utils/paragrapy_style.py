"""
Helpers for extracting paragraph indention levels
"""

def get_pStyle(p, doc):
    """
    Get the referenced style element for a paragraph with a p.pPr.pStyle
    """
    if p.pPr is not None and \
            p.pPr.pStyle is not None:
        return doc.styles.element.find("w:style[@w:styleId='%s']" % p.pPr.pStyle.val,
                doc.styles.element.nsmap)
    return None


def get_num_style(p, doc):
    """
    The the paragraph's Numbering style
    """
    if p.pPr is not None \
            and p.pPr.numPr is not None\
            and p.pPr.numPr.numId is not None:
        # the numbering style doc
        np = doc.part.numbering_part
        # the map between numbering id and the numbering style
        num = np.element.find("w:num[@w:numId='%s']" % p.pPr.numPr.numId.val,
                               np.element.nsmap)
        _path = "w:abstractNum[@w:abstractNumId='%s']" % num.abstractNumId.val
        # the numbering styles themselves
        abstractNumbering = np.element.find(_path, np.element.nsmap)
        return abstractNumbering.find("w:lvl[@w:ilvl='%s']" % p.pPr.numPr.ilvl.val,
                                      np.element.nsmap)
    return None


def get_paragraph_ind(p, doc):
    """
    Gets the style according to the style hierarchy listed in section 17.3.1.27
    "pStyle (Referenced Paragraph Style)"

    This formatting is applied at the following location in the style hierarchy:
    * Document defaults
    * Table styles
    * Numbering styles
    * Paragraph styles (this element)
    * Character styles
    * Direct Formatting
    """

    if p.pPr is not None and\
            p.pPr.ind is not None:
        return p.pPr.ind

    num_style = get_num_style(p, doc)
    if num_style is not None and \
            num_style.pPr is not None and \
            num_style.pPr.ind is not None:
        return num_style.pPr.ind

    pStyle = get_pStyle(p, doc)
    if pStyle is not None and \
            pStyle.pPr is not None and \
            pStyle.pPr.ind is not None:
        return pStyle.pPr.ind
    return None
