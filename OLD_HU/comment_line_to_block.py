#!python3
import re
import os
from shutil import rmtree
from os.path import join, split, dirname
import sys


OUTPUT = join(dirname(__file__), 'output')
REG_SPLIT = re.compile(r"[A-Z][\w\d]+_TS_TTA\d(?:HSM)?M\dI\dP\d[/\\]?")
REG_DOXYGEN_ONELINE = re.compile(
    r'(?<!!)///?<\s*(.+)[\t ]*\n'
)
REG_LINE = re.compile(
    r"(?<!/)(?<!\*)(?<!!)(?<!https:)(?<!http:)//(?![!/<])[ ]?(.+?)([\t ]+)?\n"
)


"""Comment converter: One-line comment to multiple lines. (Including doxygen-styled)"""

__author__ = 'Hu Xintao'
__date__ = '2023/05/15'
__version__ = '0.1.0'


def repl_one_file(file):
    print(f"[P] {file}")
    split_path = REG_SPLIT.split(file)
    if len(split_path) == 1:
        split_path = split(split_path[0])
    out_file = join(OUTPUT, split_path[-1])
    out_path = join(*(split(out_file)[:-1]))

    os.makedirs(out_path, exist_ok=True)
    with open(file, encoding='utf8') as f:
        content = f.read()

    with open(out_file, 'w', encoding='utf8') as of:
        content = REG_DOXYGEN_ONELINE.sub(
            lambda m: f"/*!< {m.group(1)} */\n", content)
        content = REG_LINE.sub(
            lambda m: f"/* {m.group(1).replace('*/', '* /')} */\n", content)
        of.write(content)


def path_iter(paths):
    for path in paths:
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if not (file.endswith('.c') or file.endswith('.h')):
                        continue
                    repl_one_file(os.path.join(root, file))
        elif os.path.isfile(path):
            repl_one_file(path)


def main():
    if os.path.exists(OUTPUT):
        rmtree(OUTPUT)
    if len(sys.argv) > 1:
        paths = sys.argv[1:]
    else:
        paths = [input('Paste your directory path here:\n> ').strip()]

    path_iter(paths)


if __name__ == '__main__':
    main()
