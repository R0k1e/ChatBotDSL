from IOManager import IOManager


class IOManagerStub(IOManager):
    def loadParsedStr(self) -> list:
        l = [['{',
              ['if', ['a', '==', 'b'], 'then', '_func1', 'elif', ['a', '==', 'b'], 'then', '_func2', 'else', '_func3',
               ';'], '}']]
        return l

    def saveParsedStr(self, l: list) -> None:
        print("Stub save parsed string to file:", self.__parseSaveFile)

    def getProgram(self) -> str:
        return "Simulated program"

    def loadVarDict(self, key: str = None):
        return {"$var1": "test"}

    def saveVarDict(self, varDict: dict, key: str = None) -> None:
        print("Stub save variable dictionary to file:", self.__varSaveFile)

    def getInput(self) -> str:
        return "1"

    def saveOutput(self) -> None:
        print("Stub save output data to file:", self.__outFileName)


if __name__ == "__main__":
    args = None
    f = IOManagerStub(args)
    print(f.loadParsedStr())
    print(f.loadVarDict())