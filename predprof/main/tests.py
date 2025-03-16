from django.test import TestCase
from unittest.mock import patch
import numpy as np
from main.utils import (
    get_tile,
    get_coords,
    is_top,
    is_bottom,
    is_left,
    is_right
)


class MapTests(TestCase):
    @patch('main.utils.requests.get')
    def test_get_tile_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "status": "ok",
            "message": {
                "data": [[255] * 64 for _ in range(64)]
            }
        }
        result = get_tile()
        self.assertIsInstance(result, list)
        self.assertEqual(np.array(result).shape, (64, 64))

    @patch('main.utils.requests.get')
    def test_get_tile_failure(self, mock_get):
        mock_get.return_value.status_code = 404
        result = get_tile()
        self.assertIsNone(result)

    @patch('main.utils.requests.get')
    def test_get_coords_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "status": "ok",
            "message": {
                "sender": [0, 0],
                "listener": [255, 255]
            }
        }
        result = get_coords()
        self.assertEqual(result['sender'], [0, 0])
        self.assertEqual(result['listener'], [255, 255])

    def test_is_top_true(self):
        tile = np.full((64, 64), 0)
        tile[0, :] = 255
        self.assertTrue(is_top(tile))

    def test_is_top_false(self):
        tile = np.full((64, 64), 0)
        tile[0, 0:32] = 255
        self.assertFalse(is_top(tile))

    def test_is_bottom_true(self):
        tile = np.full((64, 64), 0)
        tile[-1, :] = 255
        self.assertTrue(is_bottom(tile))

    def test_is_bottom_false(self):
        tile = np.full((64, 64), 0)
        tile[-1, 0:32] = 255
        self.assertFalse(is_bottom(tile))

    def test_is_left_true(self):
        tile = np.full((64, 64), 0)
        tile[:, 0] = 255
        self.assertTrue(is_left(tile))

    def test_is_left_false(self):
        tile = np.full((64, 64), 0)
        tile[0:32, 0] = 255
        self.assertFalse(is_left(tile))

    def test_is_right_true(self):
        tile = np.full((64, 64), 0)
        tile[:, -1] = 255
        self.assertTrue(is_right(tile))

    def test_is_right_false(self):
        tile = np.full((64, 64), 0)
        tile[0:32, -1] = 255
        self.assertFalse(is_right(tile))
