
import string

a = string.ascii_uppercase
b = 'CDEFGHIJKLMNOPQRSTUV'
d = '['
for c in b:
    d += '\'' + c + '\'' + ', '

d += ']'
print(d)