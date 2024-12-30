import sys
import numpy as np


with open('map.txt', 'r') as file1:
    data1 = file1.readlines()

map = {}
for line in data1:
    line = line.strip()
    key, val = line.split('-')
    map[key] = {}
    for dest in val.split(','):
        dest_city, d = dest.split('(')
        d = float(d.strip(')'))
        map[key][dest_city] = d


with open('coordinates.txt', 'r') as file2:
    data2 = file2.readlines()

coordinates = {}
for line in data2:
    line = line.strip()
    key, val = line.split(':(')
    coordinates[key] = []
    for loc in val.split(','):
        coordinates[key].append(float(loc.strip(')')))


def main():
    if len(sys.argv) != 3:
        print("Usage: python a-star.py <city-1> <city-2>")

    start = sys.argv[1]
    end = sys.argv[2]
    r = 3958.8

    total = 0
    next = route = start
    l = {}
    last = 0
    while next != end:
        for curr in map[next]:
            dist = map[next][curr] + total

            long1 = coordinates[curr][1]*np.pi/180
            long2 = coordinates[end][1]*np.pi/180
            lat1 = coordinates[curr][0]*np.pi/180
            lat2 = coordinates[end][0]*np.pi/180

            sld = 2*r*np.arcsin(np.sqrt((np.sin((lat2-lat1)/2)**2)+np.cos(lat1)*np.cos(lat2)*(np.sin((long2-long1)/2)**2)))

            prev_route = route
            route += ' - ' + curr

            l[float(sld+dist)] = [curr, dist, route]
            route = prev_route

        w = list(l.keys())

        route = l[min(w)][2]
        total = l[min(w)][1]
        next = l[min(w)][0]
        last = l.pop(min(w))

    print(f"From city: {start}\nTo city: {end}")
    print(f"Best Route: {last[2]}")
    print(f"Total distance: {total:.2f} mi")


if __name__ == "__main__":
    main()
