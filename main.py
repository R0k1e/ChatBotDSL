import argparse
from Translater import Translater

parser = argparse.ArgumentParser(description='Interpret the given DSL program.')
parser.add_argument('--program_file', '-pf', type=str, default=None, help='Set the program file instead of stdin')
parser.add_argument('--save_parsed', '-sp', type=str, default=None, help='the file name to save parsed program')
parser.add_argument('--load_parsed', '-lp', type=str, default=None, help='the file name to load parsed program')
parser.add_argument('--save_file', '-sf', type=str, default=None, help='save variable list to file')
parser.add_argument('--save_from_key', '-sk', type=str, default=None, help='save variable list to vault from key')
parser.add_argument('--load_file', '-lf', type=str, default=None, help='load variable list from file')
parser.add_argument('--load_from_key', '-lk', type=str, default=None, help='load variable list from key')
parser.add_argument('--var_vault', '-vv', type=str, default='./var_vault/', help='set variable vault path')
parser.add_argument('--debug', '-d', action='store_true', help='debug mode')
parser.add_argument('--mode', '-m', type=str, default='std', choices=['std','file','web'], help='data resource mode, include std, file and web mode')
parser.add_argument('--input', '-i', type=str, default=None, help='input data file name, need to set mode to file')
parser.add_argument('--output', '-o', type=str, default=None, help='output data file name, need to set mode to file')
parser.add_argument('--url', '-u', type=str, default=None, help='set web url, need to set mode to web')


args = parser.parse_args()

if __name__ == '__main__':
    t = Translater(args)
    t.translate()
