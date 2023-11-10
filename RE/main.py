import re

log = r"""
PS C:\Users\Administrator\Desktop\python> python -u "c:\Users\Administrator\Desktop\python\RE\main.py"
111
PS C:\Users\Administrator\Desktop\python> python -u "c:\Users\Administrator\Desktop\python\RE\main.py"
Traceback (most recent call last):
  File "c:\Users\Administrator\Desktop\python\RE\main.py", line 6, in <module>  
    p = re.compile('[a-Z]')
        ^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python311\Lib\re\__init__.py", line 227, in compile    
    return _compile(pattern, flags)     
           ^^^^^^^^^^^^^^^^^^^^^^^^     
  File "C:\Program Files\Python311\Lib\re\__init__.py", line 294, in _compile   
    p = _compiler.compile(pattern, flags)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python311\Lib\re\_compiler.py", line 743, in compile   
    p = _parser.parse(p, flags)
        ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python311\Lib\re\_parser.py", line 980, in parse       
    p = _parse_sub(source, state, flags & SRE_FLAG_VERBOSE, 0)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python311\Lib\re\_parser.py", line 455, in _parse_sub  
    itemsappend(_parse(source, state, verbose, nested + 1,
e\_parser.py", line 612, in _parse
    raise source.error(msg, len(this) + 1 + len(that))
re.error: bad character range a-Z at position 1
The path has a pattern like this:
driver:\path\...
PSpython -u "c:\Users\Administrator\Desktop\python\RE\main.py"   
['h', 'e', 'l', 'l', 'o', 'h', 'e', 'l', 'l', 'o']
PS C:\Users\Administrator\Desktop\python> python -u "c:\Users\Administrator\Desktop\python\RE\main.py"
['ello', 'eo']
PS C:\Users\Administrator\Desktop\python> python -u "c:\Users\Administrator\Desktop\python\RE\main.py"
['hello', 'heo']
PS C:\Users\Administrator\Desktop\python>

"""
if __name__ == "__main__":
	p = re.compile(r'(?<=[^A-Z])[A-Z]:\\[\w\\\. ]+', re.IGNORECASE)
	res = p.findall(log)
	print(*res, sep='\n')