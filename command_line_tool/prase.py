from pprint import pprint
import argparse

parser = argparse.ArgumentParser(prog="map_checker")
parser.add_argument("paths", nargs="+", help="path list")
parser.add_argument("-v", "--verbose", help="verbose option", action="store_true")
parser.add_argument("-a", "--all", help="all option", action="store_true")
args = parser.parse_args()

if args.verbose:
    pprint(args)