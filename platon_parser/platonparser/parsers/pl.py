import re
import json
import os.path
from typing import List, Tuple, Callable, Any, Dict
from ast import literal_eval
from dataclasses import dataclass

from platonparser.parser.parser_exceptions import *
from platonparser.parser.utils import Parser, ParserOutput, ParserImport, LocationResult, FullPath
from platonparser.parser.components import COMPONENT_SELECTORS


BAD_CHAR = r''.join(['/', ' ', '\t', '\n', ';', '#', '+', '&'])

# .pl grammar
KEY = r'^(?P<key>[a-zA-Z_][a-zA-Z0-9_\.]*)\s*'
COMMENT = r'(?P<comment>#.*)'
VALUE = r'(?P<value>[^=@%#][^#]*?)\s*'
FILE = r'(?P<file>([a-zA-Z0-9_]*:)?((\/)?[^' + \
    BAD_CHAR + r']+)(\/[^' + BAD_CHAR + r']+)*)\s*'
ALIAS = r'((\[\s*(?P<alias>[a-zA-Z_.][a-zA-Z0-9_.]*)\s*\])\s*?)?'

COMPONENT_LINE = re.compile(
    KEY + r'\s*(?P<operator>=:)\s*(?P<component>\w+)\s*' + COMMENT + r'?$')
URL_LINE = re.compile(
    KEY + r'(?P<operator>=\$)\s*' + FILE + COMMENT + r'?$')
ONE_LINE = re.compile(
    KEY + r'(?P<operator>=|\%|\+|\-)\s*' + VALUE + COMMENT + r'?$')
FROM_FILE_LINE = re.compile(
    KEY + r'(?P<operator>=@|\+=@|\-=@|\%@|\+@|\-@)\s*' + FILE + COMMENT + r'?$')
EXTENDS_LINE = re.compile(
    r'(extends|template)\s*=\s*' + FILE + COMMENT + r'?$')
MULTI_LINE = re.compile(
    KEY + r'(?P<operator>==|\+=|\-=|\%=)\s*' + COMMENT + r'?$')
DEPENDENCY_FILE_LINE = re.compile(r'@\s*' + FILE + ALIAS + COMMENT + r'?$')
END_MULTI_LINE = re.compile(r'==\s*$')
COMMENT_LINE = re.compile(r'\s*' + COMMENT + r'$')
EMPTY_LINE = re.compile(r'\s*$')

# Mandatory keys
MANDATORY_KEYS = ['author', 'version', 'title', 'statement', 'formState']

# Utility functions
def map_value(n: Dict[str, Any], k: str, v: Any): n[k] = v
def append_value(n: Dict[str, Any], k: str, v: Any): n[k] += v
def prepend_value(n: Dict[str, Any], k: str, v: Any): n[k] = v + n[k]


class PLParser(Parser):
    """Parser for .pl files"""
    @dataclass
    class Multiline():
        """Used to keep information about multiline parsing status"""
        ongoing: bool = False
        current_key: str = ''
        current_op: str = ''
        current_value: Any = None
        starting_line: str = ''
        starting_line_number: int = 0


    def __init__(self, file: bytes, path: FullPath, circle_id: int, get_location: Callable[[str, str, int, int], LocationResult], 
                 inherited=tuple(), check_mandatory_keys=True):
        """Initializes PLParser instance"""
        self.file = file
        self.path = path
        self.dir, self.filename = os.path.split(path.path)
        self.resource_id = path.resource_id
        self.circle_id = circle_id
        self.get_location = get_location
        self.inherited = inherited + (path,)
        self.check_mandatory_keys = check_mandatory_keys
        self.output = ParserOutput(path, circle_id, 'pl')

        self.__current_line = ''
        self.__line_number = 1
        self.__multiline = PLParser.Multiline()


    def parse(self) -> ParserOutput:
        """Parses the file and returns the corresponding output"""
        try:
            contents = self.file.decode(encoding='utf-8')
        except UnicodeError:
            raise ParserInvalidFile(self.path)

        for line in contents.split('\n'):
            self.__current_line = line
            self.parse_line(line)
            self.__line_number += 1
        
        if self.__multiline.ongoing:
            raise ParserSyntaxError(self.path, self.__current_line, self.__line_number, 'Multiline wasn\'t closed')

        if self.check_mandatory_keys:
            for key in MANDATORY_KEYS:
                if key not in self.output.data: raise ParserMissingKey(self.path, key)

        return self.output


    def parse_line(self, line: str):
        """
        Parse the given line by calling the appropriate method according to regex matches.

        Raises exceptions.ParserSyntaxError if the line wasn't match by any regex.
        """
        if self.__multiline.ongoing:
            if END_MULTI_LINE.match(line):
                self.end_multi_line()
            else:
                self.__multiline.current_value += line
        elif EXTENDS_LINE.match(line):
            self.extends_line_match(EXTENDS_LINE.match(line))
        elif FROM_FILE_LINE.match(line):
            self.from_file_line_match(FROM_FILE_LINE.match(line))
        elif URL_LINE.match(line):
            self.url_line_match(URL_LINE.match(line))
        elif COMPONENT_LINE.match(line):
            self.component_line_match(COMPONENT_LINE.match(line))
        elif DEPENDENCY_FILE_LINE.match(line):
            self.dependency_line_match(DEPENDENCY_FILE_LINE.match(line))
        elif COMMENT_LINE.match(line):
            match = COMMENT_LINE.match(line)
            if match is not None: self.output.comments.append(match.group('comment'))
        elif ONE_LINE.match(line):
            self.one_line_match(ONE_LINE.match(line))
        elif MULTI_LINE.match(line):
            self.multi_line_match(MULTI_LINE.match(line))
        elif EMPTY_LINE.match(line):
            return
        else:
            raise ParserSyntaxError(self.path, line, self.__line_number, 'Line does not correspond to any defined pattern')
        

    def one_line_match(self, match):
        """ 
        Maps value to key if operator is '=',
            appends on existing key is operator is '+',
            prepends on existing key is operator is '-',
            Maps json.loads(value) if operator is '%'

        Raise exceptions.ParserSyntaxError:
            if no group 'value', 'key' or 'operator' was found
            if operator is '%' and value isn't a well formated json
        """
        value = match.group('value')
        key = match.group('key')
        op = match.group('operator')

        if op == '=':
            self.apply_expression_to_key(key, value, map_value)
        elif op == '%':
            try:
                self.apply_expression_to_key(key, json.loads(value), map_value)
            except json.decoder.JSONDecodeError:
                raise ParserSyntaxError(self.path, self.__current_line, self.__line_number, 'Line does not correspond to a valid JSON format.')
        elif op == '+':
            self.apply_expression_to_key(key, value, append_value, key_must_exist=True)
        elif op == '-':
            self.apply_expression_to_key(key, value, prepend_value, key_must_exist=True)
        else:
            raise AssertionError


    def multi_line_match(self, match):
        """
        Starts the proecss for matching a whole multiline block
        """
        key = match.group('key')
        op = match.group('operator')

        self.__multiline.ongoing = True
        self.__multiline.current_key = key
        self.__multiline.current_op = op
        self.__multiline.current_value = ''
        self.__multiline.starting_line_number = self.__line_number
        self.__multiline.starting_line = self.__current_line


    def end_multi_line(self):
        """
        Evaluates the complete multiline value and does the action given by the operator:
            == : maps value to key
            += : appends value to key
            -= : prepends value to key
            %= : interprets value as JSON and maps to key
        """
        op = self.__multiline.current_op
        key = self.__multiline.current_key
        value = self.__multiline.current_value

        if op == '==':
            self.apply_expression_to_key(key, value, map_value)
        elif op == '%=':
            try:
                self.apply_expression_to_key(key, json.loads(value), map_value)
            except json.decoder.JSONDecodeError:
                raise ParserSyntaxError(self.path, value, self.__multiline.starting_line_number, 'Multiline does not correspond to a valid JSON format.')
        elif op == '+=':
            self.apply_expression_to_key(key, value, append_value, key_must_exist=True)
        elif op == '-=':
            self.apply_expression_to_key(key, value, prepend_value, key_must_exist=True)
        else:
            raise AssertionError
        
        self.__multiline.ongoing = False

    
    def extends_line_match(self, match):
        """
        Inheritance
        """
        location = self.call_get_location(match.group('file'))
        if location.path in self.inherited:
            raise ParserInheritanceLoopError(self.path, self.inherited)
        
        parser = PLParser(location.file, location.path, location.circle_id, self.get_location, self.inherited, check_mandatory_keys=False)
        output = parser.parse()
        self.output.merge_output(output)

        
    def from_file_line_match(self, match):
        """
        Loads file content into key
        """
        key = match.group('key')
        op = match.group('operator')
        location = self.call_get_location(match.group('file'))

        try:
            value = location.file.decode(encoding='utf-8')
        except UnicodeError:
            raise ParserInvalidFileLine(self.path, self.__current_line, self.__line_number)

        if op == '=@':
            self.apply_expression_to_key(key, value, map_value)
        elif op == '%@':
            try:
                self.apply_expression_to_key(key, json.loads(value), map_value)
            except json.decoder.JSONDecodeError:
                raise ParserSyntaxError(self.path, self.__current_line, self.__line_number, 'File does not correspond to a valid JSON format.')
        elif op in ('+=@', '+@'):
            self.apply_expression_to_key(key, value, append_value, key_must_exist=True)
        elif op in ('-=@', '-@'):
            self.apply_expression_to_key(key, value, prepend_value, key_must_exist=True)
        else:
            raise AssertionError


    def url_line_match(self, match):
        """
        Maps link to the given resource to corresponding key
        """
        #TODO: How is that supposed to work on Platon?
        key = match.group('key')
        location = self.call_get_location(match.group('file'))
        try:
            namespace, nkey = get_namespace(self.output.data, key.split('.'))
        except TypeError:
            raise ParserSemanticError(self.path, self.__current_line, self.__line_number, f'{key} does not correspond to a valid namespace')
        if nkey in namespace:
            self.output.warnings.append(f'Overwriting existing value {namespace[nkey]} at key {nkey}')
        namespace[nkey] = location.path.path


    def component_line_match(self, match):
        """
        Creates a dictionary corresponding to a component
        """
        key = match.group('key')
        component = match.group('component')
        try:
            namespace, nkey = get_namespace(self.output.data, key.split('.'))
        except TypeError:
            raise ParserSemanticError(self.path, self.__current_line, self.__line_number, f'{key} does not correspond to a valid namespace')
        
        if component not in COMPONENT_SELECTORS: raise ParserComponentNotFound(self.path, self.__current_line, self.__line_number, 'Component not found in line.')

        if nkey in namespace:
            self.output.warnings.append(f'Overwriting existing value {namespace[nkey]} at key {nkey}')

        namespace[nkey] = {
            'selector': COMPONENT_SELECTORS[component],
            'form': {}
        }


    def dependency_line_match(self, match):
        """
        Adds a file to the dependencies to load in the sandbox environnement
        """
        location = self.call_get_location(match.group('file'))

        alias = match.group('alias') or os.path.basename(location.path.path)
        self.output.dependencies.add((location.path, alias))


    def apply_expression_to_key(self, key: str, expr: str, apply: Callable[[Dict[str, Any], str, Any], None], key_must_exist:bool=False):
        """Evaluates expr like a Python expression and applies it to the corresponding key
        in the data section of the output using the given callable. If the expression is invalid, it is evaluated
        as a string directly
        
        Raises exceptions.ParserSemanticError if the key is expected to already exist and it doesn't
        """
        line_number = self.__line_number if not self.__multiline.ongoing else self.__multiline.starting_line_number
        current_line = self.__current_line if not self.__multiline.ongoing else self.__multiline.starting_line

        try:
            namespace, nkey = get_namespace(self.output.data, key.split('.'))
        except TypeError:
            raise ParserSemanticError(self.path, current_line, line_number, f'{key} does not correspond to a valid namespace')
        if nkey in namespace:
            self.output.warnings.append(f'Overwriting existing value at key "{key}"')
        if key_must_exist and nkey not in namespace: 
            raise ParserSemanticError(self.path, current_line, line_number, f'{key} does not already exist')
        try:
            value = literal_eval(expr)
        except (ValueError, TypeError, SyntaxError):
            value = expr
        apply(namespace, nkey, value)


    def call_get_location(self, URI: str):
        """Finds real path to a file given pl path"""
        result = self.get_location(URI, self.dir, self.resource_id, self.circle_id)
        if not result: raise ParserFileNotFound(self.path, self.__current_line, self.__line_number, 'URIcould not be resolved')
        return result
  

def get_namespace(d: dict, keys: List[str]) -> Tuple[dict, str]:
    """Navigates, and creates if necessary, subdictionaries in the order of
    the list of keys given and returns a tuple the last subdictionary found/created
    and the last key
    
    Raises TypeError if one of the namespaces is not a dictionary
    """
    for key in keys[:-1]:
        if not key: raise TypeError(f'key cannot be empty')
        if type(d) != dict: raise TypeError(f'{d} is not a dictionary')
        if key not in d: d[key] = {}
        d = d[key]
    if not keys[-1]: raise TypeError(f'key cannot be empty')
    if type(d) != dict: raise TypeError(f'{d} is not a dictionary')
    return d, keys[-1]


def get_parser() -> ParserImport:
    """Used to dynamically add parser to the loader"""
    return ParserImport(PLParser, 'pl', ('pl',))