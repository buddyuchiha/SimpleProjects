from collections import deque  

city_map = {  
    'Home': ['Park', 'School', 'Mail'],  
    'Park': ['Home', 'Museum', 'Cafe'],  
    'School': ['Home', 'Library', 'Mail'],  
    'Mail': ['Home', 'School', 'Hospital'],  
    'Library': ['School', 'Hospital'],  
    'Hospital': ['Library', 'Mail', 'Office'],  
    'Cafe': ['Park', 'Theater', 'Office'],  
    'Museum': ['Park', 'Shop'],  
    'Shop': ['Museum', 'Theater'],  
    'Theater': ['Shop', 'Cafe'],  
    'Office': ['Cafe', 'Hospital']  
}
  
  
def bfs_shortest_path(city_map, start, goal):   
    queue = deque([[start]])  
    visited = set()  
  
    while queue:  
        path = queue.popleft()  
        node = path[-1]  
  
        if node in visited:  
            continue  
  
        visited.add(node)  
  
        if node == goal:  
            return path  
  
        for neighbor in city_map.get(node, []):  
            new_path = list(path) 
            new_path.append(neighbor)  
            queue.append(new_path)  
  
    return None  
  

  
start = 'Home'  
goal = 'Theater'  
shortest_path = bfs_shortest_path(city_map, start, goal)  
print("Кратчайший путь от Home до Theater:", shortest_path)