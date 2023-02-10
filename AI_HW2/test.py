import csv
edgeFile = 'edges.csv'

def ucs(start, end):
    # Begin your code (Part 3)
    with open(edgeFile, 'r') as f:
        edges = list(csv.DictReader(f))
        adj_list, cost = {}, {}
        for edge in edges:
            if edge['start'] not in adj_list:
                adj_list[edge['start']] = [[float(edge['distance']), edge['end']]]
                cost[(edge['start'], edge['end'])] = float(edge['distance'])
            else:
                adj_list[edge['start']].append([float(edge['distance']), edge['end']])
                cost[(edge['start'], edge['end'])] = float(edge['distance'])
        path, dist, num_visited = [], 0, 0
        parent = {}
        p_queue, visited = [], set()
        start, end = str(start), str(end)
        p_queue.append([0, start])
        while len(p_queue) > 0:
            p_queue = sorted(p_queue)
            node = p_queue.pop(0)
            if node[1] == end:
                dist = node[0]
                break

            visited.add(node[1])
            num_visited += 1            
            if node[1] in adj_list:
                for vertex in adj_list[node[1]]:
                    flag = False
                    idx = 0
                    for elements in p_queue:
                        if elements[1] == vertex[1]:
                            idx = p_queue.index(elements)
                            flag = True
                            break
                    
                    if not flag and vertex[1] not in visited:
                        parent[vertex[1]] = node[1]
                        p_queue.append([node[0] + cost[(node[1], vertex[1])], vertex[1]])
                    elif flag:
                        if node[0] + cost[(node[1], vertex[1])] < p_queue[idx][0]:
                            parent[p_queue[idx][1]] = node[1]
                            p_queue[idx][0] = node[0] + cost[(node[1], vertex[1])]
        path.append(int(end))
        while str(path[-1]) != start:
            path.append(int(parent[str(path[-1])]))
        path.reverse()
    return path, dist, num_visited
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(426882161, 1737223506)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
