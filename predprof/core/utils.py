import numpy as np
from scipy.ndimage import maximum_filter
import matplotlib.pyplot as plt


def find_peaks(map_data):
    peaks = maximum_filter(map_data, size=3) == map_data
    return np.argwhere(peaks)


def plot_map(map_data, stations, modules):
    plt.imshow(map_data, cmap='terrain')
    for station in stations:
        color = 'blue' if station['type'] == 'C' else 'red'
        plt.scatter(station['x'], station['y'], color=color, marker='o')
    for module in modules:
        plt.scatter(module['x'], module['y'], color='yellow', marker='*')
    plt.colorbar(label='Высота')
    plt.show()


def map_view(request):
    tiles = Tile.objects.all()
    map_data = np.block([[tile.data for tile in tiles]]) 
    return render(request, 'map.html', {'map_data': map_data})