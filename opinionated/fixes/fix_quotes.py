import configparser
import os
from lib2to3 import fixer_base
from lib2to3.fixer_util import attr_chain, syms

CONFIG_VALS = {
    'SINGLE': '\'',
    'DOUBLE': '"',
}
SINGLE = '\''
DOUBLE = '"'
QUOTES = (SINGLE*3, SINGLE, DOUBLE*3, DOUBLE)
QUOTESET = frozenset([SINGLE, DOUBLE])
BACKSLASH = '\\'


def generate_possible_local_files(project_filenames=['setup.cfg'], startdir=None):
    """Find and generate all local config files."""
    tail = parent = startdir
    found_config_files = False
    while tail and not found_config_files:
        for project_filename in project_filenames:
            filename = os.path.abspath(os.path.join(parent,
                                                    project_filename))
            if os.path.exists(filename):
                yield filename
                found_config_files = True
        parent, tail = os.path.split(parent)


def is_quoted_with(value, quote):
    return value.startswith(quote) and value.endswith(quote)


def get_quote(value):
    for quote in QUOTES:
        if is_quoted_with(value, quote):
            return quote
    assert False, value


def get_first_quote(value):
    return next(filter(QUOTESET.__contains__, value))


def split_prefix(value):
    assert any(q in value for q in QUOTES)
    quote = get_first_quote(value)
    position = value.index(quote)
    return (value[:position], value[position:])

def unescape(s, quote):
    return s.replace(BACKSLASH + quote, quote)


def escape(s, quote):
    return s.replace(quote, BACKSLASH + quote)

DOCSTRING_HOLDERS = frozenset((syms.funcdef, syms.classdef, syms.file_input))
def is_docstring(node):
    top = next(filter(lambda i: i.type in DOCSTRING_HOLDERS, attr_chain(node, 'parent')))

    if top.type == syms.file_input:
        return top.children[0].children[0] == node
    if top.type in (syms.funcdef, syms.classdef):
        return next(filter(lambda x: x.type == syms.suite, top.children)).children[2].children[0] == node
    return False


def unquote(value: str, quote: str):
    return value[len(quote):-len(quote)]


def enquote(value, quote):
    return quote + value + quote


def get_quote_preference_from_config(filename):
    cfg = next(generate_possible_local_files(startdir=filename), None)
    if cfg:
        config = configparser.SafeConfigParser()
        config.read(cfg)
        if config.has_section('quotalizer'):
            return CONFIG_VALS[config['quotalizer']['preferred_quote']]
    return CONFIG_VALS['SINGLE']


class FixQuotes(fixer_base.BaseFix):
    PATTERN = 'STRING'

    def set_filename(self, filename):
        super().set_filename(filename)
        self.preferred_quote = get_quote_preference_from_config(filename)

    def transform(self, node, results):
        if (is_docstring(node)):
            return
        original_value = node.value
        pfx, value = split_prefix(node.value)
        quote = get_quote(value)
        # TODO: make quote compaction configurable
        target_quote = self.preferred_quote if '\n' not in node.value else (self.preferred_quote * 3)
        value = escape(
            unescape(unquote(value, quote), quote[0]),
            target_quote
        )
        new_value = pfx + enquote(value, target_quote)
        if original_value != new_value:
            node.value = new_value
            node.changed()
