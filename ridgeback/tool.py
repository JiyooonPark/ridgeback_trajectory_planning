class a:
    def __init__(self):
        self.n = 1

list = []
# for i in range(3):
#     list.append(a())
b = a()
c = a()
d = a()
list.append(b)
list.append(c)
list.append(d)
print(list)
list.remove(c)
print(list)