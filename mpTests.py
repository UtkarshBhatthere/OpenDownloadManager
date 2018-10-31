import multiprocessing as mp

a = list()
ip = [0,1,2,3,4,5,6,7]

def square(x, b):
    b.append(x**2)
    print(b)

prcs = list()
for j in ip:
    p = mp.Process(target=square, args=(j,a,))
    prcs.append(p)
    p.start()

for k in prcs:
    k.join()

print(a)