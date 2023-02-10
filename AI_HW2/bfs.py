import csv
import queue

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

def bfs(start, end):
    # Begin your code (Part 1)
    '''
    Before going into dfs function, read csv file, store each line in a list in edges
    Create a queue with only start in it
    Run a loop until the q is empty
        Every layer of loop pop the current node from queue
        Find the edge with start node equal to current node and end node not visited
        Update parent of the end node to start node of edge and distance 
        If the end node is end, start from end and find the path to start thruogh parent of each node
        Append the node on the route to path list and return the reverse path to get path from start to end
        If the end node is not end, push the end node into queue
    If queue is empty, means no path, return no path
    '''
    path = []
    visited = []
    parent = {}
    q = queue.Queue()
    q.put(start)
    visited.append(start)
    distance = 0

    while not q.empty():
        node = q.get()

        for edge in edges:
            if edge[0] == node and edge[1] not in visited:
                parent[edge[1]] = (edge[0], edge[2])

                visited.append(edge[1])

                if edge[1] == end:
                    current = edge[1]
                    while current != start:
                        path.append(current)

                        distance += parent[current][1]
                        
                        current = parent[current][0]
                        
                    path.append(start)
                    path.reverse()
                    
                    file.close()
                    return (path, distance, len(visited))
                        
                q.put(edge[1])
                

    return ([], -1, -1)
    # End your code (Part 1)


if __name__ == '__main__':
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
