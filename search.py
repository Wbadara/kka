import heapq
from collections import deque

soal_map = {
    'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118},
    'Zerind': {'Arad': 75, 'Oradea': 71},
    'Oradea': {'Zerind': 71, 'Sibiu': 151},
    'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilcea': 80},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Dobreta': 75},
    'Dobreta': {'Mehadia': 75, 'Craiova': 120},
    'Craiova': {'Dobreta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138},
    'Rimnicu Vilcea': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Pitesti': {'Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101},
    'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
    'Giurgiu': {'Bucharest': 90},
    'Urziceni': {'Bucharest': 85, 'Hirsova': 98, 'Vaslui': 142},
    'Hirsova': {'Urziceni': 98, 'Eforie': 86},
    'Eforie': {'Hirsova': 86},
    'Vaslui': {'Urziceni': 142, 'Iasi': 92},
    'Iasi': {'Vaslui': 92, 'Neamt': 87},
    'Neamt': {'Iasi': 87}
}

def dfs(graph, start, goal):
    stack = [[(start, 0)]]
    visited = set()
    
    while stack:
        path = stack.pop()
        node, _ = path[-1]
        
        if node == goal:
            return path
            
        if node not in visited:
            visited.add(node)
            for neighbor, distance in graph[node].items():
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append((neighbor, distance))
                    stack.append(new_path)
    return None

def bfs(graph, start, goal):
    queue = deque([[(start, 0)]])
    visited = set([start])
    
    while queue:
        path = queue.popleft()
        node, _ = path[-1]
        
        if node == goal:
            return path
            
        for neighbor, distance in graph[node].items():
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append((neighbor, distance))
                queue.append(new_path)
    return None

def ucs(graph, start, goal):
    queue = [(0, [(start, 0)])]
    visited = set()
    
    while queue:
        cost, path = heapq.heappop(queue)
        node, _ = path[-1]
        
        if node == goal:
            return path, cost
            
        if node not in visited:
            visited.add(node)
            for neighbor, distance in graph[node].items():
                if neighbor not in visited:
                    total_cost = cost + distance
                    new_path = list(path)
                    new_path.append((neighbor, distance))
                    heapq.heappush(queue, (total_cost, new_path))
    return None, 0

def calculate_cost(path):
    if not path:
        return 0
    return sum(cost for node, cost in path)

def print_result(algo_name, path, total_cost=None):
    if total_cost is None:
        total_cost = calculate_cost(path)
    route = " -> ".join([node for node, cost in path])
    print(f"=== {algo_name} ===")
    print(f"Rute: {route}")
    print(f"Total Jarak: {total_cost}\n")

if __name__ == "__main__":
    start_node = 'Arad'
    goal_node = 'Bucharest'
    
    dfs_path = dfs(soal_map, start_node, goal_node)
    print_result("Depth-First Search (DFS)", dfs_path)
    
    bfs_path = bfs(soal_map, start_node, goal_node)
    print_result("Breadth-First Search (BFS)", bfs_path)
    
    ucs_path, ucs_cost = ucs(soal_map, start_node, goal_node)
    print_result("Uniform Cost Search (UCS)", ucs_path, ucs_cost)

