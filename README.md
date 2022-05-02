# Pywarper
- a way to warp fucntions and convert passed arguments beffore they reach the main function
- this is fork from lost account
- this tools allow you to write dry code  and  its short cut  
## Features

- warp *args
- warp **kwargs
- warp first-paramater
- warp n-first-paramater
- warp warp-first-paramater
- warp-first-kind
- warp n-first-kind
--i  mean by kind:
-- - _VAR_POSITIONAL
-- - _VAR_KEYWORD
-- - _KEYWORD_ONLY
-- -  _POSITIONAL_OR_KEYWORD
-- -  _POSITIONAL_ONLY

------------
## Usage

```python
from pywarper import dwarp

def convert_to_cm(x):
	return x * 100
target =  {"x":convert_to_cm}
@dwarp(target)
def foo(x,*args):
	return x
foo(1)
# 100
target["x"] = lambda x :x*1000
foo(1)
# 1000
```

```python
from pywarper import dwarp
class Target:
	@staticmethod
	def x(value):
		return x*100
		
@dwarp(Target)
def foo(x,*args):
	return x

```
## Up comming feature
- support classes (they work but need proxy object maybe)
- support on spesail classes dunder methods __dunder__
- support first n type depend on annotation
...etc






