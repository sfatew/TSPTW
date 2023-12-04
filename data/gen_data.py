import random
import json

with open("data.txt", "w") as f:  
    n=random.randint(0,99999)
    print(n,file=f)
    for i in range(n):
        print()






