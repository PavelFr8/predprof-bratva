from django.conf import settings

import requests
import json

import numpy as np
from scipy.ndimage import maximum_filter
import matplotlib.pyplot as plt
import matplotlib
from main.models import Tile


def get_tile():
    req = requests.get(f"{settings.API_URL}")
    # req = requests.get("https://olimp.miet.ru/ppo_it/api")
    if req:
        req = req.json()
    else:
        return None
    status = req.get("status")
    if status == "ok":
        data = req.get("message").get("data")
        return data
    return None


def get_coords():
    req = requests.get(f"{settings.API_URL}/coords")
    # req = requests.get("https://olimp.miet.ru/ppo_it/api/coords")
    if req:
        req = req.json()
    else:
        return None
    status = req.get("status")
    if status == "ok":
        coords = req.get("message")
        return coords
    return None


def is_top(tile):
    return np.all(tile[0, :] == 255)


def is_bottom(tile):
    return np.all(tile[-1, :] == 255)


def is_left(tile):
    return np.all(tile[:, 0] == 255)


def is_right(tile):
    return np.all(tile[:, -1] == 255)


def create_map():
    full_map = np.zeros((256, 256), dtype=int)
    tiles = {
        "top_left": None,
        "top_right": None,
        "bottom_left": None,
        "bottom_right": None,
        "top_row": [],
        "bottom_row": [],
        "left_col": [],
        "right_col": [],
        "inner": [],
    }

    stack = []
    while len(stack) != 16:
        tile = get_tile()
        if tile not in stack:
            stack.append(tile)

            tile_np = np.array(tile)

            if is_top(tile_np) and is_left(tile_np):
                tiles["top_left"] = tile_np
            elif is_top(tile_np) and is_right(tile_np):
                tiles["top_right"] = tile_np
            elif is_bottom(tile_np) and is_left(tile_np):
                tiles["bottom_left"] = tile_np
            elif is_bottom(tile_np) and is_right(tile_np):
                tiles["bottom_right"] = tile_np
            elif is_top(tile_np):
                tiles["top_row"].append(tile_np)
            elif is_bottom(tile_np):
                tiles["bottom_row"].append(tile_np)
            elif is_left(tile_np):
                tiles["left_col"].append(tile_np)
            elif is_right(tile_np):
                tiles["right_col"].append(tile_np)
            else:
                tiles["inner"].append(tile_np)

    full_map[0:64, 0:64] = tiles["top_left"]
    Tile.objects.create(x=0, y=0, data=json.dumps(tiles["top_left"].tolist()))
    full_map[0:64, -64:] = tiles["top_right"]
    Tile.objects.create(x=15, y=0, data=json.dumps(tiles["top_right"].tolist()))
    full_map[-64:, 0:64] = tiles["bottom_left"]
    Tile.objects.create(x=15, y=0, data=json.dumps(tiles["bottom_left"].tolist()))
    full_map[-64:, -64:] = tiles["bottom_right"]
    Tile.objects.create(x=15, y=15, data=json.dumps(tiles["bottom_right"].tolist()))

    for i in range(1, 3):
        full_map[0:64, i * 64 : (i + 1) * 64] = tiles["top_row"][i - 1]
        Tile.objects.create(
            x=i, y=0, data=json.dumps(tiles["top_row"][i - 1].tolist())
        )
        full_map[-64:, i * 64 : (i + 1) * 64] = tiles["bottom_row"][i - 1]
        Tile.objects.create(
            x=0, y=i, data=json.dumps(tiles["bottom_row"][i - 1].tolist())
        )
        full_map[i * 64 : (i + 1) * 64, 0:64] = tiles["left_col"][i - 1]
        Tile.objects.create(
            x=15, y=i, data=json.dumps(tiles["left_col"][i - 1].tolist())
        )
        full_map[i * 64 : (i + 1) * 64, -64:] = tiles["right_col"][i - 1]
        Tile.objects.create(
            x=i, y=15, data=json.dumps(tiles["right_col"][i - 1].tolist())
        )

    idx = 0
    for i in range(1, 3):
        for j in range(1, 3):
            full_map[i * 64 : (i + 1) * 64, j * 64 : (j + 1) * 64] = tiles["inner"][idx]
            idx += 1

    return full_map


def plot_map(map_data, stations, modules):
    matplotlib.use("agg")
    plt.imshow(map_data, cmap="terrain")
    for station in stations:
        color = "blue" if station["type"] == "C" else "red"
        plt.scatter(station["x"], station["y"], color=color, marker="o")
    for module in modules:
        plt.scatter(module[0], module[1], color="yellow", marker="*")
    plt.colorbar(label="Высота")
    plt.savefig("static_dev/img/map.png")
    plt.close()


def create_plot():
    coords = get_coords()
    map_data = create_map()
    if coords is None or map_data is None:
        return None

    plot_map(map_data, [], [coords['sender'], coords['listener']])
    return True
