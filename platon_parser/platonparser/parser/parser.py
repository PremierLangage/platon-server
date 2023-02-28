from typing import Dict, Callable
import os
import sys
import os.path
import importlib.util
import logging
from functools import lru_cache

from platonparser.parser.utils import ParserImport, ParserOutput
from platonparser.parser.parser_exceptions import *

logger = logging.getLogger(__name__)

PARSERS_ROOT = os.path.join(os.path.dirname(__file__), '../parsers')

def load_parser_from_module(path: str):
    """Loads a parser from a path
    Calls the get_parser() function in the module to so"""
    filename = os.path.basename(path)
    module_name = os.path.splitext(filename)[0]
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    try:
        parser_import = module.get_parser()
        if type(parser_import) != ParserImport:
            logger.error(f'get_parser() function from file {filename} returned {type(parser_import)} object instead of expected ParserImport')
            return None
        return parser_import
    except AttributeError:
        logger.error(f'get_parser() function from file {filename} is not defined')
    except Exception as e:
        logger.exception(f'Could not import parser {filename}: {e}')


@lru_cache
def get_parsers(parsers_root: str) -> Dict[str, ParserImport]:
    """Loads parsers contained inside a given folder"""
    parsers = {}
    filenames = [filename for filename in os.listdir(parsers_root) if filename.endswith('.py') and '__' not in filename]
    for filename in filenames:
        parser_import = load_parser_from_module(os.path.join(parsers_root, filename))
        if parser_import is not None:
            for ext in parser_import.extensions:
                if ext in parsers:
                    logger.warn(f'Conflict detected for {ext} extension. A parser was already declared for that extension, but was overwritten by {filename}')
                parsers[ext] = parser_import   
    return parsers


def parse_file(file: bytes, path: FullPath, circle_id: int, get_location: Callable[[str, str, int, int], str]) -> ParserOutput:
    """Parses a file and returns the output"""
    parsers = get_parsers(PARSERS_ROOT)
    extension = os.path.basename(path.path).split('.')[-1]
    if extension not in parsers:
        raise NoParserError(path, extension)
    parser = parsers[extension].parser(file, path, circle_id, get_location)
    output = parser.parse()
    return output