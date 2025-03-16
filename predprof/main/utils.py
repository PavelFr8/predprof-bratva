import requests

import numpy as np
from scipy.ndimage import maximum_filter
import matplotlib.pyplot as plt


def get_tile():
    req = requests.get("https://olimp.miet.ru/ppo_it/api")
    data = req.json().get("message").get("data")
    return data


def get_coords():
    req = requests.get("https://olimp.miet.ru/ppo_it/api/coords")

    return req.json().get("message")


def create_map():
    full_map = np.zeros((256, 256), dtype=int)
    stack = []
    i = 0
    j = -1
    while len(stack) != 16:
            tile = get_tile()
            if tile not in stack:
                stack.append(tile)
                tile = np.array(tile)
                j += 1
                if j == 4:
                    i += 1
                    j = 0  
                full_map[i * 64 : (i + 1) * 64, j * 64 : (j + 1) * 64] = tile
    return full_map


def plot_map(map_data, stations, modules):
    plt.imshow(map_data, cmap="terrain")
    for station in stations:
        color = "blue" if station["type"] == "C" else "red"
        plt.scatter(station["x"], station["y"], color=color, marker="o")
    for module in modules:
        plt.scatter(module[0], module[1], color="yellow", marker="*")
    plt.colorbar(label="Высота")
    plt.show()

"""
def find_peaks(map_data):
    peaks = maximum_filter(map_data, size=3) == map_data
    return np.argwhere(peaks)

def place_stations(map_data, peaks, cuper_price, engel_price):
    stations = []
    covered_area = np.zeros_like(map_data)

    for x, y in sorted(peaks, key=lambda p: -map_data[p[0], p[1]]):
        if covered_area[x, y] == 0:
            if np.random.rand() > 0.5:
                stations.append({"x": x, "y": y, "type": "C"})
                radius = 32
            else:
                stations.append({"x": x, "y": y, "type": "E"})
                radius = 64

            for i in range(max(0, x-radius), min(256, x+radius)):
                for j in range(max(0, y-radius), min(256, y+radius)):
                    if np.sqrt((x-i)**2 + (y-j)**2) <= radius:
                        covered_area[i, j] = 1

    return stations
"""

def main():
    coords = get_coords()
    map_data = create_map()

    # peaks = find_peaks(map_data)
    # stations = place_stations(map_data, peaks, coords['price'][0], coords['price'][1])

    plot_map(map_data, [], [coords['sender'], coords['listener']])

main()
