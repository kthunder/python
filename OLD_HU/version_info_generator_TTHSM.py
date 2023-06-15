# 1. Install Python 3.10+
# 2. Run CMD.exe as Administrator, and run the commands below:
#    pip install -U --force-reinstall git+https://gitee.com/hxt-tg/tglib.git
#    pip install Jinja2
import sys
import re
import os
import io
import warnings
from os.path import join
from tglib.path import PathIterator
from jinja2 import Template
from typing import ClassVar, List, Set, TypeVar, Any
from dataclasses import dataclass
from shutil import rmtree


CONF = dict(
    module=dict(
        NAME='Fls',
        VENDOR_ID=1541,
        MODULE_ID=92,
        INSTANCE_ID=None,
        AR_RELEASE_MAJOR_VERSION=4,
        AR_RELEASE_MINOR_VERSION=4,
        AR_RELEASE_PATCH_VERSION=0,
        SW_MAJOR_VERSION=1,
        SW_MINOR_VERSION=1,
        SW_PATCH_VERSION=0,
    ),
    env=dict(
        CONTAIN_INSTANCE_ID=False,
        OUTPUT_DIR='version_output',
        OUTPUT_EXT='.txt',
        FILE_ENCODING='utf8',
        INSERT_CHECK_AFERT_VERSION_IF_NOT_FOUND_INSERTION=True,
        SKIP_SIMPLE_AUTOSAR=False,
        VERBOSE=True,
    )
)

# Base: 218
# Crc: 201
# Crypto: None
# Fls: 92
# Mcl: 224
# Mcu: 101
# Platform: 219
# Timer: 228
# Uart: 227


class IgnoreRule:
    SKIP_HEADERS: ClassVar[Set[str]] = set([
        'stdio.h',
        'stdlib.h',
        'stdint.h',
        'stdbool.h',
        'stddef.h',
        'string.h'
    ])
    SKIP_VERSION: ClassVar[Set[str]] = set([
        'A8V2HSM_CORE.h',
        'A8V2HSM_IRQ.h',
        'TT_BasicTypes.h',
        # 'TT_Devassert.h',
        # 'TT_DrvError.h',
        'TT_MemIf.h',
        'TT_PlatformTypes.h',
        'TT_StandardTypes.h',
    ])
    SKIP_CHECK: ClassVar[Set[str]] = set([
        'Std_Type.h',
    ])
    SKIP_MODULE_LINE: ClassVar[Set[str]] = set([
        # Crypto files
        # 'Aes_Drv.h',
        # 'Crypto_Hw_Ecc.h',
        # 'Crypto_Hw_Ecdsa.h',
        # 'Crypto_Hw_Hash.h',
        # 'Crypto_Hw_Mc.h',
        # 'Crypto_Hw_Rsa.h',
        # 'Crypto_Hw_SecurityCpy.h',
        # 'Crypto_Hw_Ska.h',
        # 'Crypto_Hw_Sm2.h',
        # 'Crypto_Hw_Sm4.h',
        # 'Crypto_Hw_Trng.h',
        # 'Crypto_Hw_Type.h',
        # 'Des_Drv.h',
        # 'Ecc_Drv.h',
        # 'Ecdsa_Drv.h',
        # 'Rsa_Drv.h',
        # 'Sha256_Drv.h',
        # 'Sm2_Drv.h',
        # 'Sm3_Drv.h',
        # 'Sm4_Drv.h',
        # 'Trng_Drv.h',
    ])

    @staticmethod
    def skip_header(fn):
        if fn is None:
            return True
        if 'MemMap' in fn:
            return True
        if '[' in fn or '$' in fn:
            return True
        if fn in IgnoreRule.SKIP_HEADERS:
            return True
        return False

    @staticmethod
    def skip_version(fn):
        if fn in IgnoreRule.SKIP_VERSION:
            return True
        if 'MemIf' in fn:
            return True
        if 'MemMap' in fn:
            return True
        return False

    @staticmethod
    def skip_check(fn):
        if fn in IgnoreRule.SKIP_CHECK:
            return True
        return False

    @staticmethod
    def skip_module_line(fn):
        if fn in IgnoreRule.SKIP_MODULE_LINE:
            return True
        if fn.startswith('TT'):
            return True
        if fn.startswith('A8V2') or fn.startswith('A8V2HSM'):
            return True
        return False


@dataclass
class CMacroToken:
    REG_HEADER: ClassVar[re.Pattern] \
        = re.compile(r'(?P<br1>")?(?(br1)|(?P<br2><))(?P<header>.+)(?(br2)>|").*$')
    mark: str = '#'
    op: str = None
    spaces: str = ''
    param: str = ''

    @property
    def header(self):
        if self.op != 'include':
            return None
        m = CMacroToken.REG_HEADER.match(self.param)
        if not bool(m):
            return None
        header = m.group('header')
        if IgnoreRule.skip_header(header):
            return None
        return header

    def __repr__(self) -> str:
        s = f"{self.op}"
        if self.op == 'include':
            s += f'({self.header})'
        return s

    def __str__(self) -> str:
        return f"{self.mark}{self.op}{self.spaces}{self.param}"


class PreprocessorTokenizer:
    """Tokenizer for C preprocessor grammar.

    Raises:
        TypeError: _description_
    """
    REG_TOKEN = re.compile(
        r'\s*(?P<mark>\#)(?P<op>\w+)(?P<spaces>[ \t\r\f\v]*)(?P<param>(?:[\s\S]*?(?:\\\s*)?)*?)(?:\n|$|//)')
    REG_TOKEN_TT = re.compile(
        r'\s*(?P<mark>\$\{mark\})(?P<op>\w+)(?P<spaces>[ \t\r\f\v]*)(?P<param>(?:[\s\S]*?(?:\\\s*)?)*?)(?:\n|$|//)')
    KEY_TOKEN_OP_LIST = ['if', 'ifdef', 'ifndef',
                         'else', 'elif', 'endif', 'include']

    def __init__(self, f: str | io.TextIOWrapper) -> None:
        if isinstance(f, str):
            # Assume file path
            with open(f, encoding=CONF['env']['FILE_ENCODING']) as fp:
                self.tokens = self._tokenize(fp)
        elif isinstance(f, io.TextIOWrapper):
            # Opened text file
            self.tokens = self._tokenize(f)
        else:
            raise TypeError("Only support file path or a opened text file.")

    def _tokenize(self, io_obj: io.TextIOWrapper) -> List[CMacroToken]:
        token_list = []
        with io_obj as f:
            file_content = f.read()

            if '${mark}' in file_content:
                reg = PreprocessorTokenizer.REG_TOKEN_TT
            else:
                reg = PreprocessorTokenizer.REG_TOKEN
            matches = list(reg.finditer(file_content))
            for m in matches:
                token_list.append(CMacroToken(**m.groupdict()))
        return token_list

    def key_tokens(self):
        for tk in self.tokens:
            if tk.op in PreprocessorTokenizer.KEY_TOKEN_OP_LIST:
                # Skip invalid headers and version-skipped headers
                if tk.op == 'include' and (
                    not bool(tk.header)
                    or IgnoreRule.skip_version(tk.header)
                    or IgnoreRule.skip_check(tk.header)
                ):
                    continue
                yield tk


class SourceFile:
    REG_DRV = re.compile(r'[A-Z][a-z]+_TS_TTA8(?:HSM)?M\dI\dP\d')
    REG_GEN = re.compile(r'(generate[\\/]|generate_TT[\\/])')

    def __init__(self, full_path):
        self.path = full_path

        found_patterns = SourceFile.REG_DRV.findall(full_path)
        if not found_patterns:
            found_pattern = None
            self.inner_path = ''
            warnings.warn(f'Not in a standard plugin path: "{full_path}".')
        else:
            found_pattern = found_patterns[-1]
            root = os.path.join(*os.path.split(full_path)[:-1])
            self.inner_path = root.split(found_pattern)[-1][1:]

        self.fn_prefix = CONF['module']['NAME'].upper()+'___' +\
            self.inner_path.replace('\\', '_').replace('/', '_')
        self.file_name = os.path.split(full_path)[-1]
        self.output_fn = join(
            CONF['env']['OUTPUT_DIR'], 'patches',
            f"{self.fn_prefix}___{self.file_name}{CONF['env']['OUTPUT_EXT']}")

        found_gen = SourceFile.REG_GEN.findall(self.inner_path)
        if not found_gen:
            self.type = None
        else:
            self.type = 'TT' if found_gen[-1].startswith(
                'generate_TT') else 'EB'

    @staticmethod
    def iter_path(path_list=None):
        file_ext = ['.c', '.h']
        if path_list is None:
            path_list = sys.argv[1:]

        for root, file_name in PathIterator(
                path_list,
                filter_file_extensions=file_ext,
                verbose=CONF['env']['VERBOSE'],
                raise_not_found=False,
                yield_dir=False):
            yield root, file_name

    def __str__(self) -> str:
        return self.path


class VersionInfoRender:
    _TM_SETTINGS = dict(
        trim_blocks=True,
        lstrip_blocks=True
    )

    TM = dict(
        VERSION=Template(r"""
/******************************************************************************
*                       Source File Version Information
******************************************************************************/
{% set mark = '#' %}
{% set VENDOR_ID = module.VENDOR_ID %}
{% set MODULE_ID = module.MODULE_ID %}
{% set INSTANCE_ID = module.INSTANCE_ID %}
{% set AR_RELEASE_MAJOR_VERSION = module.AR_RELEASE_MAJOR_VERSION %}
{% set AR_RELEASE_MINOR_VERSION = module.AR_RELEASE_MINOR_VERSION %}
{% set AR_RELEASE_PATCH_VERSION = module.AR_RELEASE_PATCH_VERSION %}
{% set SW_MAJOR_VERSION = module.SW_MAJOR_VERSION %}
{% set SW_MINOR_VERSION = module.SW_MINOR_VERSION %}
{% set SW_PATCH_VERSION = module.SW_PATCH_VERSION %}
{% if type == 'EB' %}
    {% set VENDOR_ID = '[!"num:inttohex(CommonPublishedInformation/VendorId)"!]' %}
    {% set MODULE_ID = '[!"CommonPublishedInformation/ModuleId"!]' %}
    {% set INSTANCE_ID = '0' %}
    {% set AR_RELEASE_MAJOR_VERSION = '[!"CommonPublishedInformation/ArMajorVersion"!]' %}
    {% set AR_RELEASE_MINOR_VERSION = '[!"CommonPublishedInformation/ArMinorVersion"!]' %}
    {% set AR_RELEASE_PATCH_VERSION = '[!"CommonPublishedInformation/ArPatchVersion"!]' %}
    {% set SW_MAJOR_VERSION = '[!"CommonPublishedInformation/SwMajorVersion"!]' %}
    {% set SW_MINOR_VERSION = '[!"CommonPublishedInformation/SwMinorVersion"!]' %}
    {% set SW_PATCH_VERSION = '[!"CommonPublishedInformation/SwPatchVersion"!]' %}
{% elif type == 'TT' %}
    {% set mark = '${mark}' %}
    {% set VENDOR_ID = '(${' ~ module.NAME ~ '.VendorId}U)' %}
    {% set MODULE_ID = '(${' ~ module.NAME ~ '.ModuleId}U)' %}
    {% set INSTANCE_ID = '(${' ~ module.NAME ~ '.InstanceId}U)' %}
    {% set AR_RELEASE_MAJOR_VERSION = '(${' ~ module.NAME ~ '.ArMajorVersion}U)' %}
    {% set AR_RELEASE_MINOR_VERSION = '(${' ~ module.NAME ~ '.ArMinorVersion}U)' %}
    {% set AR_RELEASE_PATCH_VERSION = '(${' ~ module.NAME ~ '.ArPatchVersion}U)' %}
    {% set SW_MAJOR_VERSION = '(${' ~ module.NAME ~ '.SwMajorVersion}U)' %}
    {% set SW_MINOR_VERSION = '(${' ~ module.NAME ~ '.SwMinorVersion}U)' %}
    {% set SW_PATCH_VERSION = '(${' ~ module.NAME ~ '.SwPatchVersion}U)' %}
{% endif %}
{{ mark }}define {{ this.name }}_VENDOR_ID_{{ this.fmt }}                     {{ VENDOR_ID }}
{% if module.MODULE_ID is not none and this.has_module %}
{{ mark }}define {{ this.name }}_MODULE_ID_{{ this.fmt }}                     {{ MODULE_ID }}
{% endif %}
{% if module.INSTANCE_ID is not none and this.type is not none and this.fmt == 'H' %}
{{ mark }}define {{ this.name }}_INSTANCE_ID_{{ this.fmt }}                   {{ INSTANCE_ID }}
{% endif %}
{{ mark }}define {{ this.name }}_AR_RELEASE_MAJOR_VERSION_{{ this.fmt }}      {{ AR_RELEASE_MAJOR_VERSION }}
{{ mark }}define {{ this.name }}_AR_RELEASE_MINOR_VERSION_{{ this.fmt }}      {{ AR_RELEASE_MINOR_VERSION }}
{{ mark }}define {{ this.name }}_AR_RELEASE_PATCH_VERSION_{{ this.fmt }}      {{ AR_RELEASE_PATCH_VERSION }}
{{ mark }}define {{ this.name }}_SW_MAJOR_VERSION_{{ this.fmt }}              {{ SW_MAJOR_VERSION }}
{{ mark }}define {{ this.name }}_SW_MINOR_VERSION_{{ this.fmt }}              {{ SW_MINOR_VERSION }}
{{ mark }}define {{ this.name }}_SW_PATCH_VERSION_{{ this.fmt }}              {{ SW_PATCH_VERSION }}
""".lstrip(), **_TM_SETTINGS),
        CHECK_HEADER=Template(r"""
/******************************************************************************
*                       File Version Checks
******************************************************************************/
""".lstrip(), **_TM_SETTINGS),
        CHECK=Template(r"""
{% set mark = '#' %}
{% if type == 'TT' %}
    {% set mark = '${mark}' %}
{% endif %}
/* {{ this.fn }} and {{ that.fn }} file version check */
{{ mark }}if ({{ this.name }}_VENDOR_ID_{{ this.fmt }} != {{ that.name }}_VENDOR_ID_{{ that.fmt }})
    {{ mark }}error "{{ this.fn }} and {{ that.fn }} have different vendor ids"
{{ mark }}endif
{% if module.MODULE_ID is not none and this.has_module and that.has_module %}
{{ mark }}if ({{ this.name }}_MODULE_ID_{{ this.fmt }} != {{ that.name }}_MODULE_ID_{{ that.fmt }})
    {{ mark }}error "{{ this.fn }} and {{ that.fn }} have different module ids"
{{ mark }}endif
{% endif %}
{{ mark }}if (({{ this.name }}_AR_RELEASE_MAJOR_VERSION_{{ this.fmt }} != {{ that.name }}_AR_RELEASE_MAJOR_VERSION_{{ that.fmt }}) || \
     ({{ this.name }}_AR_RELEASE_MINOR_VERSION_{{ this.fmt }} != {{ that.name }}_AR_RELEASE_MINOR_VERSION_{{ that.fmt }}) || \
     ({{ this.name }}_AR_RELEASE_PATCH_VERSION_{{ this.fmt }} != {{ that.name }}_AR_RELEASE_PATCH_VERSION_{{ that.fmt }}))
    {{ mark }}error "AutoSar Version Numbers of {{ this.fn }} and {{ that.fn }} are different"
{{ mark }}endif
{{ mark }}if (({{ this.name }}_SW_MAJOR_VERSION_{{ this.fmt }} != {{ that.name }}_SW_MAJOR_VERSION_{{ that.fmt }}) || \
     ({{ this.name }}_SW_MINOR_VERSION_{{ this.fmt }} != {{ that.name }}_SW_MINOR_VERSION_{{ that.fmt }}) || \
     ({{ this.name }}_SW_PATCH_VERSION_{{ this.fmt }} != {{ that.name }}_SW_PATCH_VERSION_{{ that.fmt }}))
    {{ mark }}error "Software Version Numbers of {{ this.fn }} and {{ that.fn }} are different"
{{ mark }}endif
""".lstrip(), **_TM_SETTINGS)
    )

    class File:
        REG_CAMEL = re.compile(
            r'([A-Z0-9]+(?=[A-Z0-9]|$|_)|[A-Z0-9]?[a-z0-9]+(?=[A-Z0-9]|$|_))(?:_)?')
        UPPER_PHRASE = ['MEMIF', 'DRVERROR', 'PBCFG', 'SECURITYCPY']

        def camel2upper(self, s):
            return '_'.join(map(str.upper, self.REG_CAMEL.findall(s)))

        def __init__(self, full_file_name) -> None:
            self.fn = full_file_name
            self.name, self.fmt = full_file_name.split('.')
            names = self.name.split('_')
            self.name = '_'.join([(self.camel2upper(n) if n.upper() not in self.UPPER_PHRASE
                                   else n.upper()) for n in names])
            self.fmt = self.fmt.upper()

        @property
        def has_module(self):
            return not IgnoreRule.skip_module_line(self.name)

        @property
        def has_version(self):
            return not IgnoreRule.skip_version(self.name)

    TOKEN_KEEP = set('include elif else'.split())
    TOKEN_FORWARD = set('if ifdef ifndef'.split())
    TOKEN_BACK = set('endif'.split())

    def __init__(self, file: SourceFile) -> None:
        self.file = file
        self.tokenizer = PreprocessorTokenizer(file.path)
        self.token_list: List[CMacroToken] = list(self.tokenizer.key_tokens())
        render_tokens, _ = VersionInfoRender._resolver(
            [CMacroToken('#', 'if', '')]
            + self.token_list
            + [CMacroToken('#', 'endif', '')]
        )
        self.render_tokens: List[CMacroToken] = render_tokens[0][1:-1]
        if len(self.render_tokens) == 1 and isinstance(self.render_tokens[0], list):
            self.render_tokens = self.render_tokens[0]

        if self.file.file_name.endswith('.h'):
            if len(self.render_tokens) > 1 and \
                (isinstance(self.render_tokens[0], CMacroToken) and self.render_tokens[0].op == 'ifndef') and \
                    (isinstance(self.render_tokens[-1], CMacroToken) and self.render_tokens[-1].op == 'endif'):
                self.render_tokens = self.render_tokens[1:-1]

    @staticmethod
    def _resolver(token_list: List[CMacroToken], cur_idx=0):
        result_list = []
        i = cur_idx
        while i < len(token_list):
            tk = token_list[i]
            if tk.op in VersionInfoRender.TOKEN_KEEP:
                result_list.append(tk)
            elif tk.op in VersionInfoRender.TOKEN_FORWARD:
                new_list, new_pos = VersionInfoRender._resolver(
                    token_list, i+1)
                result_list.append([tk]+new_list)
                i = new_pos
            elif tk.op in VersionInfoRender.TOKEN_BACK:
                result_list.append(tk)
                if cur_idx > 0:
                    # Not root
                    return result_list, i
            else:
                raise RuntimeError(f'Unexpected token {tk}')
            i += 1
        return result_list, i

    @staticmethod
    def contains(tokens, op='include'):
        if isinstance(op, str):
            def chk_fn(tk): return tk.op == op
        elif callable(op):
            chk_fn = op
        else:
            raise RuntimeError("op can only be str or a function.")

        for t in tokens:
            if isinstance(t, CMacroToken) and chk_fn(t):
                return True
            elif isinstance(t, list) and VersionInfoRender.contains(t, chk_fn):
                return True
        return False

    def render(self, output_fp: io.TextIOWrapper = None):
        output_version = ''
        output_check = ''
        if IgnoreRule.skip_version(self.file.file_name):
            return output_version, output_check

        # Verbose print
        includes = [t for t in self.tokenizer.tokens if t.op == 'include']
        if len(includes) > 0:
            print(f"Found includes:")
            for t in includes:
                print(
                    f'\t{t}{"" if not IgnoreRule.skip_header(t.header) and not IgnoreRule.skip_version(t.header) else "  (Ignored)"}')

        def _iter_output_check_info(tokens: List[CMacroToken], _output, layer=0):
            # Contains no #include
            if len(tokens) == 0 or not VersionInfoRender.contains(tokens, 'include'):
                return _output
            # Skip check for simple AUTOSAR if-endif
            if CONF['env']['SKIP_SIMPLE_AUTOSAR'] \
                    and isinstance(tokens[0], CMacroToken) \
                    and tokens[0].op == 'ifdef' \
                    and 'USING_OS_AUTOSAROS' in tokens[0].param \
                    and not VersionInfoRender.contains(tokens, 'else'):
                if CONF['env']['VERBOSE']:
                    print(f'AUTOSAR include ignored.')
                return _output
            for t in tokens:
                if isinstance(t, list):
                    _output = _iter_output_check_info(t, _output, layer+1)
                else:
                    if t.op == 'include':
                        this_file = VersionInfoRender.File(self.file.file_name)
                        that_file = VersionInfoRender.File(t.header)

                        # if this_file.has_version and that_file.has_version:
                        _output += VersionInfoRender.TM['CHECK'].render(
                            type=self.file.type,
                            this=this_file,
                            that=that_file,
                            **CONF
                        ) + '\n'
                        if layer == 0:
                            _output += '\n'
                    else:
                        _output += str(t) + '\n'
                        if t.op == 'endif' and layer == 0:
                            _output += '\n'
            return _output

        output_version += VersionInfoRender.TM['VERSION'].render(
            type=self.file.type,
            this=VersionInfoRender.File(self.file.file_name),
            **CONF
        ) + '\n\n'
        output_check += VersionInfoRender.TM['CHECK_HEADER'].render(
            type=self.file.type,
            **CONF
        ) + '\n'

        if CONF['env']['VERBOSE']:
            print(self.render_tokens)
        output_check = _iter_output_check_info(
            self.render_tokens, output_check) + "\n"

        if output_fp is None:
            fp = open(self.file.output_fn, 'w',
                      encoding=CONF['env']['FILE_ENCODING'])
        else:
            fp = output_fp
        fp.write(output_version)
        fp.write(output_check)
        if output_fp is None:
            fp.close()
        return output_version, output_check


REG_INSERT_VERSION = re.compile(
    r'/[\*= \n]+?(?i:SOURCE FILE VERSION INFORMATION|Source File Version Information)[\*= \n]+?/[\s\S]+?define\s+(?:.+?)_SW_(?:PATCH|REVISION)_VERSION(?:.+?)\n+',
    re.IGNORECASE)
REG_INSERT_CHECK = re.compile(
    r'/[\*= \n]+?(?i:Imported Compiler Switch Checks|File Version Checks)[\*= \n]+?/\n+([\s\S]+error\s*(?i:"Software Version(.+?) are different")(:?\s*\n+(?:#|\$\{mark\})endif)+)?',
    re.IGNORECASE)


def main():
    skipped_version = []
    version_insertion_not_found = []
    check_insertion_not_found = []

    for root, fn in SourceFile.iter_path():
        file = SourceFile(join(root, fn))
        file_skipped = IgnoreRule.skip_version(fn)
        output_version, output_check = VersionInfoRender(file).render()

        if file_skipped:
            skipped_version.append(file)
            continue

        # Auto insert
        with open(file.path, encoding=CONF['env']['FILE_ENCODING']) as f:
            content = f.read()

            found_version = len(list(REG_INSERT_VERSION.finditer(content))) > 0
            found_check = len(list(REG_INSERT_CHECK.finditer(content))) > 0
            try_append = CONF['env']['INSERT_CHECK_AFERT_VERSION_IF_NOT_FOUND_INSERTION']

            if found_version:
                if found_check:
                    content = REG_INSERT_VERSION.sub(output_version, content)
                    content = REG_INSERT_CHECK.sub(output_check, content)
                else:
                    if try_append:
                        content = REG_INSERT_VERSION.sub(
                            output_version+output_check, content)
                    else:
                        check_insertion_not_found.append(file)
            else:
                version_insertion_not_found.append(file)
                if found_check:
                    content = REG_INSERT_CHECK.sub(output_check, content)
                else:
                    check_insertion_not_found.append(file)

            out_dir = join(CONF['env']['OUTPUT_DIR'],
                           CONF['module']['NAME'], file.inner_path)
            os.makedirs(out_dir, exist_ok=True)

            with open(join(out_dir, file.file_name), 'w', encoding=CONF['env']['FILE_ENCODING']) as of:
                of.write(content)

    print('\n========================= [Summary] =========================')
    if skipped_version:
        print('Skip version info generating for files below:')
        print('(manual inserting instead)')
        for file in skipped_version:
            print(f'  {file.path}')
    if version_insertion_not_found:
        print('Could not find pattern of VERSION insertion:')
        for file in version_insertion_not_found:
            print(f'  {file.path}')
    if check_insertion_not_found:
        print('Could not find pattern of CHECK insertion:')
        for file in check_insertion_not_found:
            print(f'  {file.path}')


if __name__ == "__main__":
    import traceback
    if os.path.exists(CONF['env']['OUTPUT_DIR']):
        rmtree(CONF['env']['OUTPUT_DIR'])
    if not os.path.exists(CONF['env']['OUTPUT_DIR']):
        os.mkdir(CONF['env']['OUTPUT_DIR'])
        os.mkdir(join(CONF['env']['OUTPUT_DIR'], 'patches'))

    # print('Fill the info below. (Input nothing to use default value)')
    # CONF['module']['NAME'] = input(
    #     f"Module name (default={CONF['module']['NAME']!r}): ").strip() \
    #     or CONF['module']['NAME']
    # CONF['module']['VENDOR_ID'] = input(
    #     f"Vendor ID (default={CONF['module']['VENDOR_ID']!r}): ").strip() \
    #     or CONF['module']['VENDOR_ID']
    # CONF['module']['MODULE_ID'] = input(
    #     f"Module ID (default={CONF['module']['MODULE_ID']!r}): ").strip() \
    #     or CONF['module']['MODULE_ID']
    # CONF['module']['INSTANCE_ID'] = input(
    #     f"Instance ID (default={CONF['module']['INSTANCE_ID']!r}): ").strip() \
    #     or CONF['module']['INSTANCE_ID']
    # CONF['module']['AR_RELEASE_MAJOR_VERSION'] = input(
    #     f"Autosar major version (default={CONF['module']['AR_RELEASE_MAJOR_VERSION']!r}): ").strip() \
    #     or CONF['module']['AR_RELEASE_MAJOR_VERSION']
    # CONF['module']['AR_RELEASE_MINOR_VERSION'] = input(
    #     f"Autosar minor version (default={CONF['module']['AR_RELEASE_MINOR_VERSION']!r}): ").strip() \
    #     or CONF['module']['AR_RELEASE_MINOR_VERSION']
    # CONF['module']['AR_RELEASE_PATCH_VERSION'] = input(
    #     f"Autosar patch version (default={CONF['module']['AR_RELEASE_PATCH_VERSION']!r}): ").strip() \
    #     or CONF['module']['AR_RELEASE_PATCH_VERSION']
    # CONF['module']['SW_MAJOR_VERSION'] = input(
    #     f"Software major version (default={CONF['module']['SW_MAJOR_VERSION']!r}): ").strip() \
    #     or CONF['module']['SW_MAJOR_VERSION']
    # CONF['module']['SW_MINOR_VERSION'] = input(
    #     f"Software minor version (default={CONF['module']['SW_MINOR_VERSION']!r}): ").strip() \
    #     or CONF['module']['SW_MINOR_VERSION']
    # CONF['module']['SW_PATCH_VERSION'] = input(
    #     f"Software patch version (default={CONF['module']['SW_PATCH_VERSION']!r}): ").strip() \
    #     or CONF['module']['SW_PATCH_VERSION']

    try:
        main()
    except Exception:
        print(traceback.format_exc())
    input("Press ENTER to exit")
