import os, sys

import unittest

import platonparser.parsers.pl as pl
import platonparser.parser.parser_exceptions as exceptions
from platonparser.parser.utils import base_get_location, FullPath

class TestPLParser(unittest.TestCase):
    def setUp(self):
        self.dir = 'fake_pl/'

    def test_parse_general(self):
        path = os.path.join(self.dir, 'full.pl')
        with open(path, 'rb') as file: contents = file.read()
        parser = pl.PLParser(contents, FullPath(0, path), 0, base_get_location, check_mandatory_keys=False)
        output = parser.parse()
        # warning
        self.assertIn('Overwriting existing value at key "e.f.h"', output.warnings)
        # = += +
        self.assertEqual(output.data['title'], 'testtesttest')
         # = -= -
        self.assertEqual(output.data['title2'], 'AABBCC.')
        # ==
        self.assertEqual(output.data['text'], 'tests')
        # extends
        self.assertEqual(output.data['zzz'], 'zzz')
        # =@ +=@ -=@
        with open(os.path.join(self.dir, "working.pl")) as f:
            self.assertEqual(output.data['test'], 3 * f.read())
        # sub keys
        self.assertEqual(3, output.data['e']['f']['g'])
        # % %=
        self.assertEqual({'a': 1, 'b': 2}, output.data['e']['f']['i'])
        self.assertEqual({'a': 1, 'b': 2}, output.data['b'])
        # Override % with a.a
        self.assertEqual({'a': 3, 'b': 2}, output.data['a'])
        # @
        self.assertIn((base_get_location('builder/before.py', self.dir, 0, 0).path, 'builder.py'), output.dependencies)


    def test_json_from_file(self):
        path = os.path.join(self.dir, 'json_from_file.pl')
        with open(path, 'rb') as file:
            contents = file.read()
        parser = pl.PLParser(contents, FullPath(0, path), 0, base_get_location, check_mandatory_keys=False)
        output = parser.parse()
        self.assertEqual(69, output.data['json']['hello'])

    
    def test_multiline_eval(self):
        path = os.path.join(self.dir, 'multiline_eval.pl')
        with open(path, 'rb') as file:
            contents = file.read()
        parser = pl.PLParser(contents, FullPath(0, path), 0, base_get_location, check_mandatory_keys=False)
        output = parser.parse()
        self.assertEqual(3, output.data['eval']['b']['c'])
    

    @unittest.skip("feature not fully implemented in Platon")
    def test_parse_url(self):
        parser = pl.PLParser(os.path.join(self.dir, 'image.pl'), 0, 0, base_get_location, check_mandatory_keys=False)
        output = parser.parse()
    

    def test_parse_component(self):
        path = os.path.join(self.dir, 'component.pl')
        with open(path, 'rb') as file: contents = file.read()
        parser = pl.PLParser(contents, FullPath(0, path), 0, base_get_location, check_mandatory_keys=False)
        output = parser.parse()
        self.assertIn('form', output.data['formState'])

        path = os.path.join(self.dir, 'wrong_component.pl')
        with open(path, 'rb') as file: contents = file.read()
        with self.assertRaises(exceptions.ParserComponentNotFound):
            pl.PLParser(contents, FullPath(0, path), 0, base_get_location).parse()


    def test_mandatory_keys(self):
        with self.assertRaises(exceptions.ParserMissingKey):
            path = os.path.join(self.dir, 'no_author.pl')
            with open(path, 'rb') as file:
                contents = file.read()
            pl.PLParser(contents, FullPath(0, path), 0, base_get_location).parse()
        with self.assertRaises(exceptions.ParserMissingKey):
            path = os.path.join(self.dir, 'no_statement.pl')
            with open(path, 'rb') as file:
                contents = file.read()
            pl.PLParser(contents, FullPath(0, path), 0, base_get_location).parse()
        with self.assertRaises(exceptions.ParserMissingKey):
            path = os.path.join(self.dir, 'no_version.pl')
            with open(path, 'rb') as file:
                contents = file.read()
            pl.PLParser(contents, FullPath(0, path), 0, base_get_location).parse()
        with self.assertRaises(exceptions.ParserMissingKey):
            path = os.path.join(self.dir, 'no_title.pl')
            with open(path, 'rb') as file:
                contents = file.read()
            pl.PLParser(contents, FullPath(0, path), 0, base_get_location).parse()


    def test_inheritance_loop(self):
        path = os.path.join(self.dir, 'extend_loop_1.pl')
        with open(path, 'rb') as file:
            contents = file.read()
        with self.assertRaises(exceptions.ParserInheritanceLoopError):
            pl.PLParser(contents, FullPath(0, path), 0, base_get_location, check_mandatory_keys=False).parse()


    def test_parse_errors(self):
        with self.assertRaises(exceptions.ParserSemanticError):
            path = os.path.join(self.dir, "no_string_in_sub_key.pl")
            with open(path, 'rb') as file: contents = file.read()
            pl.PLParser(contents, FullPath(0, path), 0, 
                base_get_location, check_mandatory_keys=False).parse()
        with self.assertRaises(exceptions.ParserFileNotFound):
            path = os.path.join(self.dir, "syntax_file.pl")
            with open(path, 'rb') as file: contents = file.read()
            pl.PLParser(contents, FullPath(0, path), 0, 
                base_get_location, check_mandatory_keys=False).parse()
        with self.assertRaises(exceptions.ParserSyntaxError):
            path = os.path.join(self.dir, "syntax_error.pl")
            with open(path, 'rb') as file: contents = file.read()
            pl.PLParser(contents, FullPath(0, path), 0, 
                base_get_location, check_mandatory_keys=False).parse()
        with self.assertRaises(exceptions.ParserFileNotFound):
            path = os.path.join(self.dir, "extends_no_lib.pl")
            with open(path, 'rb') as file: contents = file.read()
            pl.PLParser(contents, FullPath(0, path), 0, 
                base_get_location, check_mandatory_keys=False).parse()
        with self.assertRaises(exceptions.ParserSyntaxError):
            path = os.path.join(self.dir, "open_multiline.pl")
            with open(path, 'rb') as file: contents = file.read()
            pl.PLParser(contents, FullPath(0, path), 0,
                base_get_location, check_mandatory_keys=False).parse()
        with self.assertRaises(exceptions.ParserSemanticError):
            path = os.path.join(self.dir, "append_no_key.pl")
            with open(path, 'rb') as file: contents = file.read()
            pl.PLParser(contents, FullPath(0, path), 0, 
                base_get_location, check_mandatory_keys=False).parse()
        with self.assertRaises(exceptions.ParserFileNotFound):
            path = os.path.join(self.dir, "no_file_from.pl")
            with open(path, 'rb') as file: contents = file.read()
            pl.PLParser(contents, FullPath(0, path), 0, 
                base_get_location, check_mandatory_keys=False).parse()
        with self.assertRaises(exceptions.ParserSyntaxError):
            path = os.path.join(self.dir, "invalid_one_line_json.pl")
            with open(path, 'rb') as file: contents = file.read()
            pl.PLParser(contents, FullPath(0, path), 0, 
                base_get_location, check_mandatory_keys=False).parse()
        with self.assertRaises(exceptions.ParserSyntaxError):
            path = os.path.join(self.dir, "invalid_multiline_json.pl")
            with open(path, 'rb') as file: contents = file.read()
            pl.PLParser(contents, FullPath(0, path), 0, 
                base_get_location, check_mandatory_keys=False).parse()
        with self.assertRaises(exceptions.ParserFileNotFound):
            path = os.path.join(self.dir, "no_file_sandbox.pl")
            with open(path, 'rb') as file: contents = file.read()
            pl.PLParser(contents, FullPath(0, path), 0, 
                base_get_location, check_mandatory_keys=False).parse()
        with self.assertRaises(exceptions.ParserFileNotFound):
            path = os.path.join(self.dir, "no_image.pl")
            with open(path, 'rb') as file: contents = file.read()
            pl.PLParser(contents, FullPath(0, path), 0, 
                base_get_location, check_mandatory_keys=False).parse()
        with self.assertRaises(exceptions.ParserSemanticError):
            path = os.path.join(self.dir, "prepend_no_key.pl")
            with open(path, 'rb') as file: contents = file.read()
            pl.PLParser(contents, FullPath(0, path), 0, 
                base_get_location, check_mandatory_keys=False).parse()


if __name__ == '__main__':
    unittest.main()