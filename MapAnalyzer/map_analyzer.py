import re
import sys
import io
import abc
from dataclasses import dataclass, field
from os.path import split
from typing import ClassVar, List, Dict
from pprint import pprint


HW_SPACES = [
    dict(name='PFlash', min=0x01000000, max=0x01400000),
    dict(name='DTCM', min=0x20000000, max=0x20040000),
    dict(name='ITCM', min=0x00000000, max=0x00010000),
    dict(name='SRAM', min=0x20100000, max=0x20140000),
    dict(name='Unknown', min=0x00000000, max=0xffffffff+1),
]


def get_hw_addr(addr):
    for space in HW_SPACES:
        if space['min'] <= addr < space['max']:
            return space['name']


def warn(msg):
    print('[WARN]', msg)


@dataclass
class RecordBase:
    raw_content: str = ""
    virtual_addr: int = None
    load_addr: int = None
    size: int = None
    alignment: int = None


@dataclass
class RecordSymbol(RecordBase):
    symbol: str = ""


@dataclass
class RecordInputStatement(RecordBase):
    statement: str = ""


@dataclass
class RecordInputSection(RecordBase):
    section: str = ""
    object_file: str = None
    archive_file: str = None
    symbols: List[RecordSymbol] = field(default_factory=list)


@dataclass
class RecordOutputStatement(RecordBase):
    statement: str = ""


@dataclass
class RecordOutputSection(RecordBase):
    section: str = ""
    input_sections: List[RecordInputSection | RecordInputStatement] = field(
        default_factory=list)


@dataclass
class RecordDebugInfo(RecordBase):
    info: str = ""


@dataclass
class RecordUnknown(RecordBase):
    pass


class BaseMapAnalyzer(abc.ABC):
    def __init__(self, fp: io.TextIOWrapper):
        assert fp.readable() and fp.seekable(), \
            f'Invalid file "{fp.name}".'
        self.fp = fp
        self.fp.seek(0, io.SEEK_SET)
        assert self.is_valid_file(), \
            f'Content not matched in file "{fp.name}".'
        self.fp.seek(0, io.SEEK_SET)

        self.records: List[RecordBase] = []

    @abc.abstractmethod
    def is_valid_file(self) -> bool:
        return NotImplemented

    @abc.abstractmethod
    def resolve(self) -> List[RecordBase]:
        return NotImplemented


class ClangRecordLineResolver:
    REG_LINE = re.compile(r'(?P<virtual_addr>[0-9a-f ]{8,}?) '
                          r'(?P<load_addr>[0-9a-f ]{8,}?) '
                          r'(?P<size>[0-9a-f ]{8,}?) '
                          r'(?P<alignment>[0-9a-f ]{5,}?) '
                          r'(?P<raw_content>.*)')
    REG_CONTENTS = {
        RecordDebugInfo: re.compile(r"^(?P<info>\s*\.(?:debug_(?:loc|abbrev|info|ranges|str|frame|line)|comment|ARM\.attributes|symtab|shstrtab|strtab))"),
        RecordOutputStatement: re.compile(r'^(?=\S)(?P<statement>.+?=.+|(?:BYTE|SHORT|LONG|QUAD|SQUAD)\s*\(.+?\))'),
        RecordOutputSection: re.compile(r'^(?=\S)(?P<section>.+)'),
        RecordInputStatement: re.compile(r'^ {8}(?=\S)(?P<statement>.+?=.+|(?:BYTE|SHORT|LONG|QUAD|SQUAD)\s*\(.+?\))'),
        RecordInputSection: re.compile(r'^ {8}(?=\S)(?P<section>.+)'),
        RecordSymbol: re.compile(r'^ {16}(?=\S)(?P<symbol>.+)'),
        RecordUnknown: re.compile(r"^.+"),
    }

    @staticmethod
    def resolve(line):
        m = ClangRecordLineResolver.REG_LINE.match(line)
        assert m
        result = m.groupdict()
        result['virtual_addr'] = int(result['virtual_addr'], base=16)
        result['load_addr'] = int(result['load_addr'], base=16)
        result['size'] = int(result['size'], base=16)
        result['alignment'] = int(result['alignment'], base=16)

        for cls, reg in ClangRecordLineResolver.REG_CONTENTS.items():
            m_content = reg.match(result['raw_content'])
            if m_content:
                result.update(m_content.groupdict())
                break
        return cls(**result)


class ClangMapAnalyzer(BaseMapAnalyzer):
    def is_valid_file(self) -> bool:
        first_line = self.fp.readline()
        return first_line.startswith('     VMA')

    def resolve(self) -> List[RecordBase]:
        self.records = []
        first_line = self.fp.readline()
        # of = open("output.txt", 'w', encoding='utf8')
        for lineno, line in enumerate(self.fp.readlines(), start=2):
            resolve_result = ClangRecordLineResolver.resolve(line)
            # of.write(str(resolve_result)+'\n')

            if isinstance(resolve_result, RecordDebugInfo):
                break

            self.records.append(resolve_result)
            # if lineno > 100:
            #     break

        # of.close()
        return self.records


class GCCMapAnalyzer(BaseMapAnalyzer):
    def is_valid_file(self) -> bool:
        first_line = self.fp.readline()
        return first_line.startswith('Archive member')

    def resolve(self) -> List[RecordBase]:
        return NotImplemented


class MapAnalyzer:
    pass


def _temp_symbols_info(records: List[RecordBase]):

    symbols = [record for record in records if isinstance(
        record, RecordSymbol) and not record.symbol.startswith('$')]
    symbols = sorted(symbols, key=lambda r: r.symbol)
    return symbols


def map_symbols_diff(fn_list: List[str], output_file='map_diff.csv', with_address=False):
    group_by_symbols: Dict[str, List[RecordBase]] = dict()
    for fn_idx, fn in enumerate(fn_list):
        with open(fn, encoding='utf8') as f:
            a = ClangMapAnalyzer(f)
            symbols = [record for record in a.resolve() if isinstance(
                record, RecordSymbol) and not record.symbol.startswith('$')]
            # symbols = sorted(symbols, key=lambda r: r.symbol)
        for sym in symbols:
            symbol_list = group_by_symbols.setdefault(
                sym.symbol, [None] * fn_idx)
            symbol_list.append(sym)
    diff_symbols = []
    for sym_name, sym_list in group_by_symbols.items():
        sym_hw_addrs = [(get_hw_addr(sym.virtual_addr) if sym else None)
                        for sym in sym_list]
        if any(addr != sym_hw_addrs[0] for addr in sym_hw_addrs):
            diff_symbols.append(sym_name)
    print(diff_symbols)
    # Output diff file
    file_name_list = [split(fn)[-1] for fn in fn_list]
    with open(output_file, 'w', encoding='utf8') as f:
        # Header
        f.write("Symbol")
        f.write(''.join(f',Memory ({fn})' for fn in file_name_list))
        if with_address:
            f.write(''.join(f',Address ({fn})' for fn in file_name_list))
        f.write('\n')
        for diff_symbol in diff_symbols:
            sym_list = group_by_symbols[diff_symbol]
            f.write(diff_symbol)
            for sym in sym_list:
                f.write(f",{get_hw_addr(sym.virtual_addr)}")
            if with_address:
                for sym in sym_list:
                    f.write(f",0x{sym.virtual_addr:08X}")
            f.write('\n')


def gen_symbol_report(fn):
    with open(fn, encoding='utf8') as f:
        a = ClangMapAnalyzer(f)
        symbols = [record for record in a.resolve() if isinstance(
            record, RecordSymbol) and not record.symbol.startswith('$')]
        symbols = sorted(symbols, key=lambda r: r.symbol)

    with open(fn+'.symbols', 'w', encoding='utf8') as f:
        for sym in symbols:
            f.write(f'{sym.symbol:>40s} {get_hw_addr(sym.virtual_addr)}\n')


def main():
    map_symbols_diff([r'HTC_Playground_1.map', r'HTC_Playground_2.map'], with_address=True)
    # gen_symbol_report(r'HTC_Playground_1.map')
    # gen_symbol_report(r'HTC_Playground_2.map')

if __name__ == '__main__':
    main()
