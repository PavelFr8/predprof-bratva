from django.shortcuts import render
import numpy as np

from main.models import Tile


def map_view(request):
    tiles = Tile.objects.all()
    map_data = np.block([[tile.data for tile in tiles]])
    return render(request, "map.html", {"map_data": map_data})
