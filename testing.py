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
i=[[1,2],[4,6]]
i=np.array(i)
for a in i:
    if a>3:
        idx=i.index(a)
        i[idx]=3

print(i)