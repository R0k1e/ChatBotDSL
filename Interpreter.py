from typing import Union
import os
import subprocess

from Exception import FuncNotExistError, VarNotExistError, FuncDupError, SyntaxError, ExpressionError
from Parser import Parser
from IOManager import IOManager



class Interpreter:
    def __init__(self, ioManager: IOManager = None, isDebug: bool = False) -> None:
        self.__ioManager = ioManager
        self.__funcDict = dict()
        if IOManager is not None:
            self.__varDict = ioManager.loadVarDict()
        else:
            self.__varDict = dict()
        self.__isDebug = isDebug
        self.__exitFlag = False
        
    def _setIOManager(self, ioManager: IOManager) -> None:
        # use to inject IOManager in test, not used in user program
        self.__ioManager = ioManager
        if IOManager is not None:
            self.__varDict = ioManager.loadVarDict()
        else:
            self.__varDict = dict()

    def execute(self, result: list) -> None:
        """
        translate the splited string into program
        
        Parameters
        ----------
        result : list
            The list of input string splited by Parser
            
        Returns
        -------
        outData : str
            The output data string
            
        Examples
        --------
        >>> p = Parser()
        >>> result = p.grammarParse('''{func _func1 {get $var1;}; get $var1;}''')
        >>> i = Interpreter()
        >>> outData = i.execute(result)
        """

        result = result[0] # remove the first "{", func block not exist { and }
        try:
            self.__blockProc(result)
        except Exception as e:
            print("Error in initial function")
            exit()
            
        if "_main" in self.__funcDict:
            if self.__isDebug:
                print("Process main function")
            try:
                count = 0
                while self.__exitFlag == False and count < 1000:
                    count += 1
                    self.__blockProc(self.__funcDict["_main"])
                if count >= 1000:
                    raise Exception("Loop too many times")
            except Exception as e:
                print("Error in main function")
                print(e)
                exit()
                
        self.__exitFlag = False
        
        if "_final" in self.__funcDict:
            if self.__isDebug:
                print("Process final function")
            try:
                self.__blockProc(self.__funcDict["_final"])
            except Exception as e:
                print("Error in final function")
                exit()
            
        self.__ioManager.saveVarDict(self.__varDict)
        self.__ioManager.saveOutput()
        
        return
    

    def __blockProc(self, block: list) -> None:
        # block example:
        # { func _func1 {get $var1;}; get $var1; }
        # sentences = [["func", "_func1", ["{", ["get", "$var1", ";"], "}"]], ["get", "$var1", ";"]]
        
        if self.__isDebug:
            print("Process block:", str(block))
            if self.__exitFlag:
                print("As exit, skip")
                return

        # Remove the first and last "{", "}"
        sentences = block[1:-1]
        try:
            for s in sentences:
                if self.__isDebug:
                    print("Process Sentence:", str(s))
                    if self.__exitFlag:
                        print("As exit, skip")
                        return
                if s[0] == "func":  # function definition
                    self.__funcProc(s)
                elif s[0][0] == "_": # function execute
                    self.__funcExecuteProc(s)
                elif s[0] == "loop":
                    self.__loopProc(s)
                elif s[0] == "if":
                    self.__ifProc(s)
                elif s[0][0] == "$":  # assignment
                    self.__assignProc(s)
                elif s[0] == "get":
                    self.__getProc(s)
                elif s[0] == "send":
                    self.__sendProc(s)
                elif s[0] == "exec":
                    self.__execProc(s)
                elif s[0] == "load":
                    self.__loadProc(s)
                elif s[0] == "save":
                    self.__saveProc(s)
                elif s[0] == "exit":
                    self.__exitFlag = True
                    break
                else:
                    raise SyntaxError(s[0])
        except Exception as e:
            print("Error in sentence" + str(s))
            print(e)
            exit()
    
    def __funcExecuteProc(self, sentence: list) -> None:
        try:
            block = self.__funcDict[sentence[0]]
        except:
            raise FuncNotExistError(sentence[0])
        self.__blockProc(block)

    def __execProc(self, sentence: list) -> None:
        # exec sentence example:
        # exec "echo hello" ;
        # sentence[1] = "echo hello"

        cmd = self.__varProc(sentence[1])
        os.chdir(os.getcwd())
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = self.__varProc(result.stdout.decode())
        result = result.replace("\r", "")
        result = result[:-1]
        self.__ioManager.sendOutput(result)

    def __funcProc(self, sentence: list) -> None:
        # func sentence example:
        # func _func1 {get $var1;};
        # sentence[1] = "_func1"
        # sentence[2] = ["{", ["get", "$var1", ";"], "}"]
        
        funcName = sentence[1]
        funcBody = sentence[2]
        if funcName in self.__funcDict:
            raise FuncDupError(funcName)
        else:
            self.__funcDict[funcName] = funcBody

    def __loopProc(self, sentence: list) -> None:
        # loop sentence example:
        # loop 3 times _func1;
        # sentence[1] = "3"
        # sentence[3] = "_func1"
        # if timeNum = 0, then loop infinitely

        timeNum = int(sentence[1])
        funcName = sentence[3]
        if funcName[0] == "_": # func name
            if funcName in self.__funcDict:
                funcBody = self.__funcDict[funcName]
            else:
                raise FuncNotExistError(funcName)
        elif funcName[0] == "{": # block
            funcBody = funcName
        else:
            raise SyntaxError(funcName)
        
        assert timeNum >= 0
        for i in range(timeNum):
            self.__blockProc(funcBody)

    def __ifProc(self, sentence: list) -> None:
        # if sentence example:
        # if $a == $b then _func1 elif $a == $b then _func2 else _func3 ;
        # sentence[1] = "$a == $b"
        # sentence[3] = "_func1"
        # sentence[-1] = "_func3"
        
        procFlag = False

        expList = []
        funcList = []
        for i in range(3, len(sentence), 4): # the length of if A then B is 4
            expList.append(sentence[i-2])
            funcList.append(sentence[i ])
        if len(sentence) % 4 == 3: # else exist
            elseFunc = sentence[-2]
            
        for i in range(len(expList)):
            exp = expList[i]
            funcName = funcList[i]
            if funcName[0] == "_": # func name
                if funcName in self.__funcDict:
                    funcBody = self.__funcDict[funcName]
                else:
                    raise FuncNotExistError(funcName)
            elif funcName[0] == "{": # block
                funcBody = funcName
            else:
                raise SyntaxError(funcName)
            
            
            exp = self.__expProc(exp)
            
            if exp:
                procFlag = True
                self.__blockProc(funcBody)
                break
        
        if (not procFlag) and (elseFunc is not None):
            
            if elseFunc[0] == "_": # func name
                if elseFunc in self.__funcDict:
                    funcBody = self.__funcDict[elseFunc]
                else:
                    raise FuncNotExistError(elseFunc)
            elif elseFunc[0] == "{": # block
                funcBody = elseFunc
            else:
                raise SyntaxError(elseFunc)
            
            self.__blockProc(funcBody)


    def __assignProc(self, sentence: list) -> None:
        # assignment sentence example:
        # $var1 = 1 + 1;
        # sentence[0] = "$var1"
        # sentence[2] = ["1", "+", "1"]
    

        varName = sentence[0]
        if len(sentence[2]) >= 3:  # str or exp
            if sentence[2][0] == "\"":
                varValue = self.__varProc(sentence[2])
            else:
                varValue = self.__expProc(sentence[2])
        else:
            varValue = eval(sentence[2])

        self.__varDict[varName] = varValue

    def __getProc(self, sentence: list) -> None:
        # get sentence example:
        # get $var1;
        # sentence[1] = "$var1"


        varName = sentence[1]

        try:
            rawVar = self.__ioManager.getInput()
        except Exception as e:
            print(e)
            print("get input error, return empty string")
            rawVar = ''
        val = self.__varProc(rawVar)
        self.__varDict[varName] = val
    

    def __sendProc(self, sentence: list) -> None:
        # send sentence example:
        # send $var1;
        # sentence[1] = "$var1"

        exp = sentence[1]
        outData = str(self.__expProc(exp))
        self.__ioManager.sendOutput(outData)
            
    def __loadProc(self, sentence: list) -> None:
        key = self.__varProc(sentence[1])
        loadDict = self.__ioManager.loadVarDict(key)
        self.__varDict.update(loadDict)
        
    def __saveProc(self, sentence: list) -> None:
        key = self.__varProc(sentence[1])
        self.__ioManager.saveVarDict(self.__varDict, key)
        
    def __varProc(self, var: str) -> Union[str, int]:
        if self.__isDebug:
            print("Process var:", var)
        
            if self.__exitFlag:
                print("As exit, skip")
                return
            
        if var[0] == "$":
            if var in self.__varDict:
                return self.__varDict[var]
            else:
                raise VarNotExistError(var)
        else: 
            try: # num
                return eval(var)
            except: # str
                if var[0] != "\"" or var[-1] != "\"":
                    return var
                r = var[1]
                for i in var[2:-1]:
                    r += i
                return r

    def __expProc(self, exp: list) -> Union[str, int]:
        if self.__isDebug:
            print("Process exp:", str(exp))
            if self.__exitFlag:
                print("As exit, skip")
                return
        
        if (len(exp) == 1 or exp[0] == "\""):
            return self.__varProc(exp)
        elif exp[0] == "$":
            return self.__varProc(exp)
        elif "." in exp:
            return self.__varProc(exp)
        else:
            idx = 0
            val = self.__expProc(exp[0])
            while idx < len(exp) - 2:
                exp1 = val
                op = exp[idx + 1]
                exp2 = self.__expProc(exp[idx + 2])
                if isinstance(exp1, str) or isinstance(exp2, str):
                    if op == "==":
                        val = int(eval(exp1) == eval(exp2))
                    elif op == "&":
                        val = (str(exp1) + str(exp2))
                    elif op == "in":
                        val = (str(exp1) in str(exp2))
                    else:
                        raise ExpressionError(exp1, exp2, op)
                else:
                    if op == "+":
                        val = exp1 + exp2
                    elif op == "-":
                        val = exp1 - exp2
                    elif op == "*":
                        val = exp1 * exp2
                    elif op == "/":
                        val = exp1 / exp2
                    elif op == "==":
                        val = int(exp1 == exp2)
                    else:
                        raise ExpressionError(exp1, exp2, op)
                idx += 2 # move to next exp

            return val


if __name__ == '__main__':
    f = IOManager()
    t = Interpreter(None)
    p = Parser()
    result = p.grammarParse('''
                            {
                                 $a = "a" in "abc";
                            }''')
    print(result)
    t.execute(result)