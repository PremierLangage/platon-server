import re
import json
import uuid
from django.conf import settings
from pl_runner.components import SELECTORS

from pl_runner.exceptions import ComponentNotFound, SemanticError, SyntaxErrorPL

BAD_CHAR = r''.join(settings.FILEBROWSER_DISALLOWED_CHAR)
class Parser:

    KEY = r'^(?P<key>[a-zA-Z_][a-zA-Z0-9_\.]*)\s*'
    COMMENT = r'(?P<comment>#.*)'
    VALUE = r'(?P<value>[^=@%#][^#]*?)\s*'
    FILE = r'(?P<file>([a-zA-Z0-9_]*:)?((\/)?[^' + BAD_CHAR + r']+)(\/[^' + BAD_CHAR + r']+)*)\s*'
    ALIAS = r'((\[\s*(?P<alias>[a-zA-Z_.][a-zA-Z0-9_.]*)\s*\])\s*?)?'
    
    COMPONENT_LINE = re.compile(
        KEY + r'\s*(?P<operator>=:)\s*(?P<component>\w+)\s*' + COMMENT + r'?$')
    URL_LINE = re.compile(KEY + r'(?P<operator>=\$)\s*' + FILE + COMMENT + r'?$')
    ONE_LINE = re.compile(KEY + r'(?P<operator>=|\%|\+|\-)\s*' + VALUE + COMMENT + r'?$')
    FROM_FILE_LINE = re.compile(KEY + r'(?P<operator>=@|\+=@|\-=@)\s*' + FILE + COMMENT + r'?$')
    EXTENDS_LINE = re.compile(r'(extends|template)\s*=\s*' + FILE + COMMENT + r'?$')
    MULTI_LINE = re.compile(KEY + r'(?P<operator>==|\+=|\-=|\%=)\s*' + COMMENT + r'?$')
    SANDBOX_FILE_LINE = re.compile(r'@\s*' + FILE + ALIAS + COMMENT + r'?$')
    END_MULTI_LINE = re.compile(r'==\s*$')
    COMMENT_LINE = re.compile(r'\s*' + COMMENT + r'$')
    EMPTY_LINE = re.compile(r'\s*$')
    HTML_KEYS = ['title', 'teacher', 'introductionh', 'text', 'form']

    def __init__(self, file_name: str, file: bytes) -> None:
        self.file_name = file_name
        self.file = file
        self.extends = list()
        self.dic = dict()
        self.warning = list()
        self.lines = list()
        self.lineno = 1
        self._multiline_dic = None
        self._multiline_key = None
        self._multiline_op = None
        self._multiline_value = None
        self._multiline_opened_lineno = None
        self._multiline_json = False
    
    def get_dic(self) -> dict:
        return self.dic
    
    def meta(self) -> None:
        """Append meta informations to self.dic. Meta informations
        should starts with two underscores"""
        self.dic['__format'] = '.pl'
        self.dic['__comment'] = ''
        self.dic['__includes'] = list()
        self.dic['__template'] = list()
        self.dic['__extends'] = list()

    def add_warning(self, message: str):
        """Append a warning the self.warning list according to message."""
        f = (self.file_name, self.lineno, message, self.lines[self.lineno - 1])
        self.warning.append("%s:%d -- %s\n%s" % f)

    def dic_add_key(self, key: str, value, append=False, prepend=False, replace=False):
        """Add the value to the key in the dictionnary, parse the key to create sub dictionnaries.
         Append the value if append is set to True.
         Prepend the value if prepend is set to True.
         Does not generate a warning when the key already exists if replace is set to True """
        current_dic = self.dic
        sub_keys = key.split(".")
        for k in sub_keys:
            if k == '':
                raise SyntaxErrorPL(self.file_name, self.lines[self.lineno - 1], self.lineno)
        for k in sub_keys[:-1]:  # creating sub dictionnaries
            current_dic[k] = current_dic.get(k, dict())
            current_dic = current_dic[k]
        last_key = sub_keys[-1]
        
        if last_key in current_dic and not append and not prepend and not replace:
            self.add_warning("Key '" + key + "' overwritten at line " + str(self.lineno))
        if append:
            if last_key not in current_dic:
                line = self._multiline_opened_lineno if self._multiline_key else self.lineno
                error = "Trying to append to non-existent key '" + key + "'."
                raise SemanticError(self.file_name, self.lines[line - 1], line, error)
            current_dic[last_key] += value
        elif prepend:
            if last_key not in current_dic:
                line = self._multiline_opened_lineno if self._multiline_key else self.lineno
                error = "Trying to prepend to non-existent key '" + key + "'."
                raise SemanticError(self.file_name, self.lines[line - 1], line, error)
            current_dic[last_key] = value + current_dic[last_key]
        else:
            current_dic[last_key] = value
    
    def parse(self):
        self.meta()
        self.lines = self.file.decode().split('\n')
        for line in self.lines:
            try:
                self.parse_line(line)
            except UnicodeDecodeError:
                raise SyntaxErrorPL(self.file_name,
                                    self.lines[self.lineno - 1],
                                    self.lineno,
                                    message="Cannot reference a binary file")
            self.lineno += 1
        
        if self._multiline_key:  # If a multiline value is still open at the end of the parsing
            raise SyntaxErrorPL(self.file_name,
                                self.lines[self._multiline_opened_lineno - 1],
                                self._multiline_opened_lineno,
                                message="Multiline value never closed, start ")
        
        return self.dic, self.warning

    def parse_line(self, line: str):
        """ Parse the given line by calling the appropriate function according to regex match.

            Raise loader.exceptions.SyntaxErrorPL if the line wasn't match by any regex."""
        line = line + '\n'

        if self._multiline_key:
            self.while_multi_line(line)
        
        elif self.EXTENDS_LINE.match(line):
            self.extends_line_match(self.EXTENDS_LINE.match(line), line)
            
        # elif self.FROM_FILE_LINE.match(line):
        #     self.from_file_line_match(self.FROM_FILE_LINE.match(line), line)
        
        # elif self.URL_LINE.match(line):
        #     self.url_line_match(self.URL_LINE.match(line), line)
        
        elif self.COMPONENT_LINE.match(line):
            self.component_line_match(self.COMPONENT_LINE.match(line), line)
        
        elif self.ONE_LINE.match(line):
            self.one_line_match(self.ONE_LINE.match(line), line)
        
        elif self.SANDBOX_FILE_LINE.match(line):
            self.sandbox_file_line_match(self.SANDBOX_FILE_LINE.match(line), line)
        
        elif self.MULTI_LINE.match(line):
            self.multi_line_match(self.MULTI_LINE.match(line), line)
        
        elif self.COMMENT_LINE.match(line):
            self.dic['__comment'] += '\n' + self.COMMENT_LINE.match(line).group('comment')
        
        elif not self.EMPTY_LINE.match(line):
            raise SyntaxErrorPL(self.file_name, line, self.lineno)

    def extends_line_match(self, match, line: str):
        """ Appends file, line and lineno to self.dic['__extends'] so that it can be later processed
            by ... TODO
        
        """
        try:
            path = match.group('file')
            self.dic['__extends'].append(path)
        except IndexError:
            raise SyntaxErrorPL(self.file_name, self.lines[self.lineno], self.lineno)


    def sandbox_file_line_match(self, match, line: str):
        try:
            src_path = match.group('file')
            exp_path = match.group('alias')
        except IndexError:
            raise SyntaxErrorPL(self.file_name, self.lines[self.lineno], self.lineno)

        if exp_path is None:
            exp_path = "/".join(src_path.strip("/").split("/")[1:])
        
        self.dic['__includes'].append({
            'src_path':     src_path,
            'exp_path':     exp_path
        })

    def one_line_match(self, match, line: str):
        """ Map value to key if operator is '=',
            Map json.loads(value) if operator is '%'

            Raise from loader.exceptions:
                - SyntaxErrorPL if no group 'value', 'key' or 'operator' was found
                              if operator is '%' and value isn't a well formated json"""
        
        value = match.group('value')
        key = match.group('key')
        op = match.group('operator')
        
        if op == '=':
            self.dic_add_key(key, value)
        elif op == '%':
            try:
                self.dic_add_key(key, json.loads(value))
            except json.decoder.JSONDecodeError:
                raise SyntaxErrorPL(self.file_name,
                                    line,
                                    self.lineno,
                                    message="Invalid JSON syntax starting ")
        elif op == '+':
            self.dic_add_key(key, value, append=True)
        elif op == '-':
            self.dic_add_key(key, value, prepend=True)

    def while_multi_line(self, line: str):
        """ Append line to self.dic[self._multiline_key] if line does
            not match END_MULTI_LINE.

            Raise from loader.exceptions:
                - SyntaxErrorPL if self._multiline_json is True, line match END_MULTI_LINE
                  and string consisting of all readed line is not a well formated json."""
        if self.END_MULTI_LINE.match(line):
            # [:-1] will remove last \n in a multiline value
            if self._multiline_op == '-=':
                # Modification de self._multiline_value[:-1] en self._multiline_value
                # Readfiles laisse les '\n', on passe sur un split du text
                self.dic_add_key(self._multiline_key, self._multiline_value[:-1], prepend=True)
            else:
                self.dic_add_key(self._multiline_key, self._multiline_value[:-1], append=True)
            
            if self._multiline_json:
                try:
                    d = self.dic
                    for k in self._multiline_key.split("."):
                        d = d[k]
                    self.dic_add_key(self._multiline_key, json.loads(d), replace=True)
                except json.decoder.JSONDecodeError:
                    raise SyntaxErrorPL(self.file_name,
                                        self.lines[self._multiline_opened_lineno - 1],
                                        self._multiline_opened_lineno,
                                        message="Invalid JSON syntax starting ")
            
            self._multiline_key = None
            self._multiline_op = None
            self._multiline_value = None
            self._multiline_json = False
        else:
            self._multiline_value += line
    
    def multi_line_match(self, match, line: str):
        """ Set self._multiline_key and self._multiline_opened_lineno.
            Also set self._multiline_json if operator is '=%'"""
        
        key = match.group('key')
        op = match.group('operator')
        
        self._multiline_key = key
        self._multiline_op = op
        self._multiline_value = ''
        self._multiline_opened_lineno = self.lineno
        if op == '%=':
            self._multiline_json = True
        
        if op != '+=' and op != '-=':  # Allow next lines to be concatenated
            self.dic_add_key(key, '')
    
    def component_line_match(self, match, line: str):
        """ Map value to a component.

            Raise from loader.exceptions:
                - SyntaxErrorPL if no group 'key' or 'component' was found
                - DirectoryNotFound if trying to load from a nonexistent directory
                - ComponentNotFound if component match.group("component") is not defined."""
        key = match.group('key')
        com = match.group('component')
        try:
            selector = SELECTORS[com]
            self.dic_add_key(key, {
                "cid":      str(uuid.uuid4()),
                "selector": selector
            })
        except KeyError:
            raise ComponentNotFound(com)
        except SyntaxError as e:
            raise SyntaxErrorPL(self.file_name, line, self.lineno, str(e))