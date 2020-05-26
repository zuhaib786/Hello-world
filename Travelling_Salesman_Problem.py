#python3
import math
def  Factorial(n):
    if n == 0:
        return 1
    return n * Factorial(n-1)
def Co(n,r):
    if r>n//2:
        return Co(n,n-r)
    else:
        J = 1
        for i in range(n,n-r,-1):
            J *= i
        return J//Factorial(r)
class Generator:
    def __init__(self,n,m):
        self.data = [1]*m +[0]*(n-m)
    def Increment(self):
        if self.data[-1] == 0:
            i =len(self.data) -1
            while i>=0 and self.data[i] == 0:
                i -= 1
            self.data[i] = 0
            self.data[i+1] = 1
            return True
        else:
            i = len(self.data) - 1
            while i>=0 and self.data[i] == 1:
                i -= 1
            j = i
            while j>= 0 and self.data[j] == 0:
                j -= 1
            if j == -1:
                return False
            else:
                self.data[j] =0
                self.data[j+1] = 1
                if i == j+1 :
                    return True
                else:
                    k = len(self.data) -1
                    for x in range(j+2,i+1):
                        self.data[x],self.data[k] = self.data[k],self.data[x]
                        k -= 1
                    return True
    def Binary_Number(self):
        s = ''
        for i in self.data:
            s += str(i)
        return int(s,2)
class Graph:
    def __init__(self,n):
        self.Matrix =[[0]* n for i in range(n)]
    def Add_Edge(self,a,b,weight):
        self.Matrix[a][b]  = weight
        self.Matrix[b][a] = weight
    def Solve_TSP(self):
        n = len(self.Matrix)
        C = [[float('inf')] * n for i in range(2**n)]
        Correspond = [[float('inf')] * n for i in range(2**n)]
        C[1<<n-1][0] = 0
        G = Generator(n,2)
        for i in range(Co(n-1,1)):
            b  = G.Binary_Number()
            G.Increment()
            for x in range(1,n):
                if (b & (1<<(n-x-1))) !=0:
                    if self.Matrix[x][0]!=0:
                        C[b][x] = self.Matrix[x][0]
                        Correspond[b][x] = 0
                        break
        for s in range(3,n+1):
            Total = Co(n-1,s-1)
            G = Generator(n,s)
            for i in range(Total):
                b = G.Binary_Number()
                G.Increment()
                for x in range(1,n):
                    if (b & (1<<(n-x-1))) != 0:
                        min_indx = None
                        for y in range(1,n):
                            if (b & (1<<(n-y-1))) != 0 and self.Matrix[x][y] != 0:
                                if C[b][x] > C[b^(1<<(n-x-1))][y] + self.Matrix[x][y]:
                                    min_indx = (b^(1<<(n-x-1)),y)
                                    C[b][x] = C[b^(1<<(n-x-1))][y] + self.Matrix[x][y]
                                    Correspond[b][x] = min_indx
        X = 2**(n) - 1
        m  = float('inf')
        idx = None
        Paths = []
        costs = []
        for i in range(1,n):
            if self.Matrix[0][i] != 0:
                Path = [i]
                x = Correspond[X][i]
                while x != 0  and x != float('inf'):
                    Path.append(x[1])
                    x = Correspond[x[0]][x[1]]
                if Path[-1] != Path[0]:
                    Paths.append(Path)
                    costs.append(C[X][i]+self.Matrix[0][i])
                if m > C[X][i] + self.Matrix[0][i]:
                    m = C[X][i] + self.Matrix[0][i]
                    idx = i
        if len(Paths) == 0:
            return (float('inf'),None)
        min_idx = 0
        for i in range(1,len(costs)):
            if costs[i]<costs[min_idx]:
                min_idx = i
        return [costs[min_idx],Paths[min_idx]]
def ReadData():
    n,m = map(int,input().split())
    graph = Graph(n)
    for _ in range(m):
        a,b ,weight = map(int,input().split())
        graph.Add_Edge(a-1,b-1,weight)
    return graph
graph = ReadData()
X = graph.Solve_TSP()
if len(graph.Matrix) == 2:
    print(2 * graph.Matrix[0][1])
    print("1 2")
elif X[0] == float('inf'):
    print(-1)
else:
    data = X[1]
    print(X[0])
    print(1,end = ' ')
    for i in range(len(data)):
        print(data[i]+1,end = ' ')
    print()
