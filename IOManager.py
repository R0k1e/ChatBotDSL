import requests
import pickle
import sys
import os
import json

from Parser import Parser

class IOManager:
    
    def __init__(self, args:any) -> None:
        self.__inFileName = args.input
        self.__outFileName = args.output
        self.__parseLoadFile = args.load_parsed
        self.__parseSaveFile = args.save_parsed
        self.__varSaveFile = args.save_file
        self.__varSaveKey = args.save_from_key
        self.__varLoadFile = args.load_file
        self.__varLoadKey = args.load_from_key
        self.__varVault = args.var_vault
        self.__progFile = args.program_file
        self.__url = args.url
        self.__isDebug = args.debug
        self.__mode = args.mode
        
        self.__outData = ""
        self.__parser = Parser()
        
        if self.__mode == 'file' and (self.__inFileName is None or self.__outFileName is None):
            print("Please input the input file name or the output file name in the argument")
            exit()
        if self.__mode == 'web' and self.__url is None:
            print("Please input the url in the argument")
            exit()
        
        if self.__mode != 'file' and (self.__inFileName is not None or self.__outFileName is not None):
            print("Hint: You may forget to set the mode. If you want to use the file mode, please set the mode to file. Current mode is ", self.__mode, ".")
            
        if self.__mode != 'web' and self.__url is not None:
            print("Hint: You may forget to set the mode. If you want to use the web mode, please set the mode to web. Current mode is ", self.__mode, ".")
        
        if self.__inFileName is not None:
            if self.__isDebug:
                print("Read input from file:", self.__inFileName)
            try:
                with open(self.__inFileName, "r") as f:
                    t = f.read()
            except Exception as e:
                print(e)
                print("Open input file failed, exit the program")
                exit()
            self.__inFileText = t.splitlines()
            for l in self.__inFileText:
                if l == '':
                    self.__inFileText.remove(l)
                else:
                    l = l.rstrip('\n')
            self.__inFileText = iter(self.__inFileText)
        else:
            if self.__isDebug:
                print("Read input from stdin")
                
        if os.path.exists(self.__varVault):
            if self.__isDebug:
                print("Variable vault path:", self.__varVault)
        else:
            os.makedirs(self.__varVault)
            if self.__isDebug:
                print("Create variable vault path:", self.__varVault)
                
        if os.path.exists(self.__outFileName):
            if self.__isDebug:
                print("Out file path:", self.__outFileName)
        else:
            with open(self.__outFileName, 'w') as f:
                pass
            if self.__isDebug:
                print("Create out file path:", self.__outFileName)
            
    def loadParsedStr(self) -> list:
        if self.__parseLoadFile is not None:
            if self.__isDebug:
                print("Load parsed string from file:", self.__parseLoadFile)
            try:
                with open(self.__parseLoadFile, 'rb') as f:
                    p = pickle.load(f)
            except Exception as e:
                print(e)
                print("Open parsed file failed, exit the program")
                exit()
                
        else:
            if self.__isDebug:
                print("No parsed string file, create a new one")
            s = self.getProgram()
            if self.__isDebug:
                print("Parsed string")
            p = self.__parser.grammarParse(s)
        return p

    def saveParsedStr(self, l:list) -> None:
        if self.__parseSaveFile is not None:
            if self.__isDebug:
                print("Save parsed string to file:", self.__parseSaveFile)
            try:
                with open(self.__parseSaveFile, 'wb') as f:
                    pickle.dump(l, f)
            except Exception as e:
                print(e)
                print("Open parsed file failed, exit the program")
                exit()
        else:
            if self.__isDebug:
                print("Not save parsed string to file")
            

    def getProgram(self) -> str:
        if self.__progFile is not None:
            if self.__isDebug:
                print("Program file:", self.__progFile)
            try:
                with open(self.__progFile, 'r', encoding='utf-8') as f:
                    p = f.read()
            except Exception as e:
                print("Open program file failed, exit the program")
                print(e)
                exit()
        else:
            print("Please input the code, end with Ctrl+Z on Windows or Ctrl-D on Unix-like system:")
            p = sys.stdin.read()
        return p
    
    def loadVarDict(self, key: str = None) -> dict:
        varDict = {}
        if key is not None:
            self.__varLoadFile = self.__findVarDict(key)
        elif self.__varLoadKey is not None:
            self.__varLoadFile = self.__findVarDict(self.__varLoadKey)
            
        if self.__varLoadFile is not None:
            if self.__isDebug:
                print("Load variable from file:", self.__varLoadFile)
            try:
                with open(self.__varLoadFile, 'r') as f:
                    varDict = json.loads(f.read())
            except Exception as e:
                print(e)
                print("Load var dict file failed, exit the program")
                exit()
        else :
            if self.__isDebug:
                print("No variable file, create a new dict")
            varDict = {}
            
        for name, value in varDict.items():
            if name[0] != '$':
                varDict['$' + name] = value
                del varDict[name]
        return varDict

    def saveVarDict(self, varDict: dict, key: str = None) -> None:
        if key is not None:
            self.__varSaveFile = self.__findVarDict(key)
        elif self.__varSaveKey is not None:
            self.__varSaveFile = self.__findVarDict(self.__varSaveKey)
        
        if self.__varSaveFile is not None:
            if self.__isDebug:
                print("Save variable to file:", self.__varSaveFile)
            try:
                with open(self.__varSaveFile, 'w') as f:
                    f.write(json.dumps(varDict))
            except Exception as e:
                print(e)
                print("Open var dict file failed, exit the program")
                exit()
        else:
            if self.__isDebug:
                print("Not save variable to file")      
                
    def __findVarDict(self, key: str) -> str:
        if key is not None:
            if self.__isDebug:
                print("Find var dict from key:", key)
            varPath = self.__varVault + 'var_' + key + '.json'
            if os.path.exists(varPath):
                if self.__isDebug:
                    print("Find the var dict file:", varPath)
            else:
                if self.__isDebug:
                    print("Not find the var dict file, create a new one:", varPath)
        else :
            if self.__isDebug:
                print("No key, return the none path")
            varPath = None
        return varPath
            
    def getInput(self) -> str: 
        try:
            if self.__mode == 'file':
                if self.__isDebug:
                    print("Read input from file")
                ipt = next(self.__inFileText)
                outData = "<<<" + ipt
                self.__outData += outData + '\n'
            elif self.__mode == 'web':
                if self.__isDebug:
                    print("Read input from web")
                r = requests.get(self.__url)
                if r.status_code == 200:
                    ipt = r.content.decode()
                else:
                    raise Exception('Load from url error:', r.status_code)
            elif self.__mode == 'std':
                if self.__isDebug:
                    print("Read input from stdin")
                print("<<<", end=' ')
                ipt = input()
        except Exception as e:
            print(e)
            print("get input error")
            exit()
            
        ipt = self.__parser.var.parseString(ipt)[0]
        return ipt
    
    def sendOutput(self, outData: str) -> None:
        try:
            if self.__mode == 'file':
                if self.__isDebug:
                    print("Send output to file")
                self.__outData += outData + '\n'
            elif self.__mode == 'web':
                if self.__isDebug:
                    print("Send output to web")
                r = requests.post(self.__url, data=outData)
                if r.status_code == 200:
                    if self.__isDebug:
                        print("Send output to web success")
                else:
                    print('Send to url error:', r.status_code)
            elif self.__mode == 'std':
                if self.__isDebug:
                    print("Send output to stdout")
                print(outData)
        except Exception as e:
            print(e)
            print("send output error")
            exit()
        
        
    
    def saveOutput(self) -> None:
        if self.__outFileName is not None:
            if self.__isDebug:
                print("Save in the output file:", self.__outFileName)
            if self.__outFileName is not None:
                try:
                    with open(self.__outFileName, 'w') as f:
                        f.write(self.__outData)
                except Exception as e:
                    print(e)
                    print("Open out file failed, exit the program")
                    exit()
        else:
            if self.__isDebug:
                print("Not save output to file")
                