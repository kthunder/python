import re
import clipboard

text = clipboard.paste()
# REG_CAMEL = re.compile(r'([A-Z]+(?=[A-Z]|$|_)|[A-Z]?[a-z]+(?=[A-Z]|$|_))(?:_)?')
REG_CAMEL = re.compile(r'([A-Z]+|[A-Z]?[a-z]+)_?')
CAMEL2UPPER = lambda s: '_'.join(map(str.upper, REG_CAMEL.findall(s)))
print(CAMEL2UPPER('CPUInfo'))
print(CAMEL2UPPER('InfoCPU'))
print(CAMEL2UPPER('A_a'))
print(CAMEL2UPPER('DCache'))
print(CAMEL2UPPER('Abcd_ABC'))
print(CAMEL2UPPER('AAABbbCcc'))
