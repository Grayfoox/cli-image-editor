#!/usr/bin/python

import sys
from argparse import ArgumentParser

from functions import read_image, percentage, save_image, action_dict

"""
parser setting
"""
parser: ArgumentParser = ArgumentParser()
parser.add_argument('--version', action='version', version='1.1_Sail')

parser.add_argument("--rotate", action='store_true', help="převrácení obrazu směrem doprava o 90°")
parser.add_argument("--mirror", action='store_true', help="zrcadlení")
parser.add_argument("--inverse", action='store_true', help="inverzní obraz (negativ)")
parser.add_argument("--bw", action='store_true', help="převod do odstínů šedi")
parser.add_argument("--lighten", type=percentage, const="0", nargs="?", action="append",
                    help="zesvětlení <percentage: 0-inf> ")
parser.add_argument("--darken", type=percentage, const="0", nargs="?", action="append",
                    help="ztmavení <percentage: 0-inf>")
parser.add_argument("--sharpen", action="store_true", help="zvýraznění hran (tzv. “unsharp mask”)")
parser.add_argument("--blur_3x3", action='store_true',
                    help="použije konvoluční metodu k gausovo rozmazání, POZOR: tento přepínač zabere čas")
parser.add_argument("--blur_5x5", action='store_true',
                    help="použije konvoluční metodu k gausovo rozmazání, \
                         avšak s větším okrajem POZOR: tento přepínač zabere čas")
parser.add_argument("--edge_detection", action='store_true',
                    help="použije konvoluční metodu k detekci a vykreselní hran POZOR: tento přepínač zabere čas")
parser.add_argument("--embossing", action='store_true',
                    help="použije konvoluční metodu k \"vyražení\" POZOR: tento přepínač zabere čas")
parser.add_argument("INPUT_FILE", help="Vstupni soubor na upravu (cestu k nemu)")
parser.add_argument("OUTPUT_FILE", help="Cesta k vystupu tohoto programu")
"""
------------
"""

queue = sys.argv[1:-2]  # slice pro poradi prepinacu
args = parser.parse_args()
np_image = None

try:
    np_image = read_image(args.INPUT_FILE)

except FileNotFoundError:
    print("Soubor nenalezen, ukoncuji")
    exit(1)
except Exception as ex:
    print("chyba", ex)
    exit(1)

for act in queue:
    try:
        np_image = action_dict[act](np_image, args)
    except KeyError:  # ciselne a nevalidni hodnoty muzeme preskocit
        pass
    except Exception as ex:
        print("chyba", ex)

save_image(np_image, args.OUTPUT_FILE)  # v pripade potreby soubor prepiseme
