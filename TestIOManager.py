import unittest
import argparse
import sys
import subprocess
import time
from IOManager import IOManager



class TestIOManager(unittest.TestCase):
    def setUp(self):
        args = argparse.Namespace()
        args.output = 'unittest/out.txt'
        args.input = 'unittest/in.txt'
        args.load_parsed = 'unittest/test_parsed_file.pkl'
        args.save_parsed = 'unittest/test_parsed_file.pkl'
        args.program_file = 'unittest/program.txt'
        args.load_file = 'unittest/var_peter.json'
        args.save_file = 'unittest/var_peter.json'
        args.url = 'http://localhost:8000/'
        args.save_from_key = None
        args.load_from_key = None
        args.var_vault = './var_vault/'
        args.debug = False
        args.mode = 'file'
        self.ioManager = IOManager(args)
        
    def test_getInputUrlAndSetInputUrl(self):
        #调试时可以正常输出，执行时stdout无法获取输出
        self.ioManager._IOManager__url = 'http://localhost:8000/'
        self.ioManager._IOManager__mode = 'web'
        self.web_stub_process = subprocess.Popen(['python', 'WebStub.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p = self.ioManager.getInput()
        t = self.ioManager._IOManager__parser.var.parseString('"GET"')[0] 
        plst = [p[0],p[1],p[2]]
        tlst = [t[0],t[1],t[2]]
        self.assertEqual(plst, tlst)
        self.ioManager.sendOutput("POST")
        time.sleep(3)
        self.web_stub_process.terminate()
        time.sleep(3)
        stdout, stderr = self.web_stub_process.communicate()
        stdout = stdout.decode('utf-8')
        if "POST" in stdout:
            stdout = "POST"
        self.assertEqual(stdout, 'POST')
        
    def test_loadParsedStr(self):
        self.ioManager._IOManager__parseLoadFile = 'unittest/test_parsed_file.pkl'
        p = self.ioManager.loadParsedStr()
        self.assertEqual(p, ['parsed', 'string'])
        
    def test_saveParsedStr(self):
        self.ioManager._IOManager__parseLoadFile = 'unittest/test_parsed_file.pkl'
        self.ioManager._IOManager__parseSaveFile = 'unittest/test_parsed_file.pkl'
        self.ioManager.saveParsedStr(['parsed', 'string'])
        p = self.ioManager.loadParsedStr()
        self.assertEqual(p, ['parsed', 'string'])
        
    def test_getProgramFile(self):
        self.ioManager._IOManager__progFile = 'unittest/program.txt'
        p = self.ioManager.getProgram()
        self.assertEqual(p, 'program')
    
    def test_loadVarDict(self):
        self.ioManager._IOManager__varLoadFile = 'unittest/var_peter.json'
        p = self.ioManager.loadVarDict()
        self.assertEqual(p, {'$a': 1,})
        
    def test_saveVarDict(self):
        self.ioManager._IOManager__varLoadFile = 'unittest/var_peter.json'
        self.ioManager._IOManager__varSaveFile = 'unittest/var_peter.json'
        self.ioManager.saveVarDict({'$a': 1, })
        p = self.ioManager.loadVarDict()
        self.assertEqual(p, {'$a': 1,})
        
    def test_getInputFile(self):
        self.ioManager._IOManager__mode = 'file'
        self.ioManager._IOManager__inFileName = 'unittest\in.txt'
        with open(self.ioManager._IOManager__inFileName, "r") as f:
            t = f.read()
            self.ioManager._IOManager__inFileText = iter(t.splitlines())
        ipt = self.ioManager.getInput()
        self.assertEqual(ipt, '123')
        
        
    def test_saveOutput(self):
        self.ioManager._IOManager__outFileName = 'unittest\out.txt'
        self.ioManager._IOManager__outData = '123'
        self.ioManager.saveOutput()
        with open('unittest\out.txt', 'r') as f:
            p = f.read()
        self.assertEqual(p, '123')
        
        
        
        
if __name__ == '__main__':
    unittest.main()