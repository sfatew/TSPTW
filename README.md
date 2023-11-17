
## Symmetric TSPTW PROB

### Một nhân viên giao hàng lấy hàng ở kho (điểm 0) và cần đi giao hàng cho N khách hàng 1,2,…, N. Khách hàng i nằm ở điểm i và có yêu cầu giao hàng trong khoảng thời gian từ e(i) đến l(i) và giao hàng hết d(i)  đơn vị thời gian (s). Biết rằng  t(i,j) là thời gian di  chuyển từ điểm i đến điểm j. Nhân viên giao hàng xuất phát từ kho tại thời điểm t0, hãy tính toán lộ trình giao hàng cho nhân viên giao hàng sao cho tổng thời gian di chuyển là ngắn nhất.

#### Variables
* Binary variable x(i,j) = 1 if the route traverses from point i to point j,
                         = 0, otherwise.
* t(i) represents the time at which the salesman arrived at node i 
* t(i,j) represents the truck travel time between nodes i and j.
* t'(i) = max{ei , ti }, the time point at which the agent can start to serve the node

#### Constraints
##### N is the set {1,2,...,N}

*          (All nodes have to be visited by truck exactly once & leave to exactly 1 node) 
$$ \sum_{i=1}^{N} X_{i,j} = \sum_{i=1}^{N} X_{j,i} =1, \forall j\in N$$

*          (can't travel to the same point twice)
$$ \sum_{(i,j)\in S} X_{i,j} \leq |S| -1, \forall S \subseteq N,  and |S| < N$$
        
*         (time window constrain)
$$ (t_{i}^{'} +s_{i}+ t_{i,j})x_{i,j} \leq b_{j}, \forall (i,j) $$


#### Objective function to be minimized
* (the time at which the salesman arrived back at the depot)
$$ Min(t_{N+1}) $$
          
