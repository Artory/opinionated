"""
File docstring
preserved
"""

x = ''
y = ''
z = ' '
a = '''
a '' long quote
'''
b = ' '
c = ''' this
another '' long quote
'''
e = '''
\'''
'''
f = '\'with quotes\''
k = lambda x: 'me'

class Klass:
    """DOCSTRING"""

def preserve_docstrings(a='test'):
    """Since this is a set style"""
    'But a random string after isn\'t' # comments

def annotations(a: 'test') -> 'test':
    pass
