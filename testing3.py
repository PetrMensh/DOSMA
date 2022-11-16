n = 6

a = [*range(0,10**(n//2))]
a = list(map(lambda x: str(x), a))
a = list(map(lambda x: list(x), a))
b = list(map(lambda x: list(map(lambda y: int(y), x)), a))
b = list(map(lambda x: sum(x), b))
c = list(map(lambda x: b.count(x), b))
print(sum(c))

if n == 1:
    luck_number = 9
else:
    if n % 2 == 0:
        luck_number = sum(c)
    else:
        luck_number = sum(c)*10







#print(list(map(lambda x: sum(int(list(str(x)))), a)))
#print(b)