f = open("layer1", 'r')
s = " "
for line in f.readlines():
    for i in range(0, len(line)-1, 3):
        current_number = line[i:i+3]
        if current_number in [' 04', ' 05', ' 12', ' 13', ' 20', ' 21']:
            s += current_number[1:]
        else:
            s += '08'
        s += ' '
    s += '\n'

print(s)


class A:
    def _f2(self):
        pass

    def f1(self):
        print("salut")
        self._f2()


class B(A):
    def _f2(self):
        print("à tous")


b = B()
b.f1()