import re
import sys
from os.path import split
from typing import ClassVar
import dataclasses

FILTER_RULES = [
    re.compile(r'.+?:\(.+?\)'),   # all segments
    lambda n: '.debug' not in n,  # remove rule
    lambda n: '.ARM.' not in n,  # remove rule
    lambda n: '<internal>' not in n,  # remove rule
    ]

GROUPING = True
GROUPING_PRINT_ARCHIVE = True
GROUPING_PRINT_OBJECT = False
GROUPING_PRINT_DETAILS = False

HEX = True

def fmt_int(val, as_hex=False):
    if as_hex:
        return hex(val)[2:]
    else:
        return str(val)
    
# @dataclasses.dataclass(frozen=True)
# class EntrySymbol:
#     REG_SYM_SEGMENT: ClassVar[re.Pattern] = re.compile(r'(?P<segment>\.\S+)$')

@dataclasses.dataclass(frozen=True)
class EntryLine:
    REG_LINE: ClassVar[re.Pattern] = re.compile(
        r'^\s*(?P<addr_target>\S+)\s*(?P<addr_flash>\S+)\s*(?P<size>\S+)\s*(?P<align>\S+)\s*(?P<desc>.+)\s*$')

    desc: str
    addr_target: int
    addr_flash: int
    size: int
    align: int
    
    @staticmethod
    def resolve(line_str):
        entry = EntryLine.REG_LINE.match(line_str)
        if entry:
            return EntryLine(**entry.groupdict())
        else:
            return None

    def __repr__(self) -> str:
        fields = dataclasses.fields(self)
        field_str = ', '.join(f'{f.name}={getattr(self, f.name)!r}' for f in fields)
        return f"{self.__class__.__name__}({field_str})"
    
    def __str__(self) -> str:
        if HEX:
            return f'{self.addr_target:08x}  {self.size:8x}  {self.desc}'
        else:
            return f'{self.addr_target:8d}  {self.size:8d}  {self.desc}'

    def __post_init__(self):
        object.__setattr__(self, "addr_target", int(self.addr_target, base=16))
        object.__setattr__(self, "addr_flash", int(self.addr_flash, base=16))
        object.__setattr__(self, "size", int(self.size, base=16))
        object.__setattr__(self, "align", int(self.align, base=16))
        object.__setattr__(self, "desc", self.desc.strip())
        

def read_map(map_fn):
    all_entries = []
    with open(map_fn, encoding='utf8') as f:
        for line in f.readlines():
            try:
                e = EntryLine.resolve(line)
            except:
                continue
            if e:
                all_entries.append(e)
    for rule in FILTER_RULES:
        if callable(rule):
            all_entries = list(filter(lambda e: rule(e.desc), all_entries))
        elif isinstance(rule, re.Pattern):
            all_entries = list(filter(lambda e: rule.match(e.desc), all_entries))
        elif isinstance(rule, str):
            all_entries = list(filter(lambda e: rule in e.desc, all_entries))
        else:
            raise RuntimeError('Rule not support')
    
    return all_entries
    

def size_fmt(val):
    if val > 1000:
        return f'{val/1024:.2f}k'
    else:
        return str(val)
    

def report_addr_hist(fn, addr_min, addr_max, tag=None):
    result_report_str = ''
    entries = read_map(fn)
    entries = sorted(entries, key=lambda e: e.size, reverse=True)
    if not GROUPING:
        for e in entries:
            print(e)
    else:
        all_entries_map = dict()
        all_entries_list = list()
        for e in entries:
            if ":(" not in e.desc:
                continue
            if not addr_min <= e.addr_target <= addr_max:
                continue
            name, section = e.desc.split(':(')
            section = section[:-1]
            if name.endswith(')'):
                name = split(name)[-1]
                archive, obj = name.split('(')
                obj = obj[:-1]
            else:
                archive = None
                obj = split(name)[-1]
            archives = all_entries_map.setdefault(archive, dict())
            objects = archives.setdefault(obj, dict())
            sections = objects.setdefault(section, list())
            sections.append(e)
            all_entries_list.append((archive, obj, section, e))
            # print(e)
        
        n_entries = 0
        total_size = sum(e.size for _, _, _, e in all_entries_list)
        if tag:
            result_report_str += f'**** {tag} [size={size_fmt(total_size)}, 0x{hex(addr_min)[2:].zfill(8)} ~ 0x{hex(addr_max)[2:].zfill(8)}] ****\n'
        for archive, objects in all_entries_map.items():
            archive_size = sum(e.size for a, _, _, e in all_entries_list if a == archive)
            if GROUPING_PRINT_ARCHIVE: 
                result_report_str += f"  [{size_fmt(archive_size):10s}]  {archive}\n"
            for obj, sections in objects.items():
                obj_size = sum(e.size for a, o, _, e in all_entries_list if a == archive and o == obj)
                if GROUPING_PRINT_OBJECT:
                    result_report_str += f"    > [{size_fmt(obj_size)}]  {obj}\n"
                for ens in sections.values():
                    for e in ens:
                        if GROUPING_PRINT_DETAILS:
                            result_report_str += f"        [{size_fmt(e.size)}] {e.desc.split(':(')[-1][:-1]}\n"
                        n_entries += 1
        
    result_report_str += f'Total amount of filtered entries: {n_entries}\n'
    return result_report_str

def save_report(fn, out_fn='report.txt'):
    report = ''
    report += report_addr_hist(fn, 0x01000000, 0x01400000-1, 'PFlash')
    report += report_addr_hist(fn, 0x20000000, 0x20040000-1, 'DTCM')
    report += report_addr_hist(fn, 0x00000000, 0x00010000-1, 'ITCM')
    report += report_addr_hist(fn, 0x20100000, 0x20140000-1, 'SRAM')
    out_fn 
    if out_fn:
        with open(out_fn, 'w', encoding='utf8') as f:
            f.write(report)
    else:
        print(report)


if __name__ == '__main__':
    # fn = sys.argv[1]
    fn = r'D:\Projects\A8V2SITProjects\LinkerPlayground\HTC_LinkerPlayground\debug\HTC_LinkerPlayground.map'
    save_report(fn, "report_1_archive.txt")
    GROUPING_PRINT_OBJECT = True
    save_report(fn, "report_2_object.txt")
    GROUPING_PRINT_DETAILS = True
    save_report(fn, "report_3_detail.txt")
    
    # for e in all_entries_list:
    #     print(e)