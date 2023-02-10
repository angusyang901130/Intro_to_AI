import csv
import heapq
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'

file = open(edgeFile)
csvreader = csv.reader(file)
rows = []
header = next(csvreader)
for row in csvreader:
    rows.append(row)

edges = []
for edge in rows:
    tmp = [int(edge[0]), int(edge[1]), float(edge[2]), float(edge[3])]   
    edges.append(tmp)

file.close()


file = open(heuristicFile)
csvreader = csv.reader(file)
rows = []
header = next(csvreader)
for row in csvreader:
    rows.append(row)

direct_dist = []
for d in rows:
    tmp = [int(d[0]), float(d[1]), float(d[2]), float(d[3])]   
    direct_dist.append(tmp)

file.close()

path_num = {2270143902: 1, 426882161: 2, 1718165260: 3}

def astar(start, end):
    # Begin your code (Part 4)
    '''
    Before going into dfs function, read csv files, store each line in a list in edges and direct_dist
    For direct_dist, there are three nodes as end, use path_num to decide which column(end node id) is using
    Create priority queue using heapq
    The heapq stores tuples (predict dist, dist, current id, parent id), sort by predict dist
    Dist is the length of the path to current id via parent id
    Predict dist = dist + heuristic dist
    Run a loop until heap is empty
        Every iteration pop a tuple
        If the current node is not visited, update parent of current
        Add current node to visited
        If current node is end, then find the path to start through parent of each node
        Append the node on the route into path and return the reverse path to get path from start to end
        If current node is not end, find neighbors that are not visited yet
        Push new tuple (dist + edge length + heuristic dist of neighbor, 
                        dist + edge length, neighbor id, current id) to heap
    If heap is empty, means no path, return no path
    '''
    index = path_num[start]
    visited = []
    parent = {}
    heap = []
    heapq.heappush(heap, (0, 0, start, start))  # predict dist, dist, current id, parent id

    while heap:
        predict, val, cur, par = heapq.heappop(heap)
        if cur in visited:
            continue
        
        parent[cur] = par
        visited.append(cur)
        if cur == end:
            path = []
            node = end
            while node != start:
                path.append(node)
                node = parent[node]
            path.append(start)
            path.reverse()

            return ( path, val, len(visited) )
        
        for edge in edges:
            if edge[0] == cur and edge[1] not in visited:
                for dist in direct_dist:
                    if dist[0] == edge[1]:
                        heapq.heappush(heap, (val + edge[2] + dist[index], val + edge[2], edge[1], edge[0]))

    return ([], -1, -1) 
    # End your code (Part 4)


if __name__ == '__main__':
    path, dist, num_visited = astar(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
