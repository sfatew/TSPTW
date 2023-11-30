import numpy as np

a=np.array([1,2,3,4])

a=a/sum(a)

next=np.random.choice(np.arange(1,5),p=a)

print(a)
print(next)

print(0/0)