import numbers
import functools

x = [1, [2], 3]

a = x[1]
x[1] = a[0] 
print(x)

print("Hello World")

x = {
    "f": 3
}

print(x.get("f"))

# list(map(lambda x: x if isinstance(x, str) else (raise RuntimeError("Cannot take numbers as arguments"), ['a', 'b']))  


print(list(map(def abc(x): x if isinstance(x, str) else (raise RuntimeError("Cannot take numbers as arguments"), ['a', 'b']))))