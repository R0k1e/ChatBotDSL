import unittest
from Parser import Parser

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_execute(self):
        result = self.parser.grammarParse('{exec "echo hello world";}')
        expected = [['{', ['exec', ['"', 'echo hello world', '"'], ';'], '}']]
        self.assertEqual(result, expected)

    def test_func(self):
        result = self.parser.grammarParse('''{func _myFunc {exec "echo hello world";};}''')
        expected = [['{', ['func', '_myFunc', ['{', ['exec', ['"', 'echo hello world', '"'], ';'], '}'], ';'], '}']]
        self.assertEqual(result, expected)

    def test_loop(self):
        result = self.parser.grammarParse('{loop 3 times _myFunc;}')
        expected = [['{', ['loop', '3', 'times', '_myFunc', ';'], '}']]
        self.assertEqual(result, expected)

    def test_condition(self):
        result = self.parser.grammarParse('{if $x == 5 then _myFunc elif $x == 6 then _myOtherFunc else _myThirdFunc;}')
        expected = [['{', ['if', ['$x', '==', '5'], 'then', '_myFunc', 'elif', ['$x', '==', '6'], 'then', '_myOtherFunc', 'else', '_myThirdFunc', ';'], '}']]
        self.assertEqual(result, expected)
        
    def test_condition2(self):
        result = self.parser.grammarParse('{if $x == 5 then _myFunc;}')
        expected = [['{', ['if', ['$x', '==', '5'], 'then', '_myFunc', ';'], '}']]
        self.assertEqual(result, expected)
        
    def test_condition3(self):
        result = self.parser.grammarParse('{if $x == 5 then _myFunc elif $x == 6 then _myOtherFunc;}')
        expected = [['{', ['if', ['$x', '==', '5'], 'then', '_myFunc', 'elif', ['$x', '==', '6'], 'then', '_myOtherFunc', ';'], '}']]
        self.assertEqual(result, expected)
        
    def test_condition4(self):
        result = self.parser.grammarParse('{if $x == 5 then _myFunc else _myOtherFunc;}')
        expected = [['{', ['if', ['$x', '==', '5'], 'then', '_myFunc', 'else', '_myOtherFunc', ';'], '}']]
        self.assertEqual(result, expected)

    def test_assignment(self):
        result = self.parser.grammarParse('{$x = 5 + 3;}')
        expected = [['{', ['$x', '=', ['5', '+', '3'], ';'], '}']]
        self.assertEqual(result, expected)
        
    def test_assignment2(self):
        result = self.parser.grammarParse('{$x = $y;}')
        expected = [['{', ['$x', '=', '$y', ';'], '}']]
        self.assertEqual(result, expected)
        
    def test_assignment3(self):
        result = self.parser.grammarParse('{$x = "hello world";}')
        expected = [['{', ['$x', '=', ['"', 'hello world', '"'], ';'], '}']]
        self.assertEqual(result, expected)
    
    def test_assignment4(self):
        result = self.parser.grammarParse('{$x = $y + 3;}')
        expected = [['{', ['$x', '=', ['$y', '+', '3'], ';'], '}']]
        self.assertEqual(result, expected)
    
    def test_assignment5(self):
        result = self.parser.grammarParse('{$x = $y * $z;}')
        expected = [['{', ['$x', '=', ['$y', '*', '$z'], ';'], '}']]
        self.assertEqual(result, expected)
    
    def test_assignment6(self):
        result = self.parser.grammarParse('{$x = $y == $z;}')
        expected = [['{', ['$x', '=', ['$y', '==', '$z'], ';'], '}']]
        self.assertEqual(result, expected)
    
    def test_assignment7(self):
        result = self.parser.grammarParse('{$x = "a" in $z;}')
        expected = [['{', ['$x', '=', [['"','a','"'], 'in', '$z'], ';'], '}']]
        self.assertEqual(result, expected)
        
    def test_assignment8(self):
        result = self.parser.grammarParse('{$x = $y * $z + 3 == 4;}')
        expected = [['{', ['$x', '=', [[['$y', '*', '$z'], '+', '3'], '==', '4'], ';'], '}']]
        self.assertEqual(result, expected)
        
    def test_assignment9(self):
        result = self.parser.grammarParse('{$x = $y * ($z + 3) == 4;}')
        expected = [['{', ['$x', '=', [['$y', '*', ['$z', '+', '3']], '==', '4'], ';'], '}']]
        self.assertEqual(result, expected)
    
        
    def test_get(self):
        result = self.parser.grammarParse('{get $x;}')
        expected = [['{', ['get', '$x', ';'], '}']]
        self.assertEqual(result, expected)

    def test_send(self):
        result = self.parser.grammarParse('{send $x;}')
        expected = [['{', ['send', '$x', ';'], '}']]
        self.assertEqual(result, expected)

    def test_exit(self):
        result = self.parser.grammarParse('{exit;}')
        expected = [['{', ['exit', ';'], '}']]
        self.assertEqual(result, expected)
        
    def test_comment(self):
        result = self.parser.grammarParse('''{/*comment*/get $a;}''')
        expected = [['{', ['get', '$a', ';'], '}']]
        self.assertEqual(result, expected)
    
    def test_comment2(self):
        result = self.parser.grammarParse('''{get $a;/*comment*/}''')
        expected = [['{', ['get', '$a', ';'], '}']]
        self.assertEqual(result, expected)
        
    def test_comment3(self):
        result = self.parser.grammarParse('''{/*comm
                                          ent*/get $a;/*comm
                                          ent*/}''')
        expected = [['{', ['get', '$a', ';'], '}']]
        self.assertEqual(result, expected)
        
if __name__ == '__main__':
    unittest.main()