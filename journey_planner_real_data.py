import pandas as pd
from utils.adjacency_list_graph import AdjacencyListGraph
from utils.dijkstra import dijkstra


def reconstruct_path(pi, start, destination):
    """ So here im gonna reconstruct the shortest path using the predecessor list."""
    path = []
    current = destination
    while current is not None:
        path.insert(0, current)
        current = pi[current]

    if not path or path[0] != start:
        return []
    return path


def load_network_from_excel(filename):
    """Now im gonna load the London Underground network from the Excel file.
    Only rows with valid Line, StationA, StationB, Time will be processed.
    If there is multiple connections that exist between two stations, im going to keep the one with minimum time."""

    df = pd.read_excel(filename, header=None)

    stations_set = set()
    edges_dict = {}  # So here im gonna change from set to dict to make sure it tracks minimum times

    for _, row in df.iterrows():
        # This will skip the rows without enough data
        if len(row) < 4:
            continue

        line = str(row[0]).strip()
        station_a = row[1]
        station_b = row[2]
        travel_time = row[3]

        # Now i needa validate full data
        if pd.isna(station_a) or pd.isna(station_b) or pd.isna(travel_time):
            continue

        try:
            travel_time = int(travel_time)
        except:
            continue  # This will skip the rows where time isn't an integer (again skipping rows without enough data)

        # This will clean the names
        station_a = str(station_a).strip()
        station_b = str(station_b).strip()

        # Now im gonna add stations
        stations_set.add(station_a)
        stations_set.add(station_b)

        # Here i need to store the edge with minimum time basically sorting stations to avoid A-B vs B-A duplicates
        edge_key = tuple(sorted([station_a, station_b]))

        # I need to keep the minimum travel time for this connection
        if edge_key not in edges_dict or travel_time < edges_dict[edge_key]:
            edges_dict[edge_key] = travel_time

    stations = sorted(list(stations_set))
    station_index = {name: i for i, name in enumerate(stations)}

    # Here is the part to build graph
    G = AdjacencyListGraph(len(stations), directed=False, weighted=True)

    # I need to insert edges with minimum times
    for (a, b), t in edges_dict.items():
        G.insert_edge(station_index[a], station_index[b], t)

    return G, stations



def main():
    print("London Underground Journey Planner (Task 2B)")
    print("--------------------------------------------")

    filename = "London Underground data.xlsx"

    print("Loading network data...")

    # Okay so now this will load graph and stations from Excel file
    G, stations = load_network_from_excel(filename)

    print(f"Loaded {len(stations)} stations.")
    print()

    # And then it will show a preview of some stations
    print("Example stations:")
    print(stations[:20])
    print()

    # I need it to ask the user for start/destination to calculate the route for them
    start_station = input("Enter start station: ").strip()
    destination_station = input("Enter destination station: ").strip()

    if start_station not in stations or destination_station not in stations:
        print("One or both station names are not recognised.")
        return

    start_idx = stations.index(start_station)
    dest_idx = stations.index(destination_station)

    print("\nCalculating shortest route...")

    # I need to run Dijkstra using the library code
    d, pi = dijkstra(G, start_idx)

    if d[dest_idx] == float('inf'):
        print("No route found between the selected stations.")
        return

    # And also reconstruct path
    path_indices = reconstruct_path(pi, start_idx, dest_idx)
    path_stations = [stations[i] for i in path_indices]

    print("\nShortest journey found:")
    print(" -> ".join(path_stations))
    print(f"Total travel time: {d[dest_idx]} minutes")


if __name__ == "__main__":
    main()
