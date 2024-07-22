import sys
import requests

from Parser import Parser
from Interpreter import Interpreter
from IOManager import IOManager


class Translater:
    def __init__(self, args):
        self.__isDebug = args.debug
        self.__IOManager = IOManager(args)
        self.__interpreter = Interpreter(self.__IOManager, self.__isDebug)
        
    def translate(self) -> None:
        """
        Translate the raw string into program

        Parameters
        ----------
        No parameters

        Returns
        -------
        No return value
        
        Args
        ----
        '--program_file', '-pf', type=str, default=None, help='Set the program file instead of stdin'
        '--save_parsed', '-sp', type=str, default=None, help='the file name to save parsed program'
        '--load_parsed', '-lp', type=str, default=None, help='the file name to load parsed program'
        '--save_file', '-sf', type=str, default=None, help='save variable list to file'
        '--save_from_key', '-sk', type=str, default=None, help='save variable list to vault from key'
        '--load_file', '-lf', type=str, default=None, help='load variable list from file'
        '--load_from_key', '-lk', type=str, default=None, help='load variable list from key'
        '--var_vault', '-vv', type=str, default='./var_vault/', help='set variable vault path'
        '--debug', '-d', action='store_true', help='debug mode'
        '--mode', '-m', type=str, default='std', choices=['std','file','web'], help='data resource mode, include std, file and web mode'
        '--input', '-i', type=str, default=None, help='input data file name, need to set mode to file'
        '--output', '-o', type=str, default=None, help='output data file name, need to set mode to file'
        '--url', '-u', type=str, default=None, help='set web url, need to set mode to web'

        Examples
        --------
        >>> t = Translater(args)
        >>> t.translate()
        """
        
        if self.__isDebug:
            print("Debug mode")

        parsedStr = self.__IOManager.loadParsedStr()

        if self.__isDebug:
            print("Parsed string:")
            print(parsedStr)
            
        self.__IOManager.saveParsedStr(parsedStr)
        self.__interpreter.execute(parsedStr)
        return