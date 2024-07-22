from pyparsing import Group, Literal, Word, alphanums, nums, ZeroOrMore, Forward, Optional, \
    Suppress, oneOf, infixNotation, opAssoc, ParserElement, SkipTo, opAssoc, White, Combine
from string import printable

class Parser:
    def __init__(self):
        self.grammar = self.__get_grammar()

    def __get_grammar(self) -> ParserElement:
        # Define the basic sentence
        # function name must start with _
        funcName = Word("_" + alphanums)

        # variable name must start with $
        varName = Word("$" + alphanums)
        chars = alphanums + ",.:;?/'!@#$%^&*()-_=+[]{}|\\`~ "
        string = Group(Literal('"') + ZeroOrMore(Word(chars)) + Literal('"')) 
        number = Combine(Word(nums) + Optional("." + Word(nums)))
        var = number | varName | string 
        self.var = var

        operators = [
            (oneOf("* /"), 2, opAssoc.LEFT),    
            (oneOf("+ -"), 2, opAssoc.LEFT),
            (oneOf("=="), 2, opAssoc.LEFT),
            (oneOf("in &"), 2, opAssoc.LEFT),
        ]
        exp = infixNotation(var, operators) | var

        # each sentence should end with ;
        sentence = Forward()
        block = Group(Literal("{") + ZeroOrMore(sentence) + Literal("}"))

        # 11 basic sentences
        execute = Group(Literal("exec") + string + Literal(";"))
        func = Group(Literal("func") + funcName + block + Literal(";"))
        funcExecute = Group(funcName + Literal(";"))
        loop = Group(Literal("loop") + Word(nums) + Literal("times") + (funcName|block) + Literal(";"))
        condition = Group(Literal('if') + exp + Literal('then') + (funcName| block) +
               ZeroOrMore(Literal('elif') + exp + Literal('then') + (funcName|block)) +
               Optional(Literal('else') + (funcName|block)) + Literal(';'))
        assignment = Group(varName + Literal("=") + exp + Literal(";")) | \
                    Group(varName + Literal("=") + var + Literal(";"))
        get = Group(Literal("get") + varName + Literal(";"))
        send = Group(Literal("send") + exp + Literal(";"))
        load = Group(Literal("load") + var + Literal(";"))
        save = Group(Literal("save") + var + Literal(";"))
        exitSentence = Group(Literal("exit") + Literal(";"))

        commentStart = Literal(r'/*')
        commentEnd = Literal(r'*/')
        commentContent = SkipTo(commentEnd)
        comment = Suppress(ZeroOrMore(commentStart + commentContent + commentEnd))

        sentence << Optional(comment) + (loop | condition | assignment | get | send | func | execute | load | save | exitSentence | funcExecute) \
                + Optional(comment)

        grammar = block
        return grammar

    def grammarParse(self, string: str) -> list:
        """Split the raw string into a list by pyparsing
        Parameters
        ----------
        string : str
            The input raw string
            
        Returns
        -------
        List
            The splited input divided by the sentence
            
        Examples
        --------
        >>> p = Parser()
        >>> result = p.grammarParse('''{func _func1 {get $var1;};get $var1;}''')
        >>> print(result)
        
        ['{', ['func', '_func1', ['{', ['get', '$var1', ';'], '}']], ';', ['get', '$var1', ';'],  '}']
        """
        r = self.grammar.parseString(string)
        return r.asList()


if __name__ == "__main__":
    p = Parser()
    result = p.grammarParse('''{    
    if "enquiry" in $cmd then _find
        elif "complain" in $cmd then _complain
        elif "exit" in $cmd then _exit
        else {
            _test;
        };
    }''')
    print(result)
