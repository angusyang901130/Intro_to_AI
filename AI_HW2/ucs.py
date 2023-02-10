import csv
import heapq

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
            
def ucs(start, end):
    # Begin your code (Part 3)
    '''
    Before going into dfs function, read csv file, store each line in a list in edges
    Create priority queue using heapq
    The heapq stores tuples (dist, current id, parent id), sort by dist
    Dist is the distance from start to current node
    Value is the length of the path to current id via parent id
    Run a loop until heap is empty
        Every iteration pop a tuple
        If the current node is not visited, update parent of current
        Add current node to visited
        If current node is end, then find the path to start through parent of each node
        Append the node on the route into path and return the reverse path to get path from start to end
        If current node is not end, find neighbors that are not visited yet
        Push new tuple (dist + edge length, neighbor id, current id) to heap
    If heap is empty, means no path, return no path
    '''
    visited = []
    parent = {}
    heap = []
    heapq.heappush(heap, (0, start, start))  # distance, current id, parent id

    while heap:
        val, cur, par = heapq.heappop(heap)

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
                heapq.heappush(heap, (val + edge[2], edge[1], edge[0]))

    return ([], -1, -1)
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
