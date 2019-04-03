"""
Generic XML iterators
"""
# pylint: disable=too-many-arguments, too-many-branches

from warnings import warn
from typing import (
        Optional,
        Tuple,
        Type,
        Dict,
        Sequence,
        NamedTuple,
        NewType,
        Callable,
        Generator,
        List
)
from ..elements.base import el
from ..types import xmlFragment
from ..utils.tag import get_tag
from ..utils.warnings import UnexpectedElementWarning

FragmentIterator = NewType('FragmentIterator',
        Callable[[xmlFragment, Optional[str]], Generator[xmlFragment, None, None]])

# CONSTANTS

class ElementHandlers(NamedTuple):
    """
    A convenience class
    """
    TAGS_TO_YIELD: Optional[Dict[str, Type[el]]]
    TAGS_TO_NEST: Optional[Dict[str, str]]
    TAGS_TO_IGNORE: Optional[Sequence[str]]
    TAGS_TO_WARN: Optional[Dict[str, str]]
    TAGS_TO_SKIP: Optional[Dict[str, Tuple[str, str]]]
    extends: Optional[Sequence[str]]

ElementHandlers.__new__.__defaults__ = (None,)* 6 # https://stackoverflow.com/questions/11351032/

__definitions__: Dict[str, ElementHandlers] = {}
__built__: Dict[str, ElementHandlers] = {}

def register_iterator(name: str,
                      TAGS_TO_YIELD: Dict[str, Type[el]] = None,
                      TAGS_TO_NEST: Dict[str, str] = None,
                      TAGS_TO_IGNORE: Sequence[str] = None,
                      TAGS_TO_WARN: Dict[str, str] = None,
                      TAGS_TO_SKIP: Dict[str, Tuple[str, str]] = None,
                      extends: Optional[Sequence[str]] = None,
                      check_name: bool = True,
                     ) -> None:
    """ 
    An opinionated iterator which ignores deleted and moved resources, and
    passes through in-line revision containers such as InsertedRun, and
    orientation elements like bookmarks, comments, and permissions
    """

    if check_name and name in __definitions__:
        raise ValueError("iterator named '%s' already registered" % name)

    __definitions__[name] = ElementHandlers(
            TAGS_TO_YIELD,
            TAGS_TO_NEST,
            TAGS_TO_IGNORE,
            TAGS_TO_WARN,
            TAGS_TO_SKIP,
            extends=extends
            )

def build_iterators() -> None:
    """
    Build the iterators for the current iteration
    """

    _resovled: List[str] = []
    def _resolve(x: str):

        if x in _resovled:
            return

        xdef = __definitions__[x]
        if not xdef.extends:
            __built__[x] = xdef
            _resovled.append(x)
            return

        TAGS_TO_YIELD = dict(xdef.TAGS_TO_YIELD) if xdef.TAGS_TO_YIELD else {}
        TAGS_TO_NEST = dict(xdef.TAGS_TO_NEST) if xdef.TAGS_TO_NEST else {}
        TAGS_TO_IGNORE = list(xdef.TAGS_TO_IGNORE) if xdef.TAGS_TO_IGNORE else []
        TAGS_TO_WARN = dict(xdef.TAGS_TO_WARN) if xdef.TAGS_TO_WARN else {}
        TAGS_TO_SKIP = dict(xdef.TAGS_TO_SKIP) if xdef.TAGS_TO_SKIP else {}

        for dependency in xdef.extends:
            try:
                _resolve(dependency)
            except KeyError:
                msg = "Iterator for '%s' depends on undefined group '%s'" % (x, dependency,)
                raise RuntimeError(msg)

            ddef = __built__[dependency]
            if ddef.TAGS_TO_YIELD:
                TAGS_TO_YIELD.update(ddef.TAGS_TO_YIELD)
            if ddef.TAGS_TO_NEST:
                TAGS_TO_NEST.update(ddef.TAGS_TO_NEST)
            if ddef.TAGS_TO_IGNORE:
                TAGS_TO_IGNORE.extend(ddef.TAGS_TO_IGNORE)
            if ddef.TAGS_TO_WARN:
                TAGS_TO_WARN.update(ddef.TAGS_TO_WARN)
            if ddef.TAGS_TO_SKIP:
                TAGS_TO_SKIP.update(ddef.TAGS_TO_SKIP)

        __built__[x] = ElementHandlers(
                TAGS_TO_YIELD=TAGS_TO_YIELD,
                TAGS_TO_NEST=TAGS_TO_NEST,
                TAGS_TO_IGNORE=TAGS_TO_IGNORE,
                TAGS_TO_WARN=TAGS_TO_WARN,
                TAGS_TO_SKIP=TAGS_TO_SKIP,
                )

        _resovled.append(x)

    for name in __definitions__:
        _resolve(name)


def xml_iter(
        p: xmlFragment,
        name: str,
        msg: Optional[str] = None) -> Generator[el, None, None]:
    """
    Iterates over an XML node yielding an appropriate element (el)
    """

    handlers = __built__[name]

    # INIT PHASE
    children = p.getchildren()
    if not children:
        return

    current: Optional[xmlFragment] = p.getchildren()[0]

    # ITERATION PHASE
    while current is not None:

        if msg is not None and current.tag not in handlers.TAGS_TO_IGNORE:
            print(msg +
                  ("" if current.prefix is None else (current.prefix + ":")) +
                  current.tag)

        if handlers.TAGS_TO_YIELD \
                and current.tag in handlers.TAGS_TO_YIELD:
            # Yield all math tags
            yield handlers.TAGS_TO_YIELD[current.tag](current)

            if handlers.TAGS_TO_NEST \
                    and current.tag in handlers.TAGS_TO_NEST:
                _msg = None if msg is None else ("  "+msg)
                for elt in xml_iter(current, handlers.TAGS_TO_NEST[current.tag], _msg):
                    yield elt

        elif handlers.TAGS_TO_NEST \
                and current.tag in handlers.TAGS_TO_NEST:
            _msg = None if msg is None else ("  "+msg)
            for elt in xml_iter(current, handlers.TAGS_TO_NEST[current.tag], _msg):
                yield elt


        elif handlers.TAGS_TO_WARN \
                and current.tag in handlers.TAGS_TO_WARN:
            # Skip these unhandled tags with a warning
            warn("Skipping %s tag: %s" % (handlers.TAGS_TO_WARN[current.tag],
                                          current.tag, ))


        elif handlers.TAGS_TO_IGNORE \
                and current.tag in handlers.TAGS_TO_IGNORE:
            # ignore paragraph properties, deleted content and meta tags
            # like bookmarks, permissions, comments, etc.
            pass

        elif handlers.TAGS_TO_SKIP \
                and current.tag in handlers.TAGS_TO_SKIP:
            # Skip over content that has been moved elsewhere
            data = handlers.TAGS_TO_SKIP[current.tag]
            current = skip_range(current, data[0], data[1])
            if current is None:
                return

        else:
            warn("Skipping unexpected tag: %s" % (current.tag),
                 UnexpectedElementWarning)

        current = current.getnext()

    return


def skip_range(x: xmlFragment,
               id_attr: str,
               waitfor: str) -> Optional[xmlFragment]:
    """
    A utility which returns the element at the end of the range
    """

    _id: str = x.attrib[id_attr]
    current: Optional[xmlFragment] = x.getnext()

    while True:
        if current is None:
            return current
        if get_tag(current).tag == waitfor and current.attrib[id_attr] == _id:
            return current
        current = current.getnext()
