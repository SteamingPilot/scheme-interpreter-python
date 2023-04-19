import numbers
import functools

x = [1, [2], 3]

a = x[1]
x[1] = a[0] 
print(x)