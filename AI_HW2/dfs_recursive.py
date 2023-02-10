import csv
import sys

sys.setrecursionlimit(5000)
edgeFile = 'edges.csv'
file = open(edgeFile)
csvreader = csv.reader(file)
rows = []
header = next(csvreader)
for row in csvreader:
    rows.append(row)

file.close()

edges = []
for edge in rows:
    tmp = [int(edge[0]), int(edge[1]), float(edge[2]), float(edge[3])]
    edges.append(tmp)

visited = []

def dfs(start, end):
    # Begin your code (Part 2)
    '''
    Before going into dfs function, read csv file, store each line in a list in edges
    Every recursion in dfs, find the edge in edges whose starting node = start
        If the end node of the edge is end, add the nodes of this edge to path and return
        Else if end node is not end and not visited yet, go to recursion
        From the result of recursion, check if dist is -1 
            If yes, means this edge is not in the path
            If not, add node to path, then return 
    '''
    visited.append(start)
    
    for edge in edges:
        if edge[1] == end and edge[0] == start:
            path = [edge[0], edge[1]]
            visited.append(edge[1])
            return (path, edge[2], len(visited))

        elif edge[0] == start and edge[1] not in visited:
            path, dist, num_visited = dfs(edge[1], end)
            if dist == -1:
                continue
            
            path.insert(0, edge[0])
            file.close()
            return (path, dist + edge[2], len(visited))

    return ([], -1, -1)
    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
