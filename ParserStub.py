class ParserStub:
    def __init__(self):
        pass

    def grammarParse(self, string: str) -> list:
        result = ['{', ['func', 'func1', ['{', ['exec', '"print hello world";'], '}'], ';'], '}']
        # Return the parsed result
        return result