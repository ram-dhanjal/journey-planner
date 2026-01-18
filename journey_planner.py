# journey_planner.py
# Task 2(a): So im making a Journey Planner Based on the Journey Time


from utils.adjacency_list_graph import AdjacencyListGraph
from utils.dijkstra import dijkstra

def reconstruct_path(pi, start, destination):
    """Reconstruct the shortest path from start to destination using the predecessor list."""
    path = []
    current = destination
    while current is not None:
        path.insert(0, current)
        current = pi[current]
    # Im going to return only the path that begins with the start node
    if path[0] != start:
        return []
    return path

def main():
    # Here im going to define simple artificial dataset which will be 5 stations
    stations = ['A', 'B', 'C', 'D', 'E']
    num_stations = len(stations)

    # Im gonna create a directed, weighted graph
    G = AdjacencyListGraph(num_stations, directed=True, weighted=True)

    # then insert edges with travel times in minutes (these values can be adjusted for testing)
    # Format: (start, end, duration)
    edges = [
        ('A', 'B', 5),
        ('A', 'C', 2),
        ('B', 'C', 1),
        ('B', 'D', 3),
        ('C', 'D', 7),
        ('C', 'E', 4),
        ('D', 'E', 2)
    ]

    for u, v, w in edges:
        G.insert_edge(stations.index(u), stations.index(v), w)

    # here im going to choose start and destination stations
    start_station = 'A'
    destination_station = 'E'

    print("Journey Planner - Shortest Route Based on Journey Time")
    print("------------------------------------------------------")
    print("Stations:", stations)
    print(f"Finding shortest route from {start_station} to {destination_station}...\n")

    # Run Dijkstra’s algorithm from the library to make sure the code aligns with the library code
    d, pi = dijkstra(G, stations.index(start_station))

    # now i need to reconstruct and display the shortest path
    path_indices = reconstruct_path(pi, stations.index(start_station), stations.index(destination_station))
    if not path_indices:
        print("No path found between the given stations.")
        return

    path_stations = [stations[i] for i in path_indices]
    total_duration = d[stations.index(destination_station)]

    # now time to output the results
    print("Shortest journey (station order):", " -> ".join(path_stations))
    print("Total journey duration:", total_duration, "minutes")

if __name__ == "__main__":
    main()

