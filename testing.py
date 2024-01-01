# a=[1,2,3,5,4]
# try:
#     print(a[None])
# except:
#     print(None)

# import numpy as np
# a=[[1,3,6,4,9,2],[1,4,3,5,6,8]]
# a=np.array(a)
# print(a[(1,2)])
# [b,c]=a
# print(b)

import numpy as np
# i=[[1,2],[4,6]]
# i=np.array(i)
# j=[[1,3],[5,6]]
# j=np.array(j)
# j=j**2
# print((i*j)[:,1])

a=0
i=0
while i<5:
    if a<4:
        a += 1
        print(a)
        i+=1

    else:
        print(a)
        i+=1
        print(i)
